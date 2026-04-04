import hashlib
import json
import re
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path
from typing import DefaultDict, Dict, Iterable, List, Optional, Tuple

from media_organizer.config import (
    CACHE_DIRECTORY_NAMES,
    IMAGE_EXTENSIONS,
    PROJECT_DIRECTORY_NAMES,
    SCREEN_RECORDING_PREFIXES,
    SIDECAR_EXTENSIONS,
    VIDEO_EXTENSIONS,
    Roots,
)
from media_organizer.models import FileRecord, ScanReport, ScanSummary


DATE_PATTERNS = (
    re.compile(r"(?<!\d)(20\d{2}|19\d{2})[-_]?([01]\d)[-_]?([0-3]\d)(?!\d)"),
    re.compile(r"(?<!\d)(20\d{2}|19\d{2})[-_]?([01]\d)(?!\d)"),
)
EPOCH_TS_PATTERN = re.compile(r"(?<!\d)(\d{10}|\d{13})(?!\d)")
MIN_FOLDER_INFERRED_YEAR = 1990
WEAK_SOURCE_LABEL_PATTERNS = (
    re.compile(r"^\d{1,2}$"),
    re.compile(r"^(19|20)\d{2}$"),
    re.compile(r"^(19|20)\d{2}(0[1-9]|1[0-2])$"),
    re.compile(r"^(19|20)\d{2}[-_]\d{2}$"),
    re.compile(r"^(19|20)\d{2}[-_]\d{2}[-_]\d{2}$"),
    re.compile(r"^(19|20)\d{2}\d{2}\d{2}$"),
)


def build_scan_report(roots: Roots, hash_media: bool = True) -> ScanReport:
    files: List[FileRecord] = []
    media_by_size: DefaultDict[int, List[Tuple[FileRecord, Path]]] = defaultdict(list)
    sidecar_candidates: Dict[str, List[FileRecord]] = defaultdict(list)

    for root_type, root_path in (("pictures", roots.pictures), ("videos", roots.videos)):
        for path in iter_files(root_path):
            record = build_file_record(path=path, root_type=root_type, root_path=root_path, hash_media=False)
            files.append(record)
            if record.category in ("image", "video", "project_video", "screen_recording") and hash_media:
                media_by_size[record.size_bytes].append((record, path))
            if record.category == "sidecar":
                sidecar_candidates[Path(record.path).stem].append(record)

    hash_buckets = hash_duplicate_candidates(media_by_size) if hash_media else {}
    duplicate_groups = assign_duplicate_groups(hash_buckets)
    attach_sidecar_links(files, sidecar_candidates)
    summary = build_summary(files, duplicate_groups)

    return ScanReport(
        generated_at=datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
        roots={"pictures": str(roots.pictures), "videos": str(roots.videos)},
        summary=summary,
        files=sorted(files, key=lambda item: item.path),
        duplicate_groups=duplicate_groups,
    )


def iter_files(root: Path) -> Iterable[Path]:
    if not root.exists():
        return []

    stack = [root]
    while stack:
        current = stack.pop()
        try:
            entries = sorted(current.iterdir(), key=lambda entry: entry.name.lower())
        except PermissionError:
            continue

        for entry in entries:
            if entry.is_dir():
                stack.append(entry)
                continue
            if entry.is_file():
                yield entry


def build_file_record(path: Path, root_type: str, root_path: Path, hash_media: bool) -> FileRecord:
    stat = path.stat()
    category = classify_path(path, root_type=root_type)
    inferred_date, date_source = infer_date(path, root_path, stat.st_mtime)

    record = FileRecord(
        path=str(path),
        root_type=root_type,
        category=category,
        extension=path.suffix.lower(),
        size_bytes=stat.st_size,
        modified_at=datetime.fromtimestamp(stat.st_mtime).isoformat(),
        inferred_date=inferred_date,
        date_source=date_source,
        notes=[],
    )

    if category in ("image", "video", "project_video", "screen_recording"):
        if hash_media:
            record.sha256 = hash_file(path)
        record.proposed_relative_destination = plan_destination(path, root_type, category, inferred_date, root_path)
    elif category in ("sidecar", "cache"):
        record.proposed_relative_destination = plan_destination(path, root_type, category, inferred_date, root_path)
    else:
        record.proposed_relative_destination = None

    if category == "unknown":
        record.notes.append("unclassified extension")

    return record


