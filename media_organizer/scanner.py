import hashlib
import json
import re
import subprocess
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path
from typing import DefaultDict, Dict, Iterable, List, Optional, Tuple

try:
    from PIL import Image
except ImportError:  # pragma: no cover - optional dependency at runtime
    Image = None

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
FOLDER_DATE_PREFIX_PATTERN = re.compile(r"^(20\d{2}|19\d{2})-(\d{2})-(\d{2})(?:\D|$)")
NAMED_YEAR_BUCKET_PATTERN = re.compile(r"^photos from ((?:20|19)\d{2})$", re.IGNORECASE)
ATES_CAMERA_FOLDER_PATTERN = re.compile(r"^\d{3}_(\d{2})(\d{2})(?:\s+-\s+copy)?$", re.IGNORECASE)
EPOCH_TS_PATTERN = re.compile(r"(?<!\d)(\d{10}|\d{13})(?!\d)")
YEAR_PREFIXED_SEQUENCE_PATTERN = re.compile(r"^(20\d{2}|19\d{2})\d{4,}$")
EXIF_DATETIME_PATTERN = re.compile(r"(20\d{2}|19\d{2}):(\d{2}):(\d{2})[ T](\d{2}):(\d{2}):(\d{2})")
ISO_DATETIME_PATTERN = re.compile(r"(20\d{2}|19\d{2})-(\d{2})-(\d{2})(?:[ T]\d{2}:\d{2}:\d{2})?")
MIN_FOLDER_INFERRED_YEAR = 1990
MONTH_NAME_TO_NUMBER = {
    "jan": "01",
    "feb": "02",
    "mar": "03",
    "apr": "04",
    "may": "05",
    "jun": "06",
    "jul": "07",
    "aug": "08",
    "sep": "09",
    "sept": "09",
    "oct": "10",
    "nov": "11",
    "dec": "12",
}
SOURCE_LABEL_ALIASES = {
    "jonel": "Jonel",
    "pictures from ates camera": "Jonel",
    "samyras 16": "Samyra",
    "ceu": "CEU",
    "tito osias": "Tito-Osias",
}
SPECIAL_DESTINATION_FOLDERS = {
    "ceu": Path("Shared") / "CEU" / "Undated",
    "nanay80": Path("Shared") / "nanayCora80th",
    "googleearth": Path("Reference") / "googleEarth",
    "morepics": Path("Reference") / "Legacy-Scans" / "morePics",
    "pexels": Path("Reference") / "Pexels",
    "screenshots": Path("Reference") / "Screenshots",
    "wallpapers": Path("Reference") / "Wallpapers",
}
SPECIAL_DESTINATION_FILES = {
    "joy.png": Path("Reference") / "Legacy-Scans" / "loose-root" / "joy.png",
}
WEAK_SOURCE_LABEL_PATTERNS = (
    re.compile(r"^\d{1,2}$"),
    re.compile(r"^(19|20)\d{2}$"),
    re.compile(r"^(19|20)\d{2}(0[1-9]|1[0-2])$"),
    re.compile(r"^(19|20)\d{2}[-_]\d{2}$"),
    re.compile(r"^(19|20)\d{2}[-_]\d{2}[-_]\d{2}$"),
    re.compile(r"^(19|20)\d{2}\d{2}\d{2}$"),
)
VIDEO_PROJECT_FILENAME_PATTERNS = (
    re.compile(r"^cs50w-project\d+\.(mp4|mov|m4v|avi|mkv|webm)$", re.IGNORECASE),
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
    special_destination = derive_special_destination(path, root_path)
    project_destination = derive_project_destination(path, root_type, root_path)

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

    if special_destination is not None:
        if hash_media:
            if category in ("image", "video", "project_video", "screen_recording"):
                record.sha256 = hash_file(path)
        record.proposed_relative_destination = special_destination
    elif category in ("sidecar", "cache"):
        record.proposed_relative_destination = plan_destination(path, root_type, category, inferred_date, root_path)
    elif project_destination is not None:
        if hash_media:
            if category in ("image", "video", "project_video", "screen_recording"):
                record.sha256 = hash_file(path)
        record.proposed_relative_destination = project_destination
    elif category in ("image", "video", "project_video", "screen_recording"):
        if hash_media:
            record.sha256 = hash_file(path)
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

    year_only_date = infer_year_only_date_from_name(name)
    if year_only_date:
        return year_only_date, "filename"

    metadata_date = infer_embedded_metadata_date(path)
    if metadata_date:
        return metadata_date, "metadata"

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
    candidate = build_date_from_ates_camera_parts(parts)
    if candidate:
        return candidate

    for part in parts:
        candidate = build_date_from_prefixed_part(part)
        if candidate:
            return candidate

    for part in parts:
        candidate = build_date_from_named_year_bucket(part)
        if candidate:
            return candidate

    for index in range(len(parts) - 1):
        candidate = build_date_from_year_and_month_name(parts[index], parts[index + 1])
        if candidate:
            return candidate

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


def build_date_from_ates_camera_parts(parts: Tuple[str, ...]) -> Optional[str]:
    for index in range(len(parts) - 1):
        parent = parts[index].strip().lower()
        child = parts[index + 1].strip()
        if parent != "pictures from ates camera":
            continue

        match = ATES_CAMERA_FOLDER_PATTERN.match(child)
        if not match:
            continue

        month, day = match.groups()
        month_value = int(month)
        year = "2013" if month_value >= 6 else "2014"
        return build_date_from_parts(year, month, day)

    return None


def build_date_from_prefixed_part(part: str) -> Optional[str]:
    match = FOLDER_DATE_PREFIX_PATTERN.match(part)
    if not match:
        return None

    year, month, day = match.groups()
    return build_date_from_parts(year, month, day)


def build_date_from_named_year_bucket(part: str) -> Optional[str]:
    match = NAMED_YEAR_BUCKET_PATTERN.match(part)
    if not match:
        return None

    return build_date_from_parts(match.group(1), "01", "01")


def build_date_from_year_and_month_name(year_part: str, month_part: str) -> Optional[str]:
    month_number = MONTH_NAME_TO_NUMBER.get(month_part.strip().lower())
    if not month_number:
        return None

    return build_date_from_parts(year_part, month_number, "01")


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


def infer_year_only_date_from_name(name: str) -> Optional[str]:
    match = YEAR_PREFIXED_SEQUENCE_PATTERN.match(name)
    if not match:
        return None

    return build_date_from_parts(match.group(1), "01", "01")


def infer_embedded_metadata_date(path: Path) -> Optional[str]:
    image_metadata_date = infer_exif_date(path)
    if image_metadata_date:
        return image_metadata_date

    return infer_video_metadata_date(path)


def infer_exif_date(path: Path) -> Optional[str]:
    if Image is None or path.suffix.lower() not in IMAGE_EXTENSIONS:
        return None

    try:
        with Image.open(path) as image_handle:
            exif = image_handle.getexif()
    except (OSError, ValueError, SyntaxError):
        return None

    if not exif:
        return None

    for tag in (36867, 36868, 306):
        value = exif.get(tag)
        if not value:
            continue

        inferred = extract_date_from_metadata_value(str(value))
        if inferred:
            return inferred

    return None


def infer_video_metadata_date(path: Path) -> Optional[str]:
    if path.suffix.lower() not in VIDEO_EXTENSIONS:
        return None

    try:
        result = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-print_format",
                "json",
                "-show_entries",
                "format_tags:stream_tags",
                str(path),
            ],
            capture_output=True,
            text=True,
            check=True,
        )
    except (FileNotFoundError, PermissionError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return None

    try:
        probe_data = json.loads(result.stdout or "{}")
    except json.JSONDecodeError:
        return None

    format_tags = probe_data.get("format", {}).get("tags", {})
    candidate_values = list(format_tags.values())

    for stream in probe_data.get("streams", []):
        candidate_values.extend(stream.get("tags", {}).values())

    for value in candidate_values:
        if not value:
            continue
        inferred = extract_date_from_metadata_value(str(value))
        if inferred:
            return inferred

    return None


def extract_date_from_metadata_value(raw_value: str) -> Optional[str]:
    match = EXIF_DATETIME_PATTERN.search(raw_value)
    if match:
        year, month, day, _, _, _ = match.groups()
        try:
            return date(int(year), int(month), int(day)).isoformat()
        except ValueError:
            return None

    iso_match = ISO_DATETIME_PATTERN.search(raw_value)
    if iso_match:
        year, month, day = iso_match.groups()
        try:
            return date(int(year), int(month), int(day)).isoformat()
        except ValueError:
            return None

    return None


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
    destination_root = derive_destination_root(source_label)
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
        return str(Path(destination_root) / year / "{0}_{1}".format(date_value, source_label) / path.name)
    return str(relative)


def sanitize_label(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "-", value.strip())
    return cleaned.strip("-") or "root"


def derive_source_label(relative_path: Path, root_path: Path) -> str:
    parent = relative_path.parent
    if parent == Path("."):
        return sanitize_label(root_path.name)

    for part in reversed(parent.parts):
        aliased_label = get_source_label_alias(part)
        if aliased_label:
            return aliased_label

    for part in reversed(parent.parts):
        if not is_weak_source_label(part):
            return sanitize_label(part)

    return sanitize_label(root_path.name)


def get_source_label_alias(value: str) -> Optional[str]:
    return SOURCE_LABEL_ALIASES.get(value.strip().lower())


def derive_destination_root(source_label: str) -> str:
    if source_label == "Jonel":
        return str(Path("Shared") / "Jonel")
    if source_label == "Samyra":
        return str(Path("Shared") / "Samyra")
    if source_label == "CEU":
        return str(Path("Shared") / "CEU")
    if source_label == "Tito-Osias":
        return str(Path("Shared") / "Tito-Osias")
    return "Library"


def derive_special_destination(path: Path, root_path: Path) -> Optional[str]:
    try:
        relative = path.relative_to(root_path)
    except ValueError:
        return None

    if not relative.parts:
        return None

    if len(relative.parts) == 1:
        file_destination = SPECIAL_DESTINATION_FILES.get(relative.name.lower())
        if file_destination is not None:
            return str(file_destination)

    destination_root = SPECIAL_DESTINATION_FOLDERS.get(relative.parts[0].strip().lower())
    if destination_root is None:
        return None

    remainder = Path(*relative.parts[1:]) if len(relative.parts) > 1 else Path(path.name)
    return str(destination_root / remainder)


def derive_project_destination(path: Path, root_type: str, root_path: Path) -> Optional[str]:
    if root_type != "videos":
        return None

    try:
        relative = path.relative_to(root_path)
    except ValueError:
        return None

    if len(relative.parts) == 1 and any(pattern.match(path.name) for pattern in VIDEO_PROJECT_FILENAME_PATTERNS):
        return str(Path("Projects") / "cs50w" / path.name)

    if not any(part.strip().lower() in PROJECT_DIRECTORY_NAMES for part in relative.parts):
        return None

    return str(Path("Projects") / relative)


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