def hash_duplicate_candidates(
    media_by_size: Dict[int, List[Tuple[FileRecord, Path]]]
) -> Dict[str, List[FileRecord]]:
    hash_buckets: DefaultDict[str, List[FileRecord]] = defaultdict(list)
    for size_bytes, candidates in media_by_size.items():
        if size_bytes == 0 or len(candidates) < 2:
            continue
        for record, path in candidates:
            record.sha256 = hash_file(path)
            hash_buckets[record.sha256].append(record)
    return hash_buckets


def classify_path(path: Path, root_type: str) -> str:
    extension = path.suffix.lower()
    lower_parts = [part.lower() for part in path.parts]
    filename = path.name.lower()

    if any(part in CACHE_DIRECTORY_NAMES for part in lower_parts):
        return "cache"
    if extension in IMAGE_EXTENSIONS:
        return "image"
    if extension in VIDEO_EXTENSIONS:
        if root_type == "videos":
            if any(part in PROJECT_DIRECTORY_NAMES for part in lower_parts):
                return "project_video"
            if filename.startswith(SCREEN_RECORDING_PREFIXES):
                return "screen_recording"
        return "video"
    if extension in SIDECAR_EXTENSIONS:
        return "sidecar"
    return "unknown"


def infer_date(path: Path, root_path: Path, modified_ts: float) -> Tuple[Optional[str], Optional[str]]:
    name = path.stem
    for pattern in DATE_PATTERNS:
        match = pattern.search(name)
        if not match:
            continue
        groups = match.groups()
        if len(groups) == 3:
            year, month, day = groups
        else:
            year, month = groups
            day = "01"
        try:
            inferred = datetime(int(year), int(month), int(day)).date().isoformat()
        except ValueError:
            continue
        return inferred, "filename"

    epoch_date = infer_epoch_date_from_name(name)
    if epoch_date:
        return epoch_date, "filename"

    relative_parent = get_relative_parent_parts(path, root_path)
    folder_date = infer_date_from_parts(relative_parent)
    if folder_date:
        return folder_date, "path"

    modified = datetime.fromtimestamp(modified_ts).date().isoformat()
    return modified, "mtime"


def get_relative_parent_parts(path: Path, root_path: Path) -> Tuple[str, ...]:
    try:
        return path.relative_to(root_path).parent.parts
    except ValueError:
        return path.parent.parts


def infer_date_from_parts(parts: Tuple[str, ...]) -> Optional[str]:
    for part in parts:
        candidate = build_date_from_compact_part(part)
        if candidate:
            return candidate

    for index in range(len(parts) - 2):
        candidate = build_date_from_parts(parts[index], parts[index + 1], parts[index + 2])
        if candidate:
            return candidate

    for index in range(len(parts) - 1):
        candidate = build_date_from_parts(parts[index], parts[index + 1], None)
        if candidate:
            return candidate

    return None


def build_date_from_parts(year_part: str, month_part: str, day_part: Optional[str]) -> Optional[str]:
    if not (year_part.isdigit() and month_part.isdigit()):
        return None

    year = int(year_part)
    month = int(month_part)
    day = int(day_part) if day_part and day_part.isdigit() else 1

    if year < MIN_FOLDER_INFERRED_YEAR or year > date.today().year + 1:
        return None

    try:
        return date(year, month, day).isoformat()
    except ValueError:
        return None


def build_date_from_compact_part(part: str) -> Optional[str]:
    if not part.isdigit():
        return None

    if len(part) == 6:
        return build_date_from_parts(part[:4], part[4:6], None)

    if len(part) == 8:
        return build_date_from_parts(part[:4], part[4:6], part[6:8])

    return None


def infer_epoch_date_from_name(name: str) -> Optional[str]:
    match = EPOCH_TS_PATTERN.search(name)
    if not match:
        return None

    raw_value = match.group(1)
    if len(raw_value) == 13:
        timestamp = int(raw_value) / 1000.0
    else:
        timestamp = float(raw_value)

    try:
        inferred = datetime.fromtimestamp(timestamp).date()
    except (OverflowError, OSError, ValueError):
        return None

    if inferred.year < MIN_FOLDER_INFERRED_YEAR or inferred.year > date.today().year + 1:
        return None

    return inferred.isoformat()


def hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def assign_duplicate_groups(hash_buckets: Dict[str, List[FileRecord]]) -> Dict[str, List[str]]:
    duplicate_groups: Dict[str, List[str]] = {}
    group_index = 0
    for sha256, records in sorted(hash_buckets.items()):
        if len(records) < 2:
            continue
        group_index += 1
        group_id = "dup-{0:04d}".format(group_index)
        duplicate_groups[group_id] = [record.path for record in sorted(records, key=lambda item: item.path)]
        for record in records:
            record.duplicate_group = group_id
    return duplicate_groups


def attach_sidecar_links(files: List[FileRecord], sidecar_candidates: Dict[str, List[FileRecord]]) -> None:
    media_by_stem: DefaultDict[str, List[FileRecord]] = defaultdict(list)
    media_by_name: DefaultDict[str, List[FileRecord]] = defaultdict(list)
    for record in files:
        if record.category in ("image", "video", "project_video", "screen_recording"):
            media_path = Path(record.path)
            media_by_stem[media_path.stem].append(record)
            media_by_name[media_path.name].append(record)

    for stem, sidecars in sidecar_candidates.items():
        direct_matches = media_by_stem.get(stem, [])
        if direct_matches:
            target = sorted(direct_matches, key=lambda item: item.path)[0]
            for sidecar in sidecars:
                sidecar.sidecar_for = target.path
            continue

        trimmed_stem = normalize_sidecar_stem(stem)
        trimmed_matches = media_by_stem.get(trimmed_stem, [])
        if trimmed_matches:
            target = sorted(trimmed_matches, key=lambda item: item.path)[0]
            for sidecar in sidecars:
                sidecar.sidecar_for = target.path
            continue

        name_matches = media_by_name.get(trimmed_stem, [])
        if name_matches:
            target = sorted(name_matches, key=lambda item: item.path)[0]
            for sidecar in sidecars:
                sidecar.sidecar_for = target.path


def build_summary(files: List[FileRecord], duplicate_groups: Dict[str, List[str]]) -> ScanSummary:
    summary = ScanSummary()
    summary.total_files = len(files)
    summary.total_bytes = sum(record.size_bytes for record in files)
    summary.images = sum(1 for record in files if record.category == "image")
    summary.videos = sum(
        1 for record in files if record.category in ("video", "project_video", "screen_recording")
    )
    summary.sidecars = sum(1 for record in files if record.category == "sidecar")
    summary.caches = sum(1 for record in files if record.category == "cache")
    summary.unknown = sum(1 for record in files if record.category == "unknown")
    summary.duplicate_groups = len(duplicate_groups)
    summary.duplicate_files = sum(len(group) for group in duplicate_groups.values())
    return summary


def plan_destination(
    path: Path,
    root_type: str,
    category: str,
    inferred_date: Optional[str],
    root_path: Path,
) -> str:
    relative = path.relative_to(root_path)
    source_label = derive_source_label(relative, root_path)
    date_value = inferred_date or "unknown-date"
    year = date_value[:4] if len(date_value) >= 4 else "unknown"

    if category == "cache":
        return str(Path("App-Caches") / relative)
    if category == "sidecar":
        return str(Path("Exports") / relative)
    if category == "screen_recording":
        return str(Path("ScreenRecordings") / year / "{0}_{1}".format(date_value, source_label) / path.name)
    if category == "project_video":
        return str(Path("Projects") / relative)
    if category in ("image", "video"):
        return str(Path("Library") / year / "{0}_{1}".format(date_value, source_label) / path.name)
    return str(relative)


def sanitize_label(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "-", value.strip())
    return cleaned.strip("-") or "root"


def derive_source_label(relative_path: Path, root_path: Path) -> str:
    parent = relative_path.parent
    if parent == Path("."):
        return sanitize_label(root_path.name)

    for part in reversed(parent.parts):
        if not is_weak_source_label(part):
            return sanitize_label(part)

    return sanitize_label(root_path.name)


def is_weak_source_label(value: str) -> bool:
    candidate = value.strip()
    if not candidate:
        return True

    lowered = candidate.lower()
    if lowered in {"dcim", "100media", "camera", "photos", "videos"}:
        return True

    return any(pattern.match(lowered) for pattern in WEAK_SOURCE_LABEL_PATTERNS)


def normalize_sidecar_stem(stem: str) -> str:
    normalized = stem.replace(".supplemental-metadata", "")
    for extension in sorted(IMAGE_EXTENSIONS | VIDEO_EXTENSIONS, key=len, reverse=True):
        if normalized.lower().endswith(extension):
            return normalized[: -len(extension)]
    return normalized


def write_report(report: ScanReport, report_path: Path) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with report_path.open("w", encoding="utf-8") as handle:
        json.dump(report.to_dict(), handle, indent=2, sort_keys=False)
        handle.write("\n")
