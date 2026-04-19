import argparse
import hashlib
import json
import os
import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

from media_organizer.config import Roots
from media_organizer.scanner import build_file_record, build_scan_report, write_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="media-organizer",
        description="Safety-first scan and planning tool for personal media libraries.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    scan_parser = subparsers.add_parser(
        "scan",
        help="Scan media roots and write a dry-run report with proposed destinations.",
    )
    scan_parser.add_argument("--pictures-root", required=True, help="Root directory to scan for pictures.")
    scan_parser.add_argument("--videos-root", required=True, help="Root directory to scan for videos.")
    scan_parser.add_argument("--report", required=True, help="Path to write the JSON report.")
    scan_parser.add_argument(
        "--skip-hash",
        action="store_true",
        help="Skip SHA-256 hashing. Faster, but duplicate detection will be disabled.",
    )

    preview_parser = subparsers.add_parser(
        "preview",
        help="Preview planned destinations for specific files without running a full scan.",
    )
    preview_parser.add_argument("--pictures-root", required=True, help="Root directory used for picture planning.")
    preview_parser.add_argument("--videos-root", required=True, help="Root directory used for video planning.")
    preview_parser.add_argument(
        "--path",
        action="append",
        required=True,
        help="Specific file path to preview. Repeat for multiple files.",
    )

    suspicious_parser = subparsers.add_parser(
        "suspicious-report",
        help="Print suspicious planned destinations from an existing JSON scan report.",
    )
    suspicious_parser.add_argument("--report", required=True, help="Path to an existing JSON scan report.")
    suspicious_parser.add_argument(
        "--limit",
        type=int,
        default=25,
        help="Maximum number of suspicious entries to print.",
    )

    mtime_parser = subparsers.add_parser(
        "mtime-summary",
        help="Group remaining mtime-dated media from an existing JSON scan report.",
    )
    mtime_parser.add_argument("--report", required=True, help="Path to an existing JSON scan report.")
    mtime_parser.add_argument(
        "--limit",
        type=int,
        default=25,
        help="Maximum number of grouped mtime patterns to print.",
    )

    google_photos_parser = subparsers.add_parser(
        "google-photos-summary",
        help="Summarize Google Photos Takeout folders from an existing JSON scan report.",
    )
    google_photos_parser.add_argument("--report", required=True, help="Path to an existing JSON scan report.")
    google_photos_parser.add_argument(
        "--limit",
        type=int,
        default=25,
        help="Maximum number of Google Photos folders to print.",
    )

    google_photos_folder_parser = subparsers.add_parser(
        "google-photos-folder",
        help="Inspect one Google Photos Takeout folder from an existing JSON scan report.",
    )
    google_photos_folder_parser.add_argument("--report", required=True, help="Path to an existing JSON scan report.")
    google_photos_folder_parser.add_argument("--folder", required=True, help="Google Photos top-level folder name.")
    google_photos_folder_parser.add_argument(
        "--limit",
        type=int,
        default=25,
        help="Maximum number of grouped items to print.",
    )

    google_photos_received_parser = subparsers.add_parser(
        "google-photos-received",
        help="Print only received_* Google Photos items grouped by folder.",
    )
    google_photos_received_parser.add_argument("--report", required=True, help="Path to an existing JSON scan report.")
    google_photos_received_parser.add_argument(
        "--limit",
        type=int,
        default=25,
        help="Maximum number of folders to print.",
    )

    google_photos_sidecars_parser = subparsers.add_parser(
        "google-photos-sidecar-gaps",
        help="Print sidecar-only or unmatched-sidecar Google Photos groups.",
    )
    google_photos_sidecars_parser.add_argument("--report", required=True, help="Path to an existing JSON scan report.")
    google_photos_sidecars_parser.add_argument(
        "--limit",
        type=int,
        default=25,
        help="Maximum number of sidecar groups to print.",
    )

    google_photos_compare_parser = subparsers.add_parser(
        "google-photos-compare",
        help="Compare Google Photos media against the rest of the library by normalized name and date.",
    )
    google_photos_compare_parser.add_argument("--report", required=True, help="Path to an existing JSON scan report.")
    google_photos_compare_parser.add_argument(
        "--limit",
        type=int,
        default=25,
        help="Maximum number of matched groups to print.",
    )
    google_photos_compare_parser.add_argument(
        "--date",
        action="append",
        help="Only include matches for this inferred date. Repeat for multiple dates.",
    )
    google_photos_compare_parser.add_argument(
        "--rest-folder-contains",
        help="Only include matches whose non-Google sample path contains this text.",
    )
    google_photos_compare_parser.add_argument(
        "--output",
        help="Optional path to write the filtered match groups as JSON.",
    )

    review_package_parser = subparsers.add_parser(
        "final-review-package",
        help="Write a final review bundle with summaries and focused JSON slices.",
    )
    review_package_parser.add_argument("--report", required=True, help="Path to an existing JSON scan report.")
    review_package_parser.add_argument("--output-dir", required=True, help="Directory to write the review bundle.")

    apply_parser = subparsers.add_parser(
        "apply",
        help="Build a conservative move manifest from a scan report and optionally execute it.",
    )
    apply_parser.add_argument("--report", required=True, help="Path to an existing JSON scan report.")
    apply_parser.add_argument("--dest-root", required=True, help="Destination root for applied moves.")
    apply_parser.add_argument(
        "--manifest",
        help="Optional path to write the planned operations and skipped items as JSON.",
    )
    apply_parser.add_argument(
        "--log",
        help="Optional path to write apply results as JSON. Useful for executed runs.",
    )
    apply_parser.add_argument(
        "--execute",
        action="store_true",
        help="Perform real moves. Without this flag the command is dry-run only.",
    )
    apply_parser.add_argument(
        "--include-mtime",
        action="store_true",
        help="Include items whose inferred date came from mtime.",
    )
    apply_parser.add_argument(
        "--include-duplicates",
        action="store_true",
        help="Include duplicate-group members.",
    )
    apply_parser.add_argument(
        "--include-received",
        action="store_true",
        help="Include Google Photos received_* artifacts.",
    )
    apply_parser.add_argument(
        "--include-google-takeout",
        action="store_true",
        help="Include all Google Takeout media and sidecars.",
    )
    apply_parser.add_argument(
        "--include-unmatched-sidecars",
        action="store_true",
        help="Include unmatched sidecars or sidecars whose media target is excluded.",
    )
    apply_parser.add_argument(
        "--include-unknown",
        action="store_true",
        help="Include files classified as unknown.",
    )
    apply_parser.add_argument(
        "--include-caches",
        action="store_true",
        help="Include cache files that would otherwise route to App-Caches/.",
    )
    apply_parser.add_argument(
        "--include-pleasantharmony",
        action="store_true",
        help="Include files routed under Projects/PleasantHarmony/.",
    )
    return parser


def main(argv: Optional[list] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "scan":
        roots = Roots(pictures=Path(args.pictures_root).expanduser(), videos=Path(args.videos_root).expanduser())
        report = build_scan_report(roots=roots, hash_media=not args.skip_hash)
        write_report(report, Path(args.report).expanduser())
        print("Scanned {0} files; report written to {1}".format(report.summary.total_files, args.report))
        return 0

    if args.command == "preview":
        roots = Roots(pictures=Path(args.pictures_root).expanduser(), videos=Path(args.videos_root).expanduser())
        for raw_path in args.path:
            preview_path = Path(raw_path).expanduser()
            root_type, root_path = resolve_preview_root(preview_path, roots)
            record = build_file_record(preview_path, root_type=root_type, root_path=root_path, hash_media=False)
            print("{0} -> {1}".format(record.path, record.proposed_relative_destination or "[no destination]"))
        return 0

    if args.command == "suspicious-report":
        report_path = Path(args.report).expanduser()
        report_data = json.loads(report_path.read_text(encoding="utf-8"))
        suspicious_files = collect_suspicious_report_entries(report_data)

        print(
            "Found {0} suspicious planned destinations in {1}".format(
                len(suspicious_files), report_path
            )
        )
        for item in suspicious_files[: args.limit]:
            print(
                "{0} | {1} | date={2} ({3}) | reasons={4}".format(
                    item["path"],
                    item["destination"],
                    item.get("inferred_date") or "unknown",
                    item.get("date_source") or "unknown",
                    ",".join(item["reasons"]),
                )
            )
        return 0

    if args.command == "mtime-summary":
        report_path = Path(args.report).expanduser()
        report_data = json.loads(report_path.read_text(encoding="utf-8"))
        mtime_groups = collect_mtime_summary_groups(report_data)

        print(
            "Found {0} grouped mtime patterns across {1} files in {2}".format(
                len(mtime_groups),
                sum(item["count"] for item in mtime_groups),
                report_path,
            )
        )
        for item in mtime_groups[: args.limit]:
            print(
                "{0} files | folder={1} | pattern={2} | sample={3}".format(
                    item["count"],
                    item["folder"],
                    item["pattern"],
                    item["sample"],
                )
            )
        return 0

    if args.command == "google-photos-summary":
        report_path = Path(args.report).expanduser()
        report_data = json.loads(report_path.read_text(encoding="utf-8"))
        summaries = collect_google_photos_summary(report_data)

        print(
            "Found {0} Google Photos folders in {1}".format(
                len(summaries),
                report_path,
            )
        )
        for item in summaries[: args.limit]:
            print(
                "{folder} | media={media} sidecars={sidecars} edited={edited} received={received} "
                "mtime={mtime} metadata={metadata} path={path} filename={filename} sample={sample}".format(
                    **item
                )
            )
        return 0

    if args.command == "google-photos-folder":
        report_path = Path(args.report).expanduser()
        report_data = json.loads(report_path.read_text(encoding="utf-8"))
        folder_summary = inspect_google_photos_folder(report_data, args.folder)

        if folder_summary is None:
            print("Google Photos folder not found: {0}".format(args.folder))
            return 1

        print(
            "{folder} | media={media} sidecars={sidecars} edited={edited} received={received} "
            "unmatched_sidecars={unmatched_sidecars}".format(**folder_summary)
        )
        for item in folder_summary["groups"][: args.limit]:
            print(
                "{kind} | count={count} sidecars={sidecars} name={name} sample={sample}".format(
                    **item
                )
            )
        return 0

    if args.command == "google-photos-received":
        report_path = Path(args.report).expanduser()
        report_data = json.loads(report_path.read_text(encoding="utf-8"))
        received_groups = collect_google_photos_received(report_data)

        print(
            "Found {0} Google Photos folders with received_* items in {1}".format(
                len(received_groups),
                report_path,
            )
        )
        for item in received_groups[: args.limit]:
            print(
                "{folder} | media={media} sidecars={sidecars} date_sources={date_sources} sample={sample}".format(
                    **item
                )
            )
        return 0

    if args.command == "google-photos-sidecar-gaps":
        report_path = Path(args.report).expanduser()
        report_data = json.loads(report_path.read_text(encoding="utf-8"))
        sidecar_gaps = collect_google_photos_sidecar_gaps(report_data)

        print(
            "Found {0} sidecar-only Google Photos groups in {1}".format(
                len(sidecar_gaps),
                report_path,
            )
        )
        for item in sidecar_gaps[: args.limit]:
            print(
                "{folder} | sidecars={sidecars} name={name} sample={sample}".format(
                    **item
                )
            )
        return 0

    if args.command == "google-photos-compare":
        report_path = Path(args.report).expanduser()
        report_data = json.loads(report_path.read_text(encoding="utf-8"))
        comparisons = collect_google_photos_matches(
            report_data,
            dates=args.date,
            rest_folder_contains=args.rest_folder_contains,
        )

        if args.output:
            output_path = Path(args.output).expanduser()
            write_json_output(
                output_path,
                {
                    "report": str(report_path),
                    "dates": args.date or [],
                    "rest_folder_contains": args.rest_folder_contains,
                    "match_count": len(comparisons),
                "matches": comparisons,
            },
            )
            print("Wrote {0} Google Photos match groups to {1}".format(len(comparisons), output_path))
            return 0

        print(
            "Found {0} Google Photos match groups against the rest of the library in {1}".format(
                len(comparisons),
                report_path,
            )
        )
        for item in comparisons[: args.limit]:
            print(
                "{date} | {name} | google={google_count} rest={rest_count} "
                "google_sample={google_sample} rest_sample={rest_sample}".format(**item)
            )
        return 0

    if args.command == "final-review-package":
        report_path = Path(args.report).expanduser()
        report_data = json.loads(report_path.read_text(encoding="utf-8"))
        output_dir = Path(args.output_dir).expanduser()
        write_final_review_package(report_data, report_path, output_dir)
        print("Wrote final review package to {0}".format(output_dir))
        return 0

    if args.command == "apply":
        report_path = Path(args.report).expanduser()
        report_data = json.loads(report_path.read_text(encoding="utf-8"))
        dest_root = Path(args.dest_root).expanduser()
        payload = build_apply_payload(
            report_data=report_data,
            report_path=report_path,
            dest_root=dest_root,
            include_mtime=args.include_mtime,
            include_duplicates=args.include_duplicates,
            include_received=args.include_received,
            include_google_takeout=args.include_google_takeout,
            include_unmatched_sidecars=args.include_unmatched_sidecars,
            include_unknown=args.include_unknown,
            include_caches=args.include_caches,
            include_pleasantharmony=args.include_pleasantharmony,
        )
        if args.manifest:
            write_json_output(Path(args.manifest).expanduser(), payload)

        operations = payload["operations"]
        skipped = payload["skipped"]
        mode_label = "execute" if args.execute else "dry-run"
        print(
            "Built {0} apply operations and skipped {1} files from {2} ({3})".format(
                len(operations),
                len(skipped),
                report_path,
                mode_label,
            )
        )

        if not args.execute:
            for item in operations[:25]:
                print("{0} -> {1}".format(item["source"], item["destination"]))
            return 0

        results = execute_apply_operations(operations)
        success_count = sum(1 for item in results if item["status"] in {"moved", "already-present"})
        print(
            "Applied {0} operations successfully; {1} conflicts/errors".format(
                success_count,
                len(results) - success_count,
            )
        )
        for item in results:
            if item["status"] not in {"moved", "already-present"}:
                print("{0} | {1} | {2}".format(item["status"], item["source"], item["message"]))
        if args.log:
            write_json_output(
                Path(args.log).expanduser(),
                {
                    "report": str(report_path),
                    "dest_root": str(dest_root),
                    "results": results,
                },
            )
        return 0 if all(item["status"] in {"moved", "already-present"} for item in results) else 1

    parser.error("Unknown command")
    return 2


def resolve_preview_root(path: Path, roots: Roots) -> Tuple[str, Path]:
    resolved_path = path.resolve()
    resolved_pictures = roots.pictures.resolve()
    resolved_videos = roots.videos.resolve()

    if is_within_root(resolved_path, resolved_pictures):
        return "pictures", roots.pictures
    if is_within_root(resolved_path, resolved_videos):
        return "videos", roots.videos

    raise ValueError(
        "Preview path must be inside one of the configured roots: {0}".format(path)
    )


def is_within_root(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def collect_suspicious_report_entries(report_data: Dict[str, object]) -> List[Dict[str, object]]:
    suspicious_entries: List[Dict[str, object]] = []
    for file_record in report_data.get("files", []):
        destination = file_record.get("proposed_relative_destination") or ""
        if not destination.startswith("Library/"):
            continue

        reasons = classify_suspicious_destination(file_record)
        if not reasons:
            continue

        suspicious_entries.append(
            {
                "path": file_record["path"],
                "destination": destination,
                "inferred_date": file_record.get("inferred_date"),
                "date_source": file_record.get("date_source"),
                "reasons": reasons,
            }
        )
    return suspicious_entries


def classify_suspicious_destination(file_record: Dict[str, object]) -> List[str]:
    destination = file_record.get("proposed_relative_destination") or ""
    bucket_name = Path(destination).parent.name
    label = bucket_name.split("_", 1)[1] if "_" in bucket_name else ""
    reasons: List[str] = []
    generic_label = label.lower() in {"pictures", "videos", "dcim", "camera", "photos"}

    if label.isdigit():
        reasons.append("numeric-label")
    if file_record.get("date_source") == "mtime":
        reasons.append("mtime-date")
    if generic_label and reasons:
        reasons.append("generic-label")

    return reasons


def collect_mtime_summary_groups(report_data: Dict[str, object]) -> List[Dict[str, object]]:
    grouped: Dict[Tuple[str, str], Dict[str, object]] = {}
    for file_record in report_data.get("files", []):
        if file_record.get("date_source") != "mtime":
            continue
        if file_record.get("category") not in {"image", "video", "project_video", "screen_recording"}:
            continue
        destination = str(file_record.get("proposed_relative_destination") or "")
        if destination.startswith("Shared/nanayCora80th/"):
            continue
        if destination.startswith("Shared/CEU/Undated/"):
            continue
        if destination.startswith("Projects/"):
            continue
        if destination.startswith("Reference/"):
            continue

        path = Path(file_record["path"])
        folder = str(path.parent)
        pattern = normalize_filename_pattern(path.name)
        key = (folder, pattern)

        item = grouped.setdefault(
            key,
            {
                "folder": folder,
                "pattern": pattern,
                "count": 0,
                "sample": path.name,
            },
        )
        item["count"] += 1

    return sorted(
        grouped.values(),
        key=lambda item: (-int(item["count"]), str(item["folder"]).lower(), str(item["pattern"]).lower()),
    )


def normalize_filename_pattern(name: str) -> str:
    return re.sub(r"\d+", "<digits>", name)


def collect_google_photos_summary(report_data: Dict[str, object]) -> List[Dict[str, object]]:
    roots = report_data.get("roots", {})
    pictures_root = roots.get("pictures")
    if not pictures_root:
        return []

    google_photos_root = Path(pictures_root) / "google-takeout" / "Takeout" / "Google Photos"
    grouped: Dict[str, Dict[str, object]] = {}

    for file_record in report_data.get("files", []):
        record_path = Path(file_record["path"])
        try:
            relative = record_path.relative_to(google_photos_root)
        except ValueError:
            continue

        top_folder = relative.parts[0] if relative.parts else "."
        item = grouped.setdefault(
            top_folder,
            {
                "folder": top_folder,
                "media": 0,
                "sidecars": 0,
                "edited": 0,
                "received": 0,
                "mtime": 0,
                "metadata": 0,
                "path": 0,
                "filename": 0,
                "sample": record_path.name,
            },
        )

        category = file_record.get("category")
        date_source = file_record.get("date_source")
        lowered_name = record_path.name.lower()
        if category in {"image", "video", "project_video", "screen_recording"}:
            item["media"] += 1
            if date_source in {"mtime", "metadata", "path", "filename"}:
                item[date_source] += 1
        if category == "sidecar":
            item["sidecars"] += 1
        if "-edited" in lowered_name or "edited." in lowered_name:
            item["edited"] += 1
        if lowered_name.startswith("received_"):
            item["received"] += 1

    return sorted(
        grouped.values(),
        key=lambda item: (
            -int(item["media"]),
            -int(item["sidecars"]),
            str(item["folder"]).lower(),
        ),
    )


def inspect_google_photos_folder(report_data: Dict[str, object], folder_name: str) -> Optional[Dict[str, object]]:
    roots = report_data.get("roots", {})
    pictures_root = roots.get("pictures")
    if not pictures_root:
        return None

    google_photos_root = Path(pictures_root) / "google-takeout" / "Takeout" / "Google Photos"
    grouped_items: Dict[str, Dict[str, object]] = {}
    found_folder = False

    summary = {
        "folder": folder_name,
        "media": 0,
        "sidecars": 0,
        "edited": 0,
        "received": 0,
        "unmatched_sidecars": 0,
        "groups": [],
    }

    for file_record in report_data.get("files", []):
        record_path = Path(file_record["path"])
        try:
            relative = record_path.relative_to(google_photos_root)
        except ValueError:
            continue

        if not relative.parts or relative.parts[0] != folder_name:
            continue

        found_folder = True
        category = file_record.get("category")
        name = record_path.name
        lowered_name = name.lower()
        key = normalize_google_photos_group_name(name)
        item = grouped_items.setdefault(
            key,
            {
                "name": key,
                "count": 0,
                "sidecars": 0,
                "edited_count": 0,
                "received_count": 0,
                "sample": name,
            },
        )

        if category in {"image", "video", "project_video", "screen_recording"}:
            summary["media"] += 1
            item["count"] += 1
        elif category == "sidecar":
            summary["sidecars"] += 1
            item["sidecars"] += 1

        if is_google_photos_edited_name(lowered_name):
            summary["edited"] += 1
            item["edited_count"] += 1
        if lowered_name.startswith("received_"):
            summary["received"] += 1
            item["received_count"] += 1

    if not found_folder:
        return None

    groups: List[Dict[str, object]] = []
    for item in grouped_items.values():
        if item["sidecars"] and not item["count"]:
            summary["unmatched_sidecars"] += item["sidecars"]

        kind = "mixed"
        if item["edited_count"] and item["count"] >= 2:
            kind = "edited-pair"
        elif item["received_count"]:
            kind = "received"
        elif item["sidecars"] and item["count"]:
            kind = "media+sidecar"
        elif item["sidecars"] and not item["count"]:
            kind = "sidecar-only"

        groups.append(
            {
                "kind": kind,
                "count": item["count"],
                "sidecars": item["sidecars"],
                "name": item["name"],
                "sample": item["sample"],
            }
        )

    summary["groups"] = sorted(
        groups,
        key=lambda item: (-int(item["count"]), -int(item["sidecars"]), str(item["name"]).lower()),
    )
    return summary


def normalize_google_photos_group_name(name: str) -> str:
    lowered = name.lower()
    if is_google_photos_sidecar_name(lowered):
        base = strip_google_photos_sidecar_suffix(name)
    else:
        base = name

    base = re.sub(r"-edited(?=\.[^.]+$)", "", base, flags=re.IGNORECASE)
    return base


def is_google_photos_sidecar_name(lowered_name: str) -> bool:
    return ".supplemental" in lowered_name and lowered_name.endswith(".json")


def strip_google_photos_sidecar_suffix(name: str) -> str:
    lowered = name.lower()
    marker_index = lowered.find(".supplemental")
    if marker_index != -1:
        return name[:marker_index]
    return name


def is_google_photos_edited_name(lowered_name: str) -> bool:
    return "-edited" in lowered_name or "edited." in lowered_name


def write_json_output(output_path: Path, payload: Dict[str, object]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=False)
        handle.write("\n")


def write_text_output(output_path: Path, text: str) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(text, encoding="utf-8")


def build_apply_payload(
    report_data: Dict[str, object],
    report_path: Path,
    dest_root: Path,
    include_mtime: bool = False,
    include_duplicates: bool = False,
    include_received: bool = False,
    include_google_takeout: bool = False,
    include_unmatched_sidecars: bool = False,
    include_unknown: bool = False,
    include_caches: bool = False,
    include_pleasantharmony: bool = False,
) -> Dict[str, object]:
    files = [item for item in report_data.get("files", []) if isinstance(item, dict)]
    selected_sources: Set[str] = set()
    skipped: List[Dict[str, object]] = []

    for file_record in files:
        skip_reason = classify_apply_skip_reason(
            file_record=file_record,
            report_data=report_data,
            include_mtime=include_mtime,
            include_duplicates=include_duplicates,
            include_received=include_received,
            include_google_takeout=include_google_takeout,
            include_unmatched_sidecars=include_unmatched_sidecars,
            include_unknown=include_unknown,
            include_caches=include_caches,
            include_pleasantharmony=include_pleasantharmony,
        )
        if skip_reason is not None:
            skipped.append(
                {
                    "path": file_record.get("path"),
                    "reason": skip_reason,
                }
            )
            continue
        selected_sources.add(str(file_record["path"]))

    operations: List[Dict[str, object]] = []
    deferred_sidecars: List[Dict[str, object]] = []
    for file_record in files:
        source = str(file_record.get("path") or "")
        if source not in selected_sources:
            continue

        destination_relative = str(file_record.get("proposed_relative_destination") or "")
        if not destination_relative:
            continue

        if file_record.get("category") == "sidecar":
            sidecar_for = file_record.get("sidecar_for")
            if sidecar_for and str(sidecar_for) not in selected_sources and not include_unmatched_sidecars:
                deferred_sidecars.append(
                    {
                        "path": source,
                        "reason": "sidecar-target-not-selected",
                    }
                )
                continue

        operations.append(
            {
                "source": source,
                "destination": str(dest_root / destination_relative),
                "destination_relative": destination_relative,
                "category": file_record.get("category"),
                "size_bytes": file_record.get("size_bytes"),
                "modified_at": file_record.get("modified_at"),
                "sha256": file_record.get("sha256"),
                "duplicate_group": file_record.get("duplicate_group"),
                "date_source": file_record.get("date_source"),
                "sidecar_for": file_record.get("sidecar_for"),
            }
        )

    skipped.extend(deferred_sidecars)
    operations.sort(
        key=lambda item: (
            1 if item.get("category") == "sidecar" else 0,
            str(item["destination"]).lower(),
            str(item["source"]).lower(),
        )
    )

    return {
        "report": str(report_path),
        "dest_root": str(dest_root),
        "operation_count": len(operations),
        "skip_count": len(skipped),
        "operations": operations,
        "skipped": sorted(skipped, key=lambda item: (str(item["reason"]), str(item["path"]))),
    }


def classify_apply_skip_reason(
    file_record: Dict[str, object],
    report_data: Dict[str, object],
    include_mtime: bool,
    include_duplicates: bool,
    include_received: bool,
    include_google_takeout: bool,
    include_unmatched_sidecars: bool,
    include_unknown: bool,
    include_caches: bool,
    include_pleasantharmony: bool,
) -> Optional[str]:
    destination = str(file_record.get("proposed_relative_destination") or "")
    if not destination:
        return "no-destination"

    category = str(file_record.get("category") or "")
    if category == "cache" and not include_caches:
        return "cache"
    if category == "unknown" and not include_unknown:
        return "unknown-category"

    if file_record.get("date_source") == "mtime" and not include_mtime:
        return "mtime-date"

    if file_record.get("duplicate_group") and not include_duplicates:
        return "duplicate-group"

    if is_pleasantharmony_record(file_record) and not include_pleasantharmony:
        return "pleasantharmony"

    if is_google_takeout_record(file_record, report_data) and not include_google_takeout:
        return "google-takeout"

    if is_google_photos_received_record(file_record, report_data) and not include_received:
        return "google-photos-received"

    if category == "sidecar":
        if not file_record.get("sidecar_for") and not include_unmatched_sidecars:
            return "unmatched-sidecar"
        if (
            is_google_photos_sidecar_gap_record(file_record, report_data)
            and not include_unmatched_sidecars
        ):
            return "google-photos-sidecar-gap"

    return None


def is_google_photos_received_record(file_record: Dict[str, object], report_data: Dict[str, object]) -> bool:
    google_photos_root = get_google_photos_root(report_data)
    if google_photos_root is None:
        return False

    record_path = Path(str(file_record.get("path") or ""))
    try:
        record_path.relative_to(google_photos_root)
    except ValueError:
        return False
    return record_path.name.lower().startswith("received_")


def is_google_takeout_record(file_record: Dict[str, object], report_data: Dict[str, object]) -> bool:
    google_photos_root = get_google_photos_root(report_data)
    if google_photos_root is None:
        return False

    record_path = Path(str(file_record.get("path") or ""))
    try:
        record_path.relative_to(google_photos_root)
        return True
    except ValueError:
        return False


def is_pleasantharmony_record(file_record: Dict[str, object]) -> bool:
    destination = str(file_record.get("proposed_relative_destination") or "")
    return destination.startswith("Projects/PleasantHarmony/")


def is_google_photos_sidecar_gap_record(file_record: Dict[str, object], report_data: Dict[str, object]) -> bool:
    if file_record.get("category") != "sidecar":
        return False

    google_photos_root = get_google_photos_root(report_data)
    if google_photos_root is None:
        return False

    record_path = Path(str(file_record.get("path") or ""))
    try:
        relative = record_path.relative_to(google_photos_root)
    except ValueError:
        return False

    if file_record.get("sidecar_for"):
        return False

    folder = relative.parts[0] if relative.parts else "."
    expected_name = normalize_google_photos_group_name(record_path.name)
    for candidate in report_data.get("files", []):
        if not isinstance(candidate, dict):
            continue
        if candidate.get("category") not in {"image", "video", "project_video", "screen_recording"}:
            continue
        candidate_path = Path(str(candidate.get("path") or ""))
        try:
            candidate_relative = candidate_path.relative_to(google_photos_root)
        except ValueError:
            continue
        candidate_folder = candidate_relative.parts[0] if candidate_relative.parts else "."
        if candidate_folder != folder:
            continue
        if normalize_google_photos_group_name(candidate_path.name) == expected_name:
            return False
    return True


def execute_apply_operations(operations: List[Dict[str, object]]) -> List[Dict[str, object]]:
    results: List[Dict[str, object]] = []
    for operation in operations:
        source = Path(str(operation["source"]))
        destination = Path(str(operation["destination"]))
        try:
            verify_source_matches_report(source, operation)
            destination.parent.mkdir(parents=True, exist_ok=True)
            if destination.exists():
                if files_match_for_apply(source, destination, operation):
                    if source.resolve() != destination.resolve():
                        source.unlink()
                    results.append(
                        {
                            "source": str(source),
                            "destination": str(destination),
                            "status": "already-present",
                            "message": "destination already contained matching content",
                        }
                    )
                    continue
                results.append(
                    {
                        "source": str(source),
                        "destination": str(destination),
                        "status": "conflict",
                        "message": "destination exists with different content",
                    }
                )
                continue

            move_file_verified(source, destination)
            results.append(
                {
                    "source": str(source),
                    "destination": str(destination),
                    "status": "moved",
                    "message": "moved successfully",
                }
            )
        except Exception as exc:
            results.append(
                {
                    "source": str(source),
                    "destination": str(destination),
                    "status": "error",
                    "message": str(exc),
                }
            )
    return results


def verify_source_matches_report(source: Path, operation: Dict[str, object]) -> None:
    if not source.exists():
        raise FileNotFoundError("source file no longer exists")

    stat = source.stat()
    expected_size = operation.get("size_bytes")
    if expected_size is None or int(expected_size) != stat.st_size:
        raise ValueError("source size no longer matches the saved report")

    if str(operation.get("modified_at") or "") != datetime.fromtimestamp(stat.st_mtime).isoformat():
        raise ValueError("source modified time no longer matches the saved report")


def files_match_for_apply(source: Path, destination: Path, operation: Dict[str, object]) -> bool:
    if source.stat().st_size != destination.stat().st_size:
        return False

    expected_hash = str(operation.get("sha256") or "")
    if expected_hash:
        return hash_path(destination) == expected_hash

    return hash_path(source) == hash_path(destination)


def hash_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def move_file_verified(source: Path, destination: Path) -> None:
    source_stat = source.stat()
    if same_filesystem(source, destination.parent):
        os.replace(source, destination)
        return

    shutil.copy2(source, destination)
    if source_stat.st_size != destination.stat().st_size:
        raise ValueError("copied destination size does not match source")
    if hash_path(source) != hash_path(destination):
        raise ValueError("copied destination hash does not match source")
    source.unlink()


def same_filesystem(source: Path, destination_parent: Path) -> bool:
    try:
        return source.stat().st_dev == destination_parent.stat().st_dev
    except FileNotFoundError:
        return False


def get_google_photos_root(report_data: Dict[str, object]) -> Optional[Path]:
    roots = report_data.get("roots", {})
    pictures_root = roots.get("pictures")
    if not pictures_root:
        return None
    return Path(pictures_root) / "google-takeout" / "Takeout" / "Google Photos"


def collect_google_photos_received(report_data: Dict[str, object]) -> List[Dict[str, object]]:
    google_photos_root = get_google_photos_root(report_data)
    if google_photos_root is None:
        return []

    grouped: Dict[str, Dict[str, object]] = {}
    for file_record in report_data.get("files", []):
        record_path = Path(file_record["path"])
        lowered_name = record_path.name.lower()
        if not lowered_name.startswith("received_"):
            continue
        try:
            relative = record_path.relative_to(google_photos_root)
        except ValueError:
            continue

        folder = relative.parts[0] if relative.parts else "."
        item = grouped.setdefault(
            folder,
            {
                "folder": folder,
                "media": 0,
                "sidecars": 0,
                "date_sources": set(),
                "sample": record_path.name,
            },
        )
        if file_record.get("category") == "sidecar":
            item["sidecars"] += 1
        else:
            item["media"] += 1
        if file_record.get("date_source"):
            item["date_sources"].add(str(file_record["date_source"]))

    results: List[Dict[str, object]] = []
    for item in grouped.values():
        results.append(
            {
                "folder": item["folder"],
                "media": item["media"],
                "sidecars": item["sidecars"],
                "date_sources": ",".join(sorted(item["date_sources"])) or "unknown",
                "sample": item["sample"],
            }
        )

    return sorted(results, key=lambda item: (-int(item["media"]), -int(item["sidecars"]), str(item["folder"]).lower()))


def collect_google_photos_sidecar_gaps(report_data: Dict[str, object]) -> List[Dict[str, object]]:
    google_photos_root = get_google_photos_root(report_data)
    if google_photos_root is None:
        return []

    grouped: Dict[Tuple[str, str], Dict[str, object]] = {}
    for file_record in report_data.get("files", []):
        record_path = Path(file_record["path"])
        try:
            relative = record_path.relative_to(google_photos_root)
        except ValueError:
            continue

        folder = relative.parts[0] if relative.parts else "."
        key_name = normalize_google_photos_group_name(record_path.name)
        key = (folder, key_name)
        item = grouped.setdefault(
            key,
            {
                "folder": folder,
                "name": key_name,
                "count": 0,
                "sidecars": 0,
                "sample": record_path.name,
            },
        )
        if file_record.get("category") == "sidecar":
            item["sidecars"] += 1
        elif file_record.get("category") in {"image", "video", "project_video", "screen_recording"}:
            item["count"] += 1

    gaps = [
        {
            "folder": item["folder"],
            "name": item["name"],
            "sidecars": item["sidecars"],
            "sample": item["sample"],
        }
        for item in grouped.values()
        if item["sidecars"] and not item["count"]
    ]
    return sorted(gaps, key=lambda item: (-int(item["sidecars"]), str(item["folder"]).lower(), str(item["name"]).lower()))


def collect_google_photos_matches(
    report_data: Dict[str, object],
    dates: Optional[List[str]] = None,
    rest_folder_contains: Optional[str] = None,
) -> List[Dict[str, object]]:
    google_photos_root = get_google_photos_root(report_data)
    if google_photos_root is None:
        return []

    google_groups: Dict[Tuple[str, str], Dict[str, object]] = {}
    rest_groups: Dict[Tuple[str, str], Dict[str, object]] = {}

    for file_record in report_data.get("files", []):
        if file_record.get("category") not in {"image", "video", "project_video", "screen_recording"}:
            continue

        record_path = Path(file_record["path"])
        normalized_name = normalize_google_photos_group_name(record_path.name)
        inferred_date = str(file_record.get("inferred_date") or "unknown")
        key = (inferred_date, normalized_name.lower())

        try:
            record_path.relative_to(google_photos_root)
            target = google_groups
        except ValueError:
            target = rest_groups

        item = target.setdefault(
            key,
            {
                "date": inferred_date,
                "name": normalized_name,
                "count": 0,
                "sample": str(record_path),
            },
        )
        item["count"] += 1

    results: List[Dict[str, object]] = []
    for key, google_item in google_groups.items():
        rest_item = rest_groups.get(key)
        if not rest_item:
            continue
        result = {
            "date": google_item["date"],
            "name": google_item["name"],
            "google_count": google_item["count"],
            "rest_count": rest_item["count"],
            "google_sample": google_item["sample"],
            "rest_sample": rest_item["sample"],
        }

        if dates and result["date"] not in set(dates):
            continue
        if rest_folder_contains and rest_folder_contains.lower() not in result["rest_sample"].lower():
            continue

        results.append(
            {
                "date": result["date"],
                "name": result["name"],
                "google_count": result["google_count"],
                "rest_count": result["rest_count"],
                "google_sample": result["google_sample"],
                "rest_sample": result["rest_sample"],
            }
        )

    return sorted(
        results,
        key=lambda item: (
            -(int(item["google_count"]) + int(item["rest_count"])),
            str(item["date"]).lower(),
            str(item["name"]).lower(),
        ),
    )


def write_final_review_package(report_data: Dict[str, object], report_path: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    mtime_groups = collect_mtime_summary_groups(report_data)
    suspicious_entries = collect_suspicious_report_entries(report_data)
    google_summary = collect_google_photos_summary(report_data)
    received_groups = collect_google_photos_received(report_data)
    sidecar_gaps = collect_google_photos_sidecar_gaps(report_data)
    google_matches = collect_google_photos_matches(report_data)
    focused_matches = collect_google_photos_matches(
        report_data,
        dates=["2014-05-28", "2014-06-21", "2014-07-19"],
        rest_folder_contains="/home/gabriel/Pictures/20140723 and earlier",
    )

    write_json_output(output_dir / "mtime-summary.json", {"groups": mtime_groups})
    write_json_output(output_dir / "suspicious-destinations.json", {"entries": suspicious_entries})
    write_json_output(output_dir / "google-photos-summary.json", {"folders": google_summary})
    write_json_output(output_dir / "google-photos-received.json", {"folders": received_groups})
    write_json_output(output_dir / "google-photos-sidecar-gaps.json", {"groups": sidecar_gaps})
    write_json_output(output_dir / "google-photos-matches.json", {"matches": google_matches})
    write_json_output(
        output_dir / "google-photos-2014-review.json",
        {
            "dates": ["2014-05-28", "2014-06-21", "2014-07-19"],
            "rest_folder_contains": "/home/gabriel/Pictures/20140723 and earlier",
            "matches": focused_matches,
        },
    )

    summary_text = build_final_review_summary(
        report_data=report_data,
        report_path=report_path,
        mtime_groups=mtime_groups,
        suspicious_entries=suspicious_entries,
        google_summary=google_summary,
        received_groups=received_groups,
        sidecar_gaps=sidecar_gaps,
        focused_matches=focused_matches,
    )
    write_text_output(output_dir / "README.md", summary_text)


def build_final_review_summary(
    report_data: Dict[str, object],
    report_path: Path,
    mtime_groups: List[Dict[str, object]],
    suspicious_entries: List[Dict[str, object]],
    google_summary: List[Dict[str, object]],
    received_groups: List[Dict[str, object]],
    sidecar_gaps: List[Dict[str, object]],
    focused_matches: List[Dict[str, object]],
) -> str:
    summary = report_data.get("summary", {})
    destination_roots = collect_destination_root_counts(report_data)

    lines = [
        "# Final Review Package",
        "",
        "Source report: `{0}`".format(report_path),
        "",
        "## Scan Summary",
        "",
        "- total files: {0}".format(summary.get("total_files", 0)),
        "- images: {0}".format(summary.get("images", 0)),
        "- videos: {0}".format(summary.get("videos", 0)),
        "- sidecars: {0}".format(summary.get("sidecars", 0)),
        "- caches: {0}".format(summary.get("caches", 0)),
        "- unknown: {0}".format(summary.get("unknown", 0)),
        "",
        "## Planned Structure",
        "",
        "- destination roots: {0}".format(
            ", ".join("{0}={1}".format(key, value) for key, value in destination_roots.items())
        ),
        "- main library shape: `Library/YYYY/YYYY-MM-DD_source/...`",
        "- shared branches in use: `Shared/Jonel/...`, `Shared/Samyra/...`",
        "- sidecars route to: `Exports/...`",
        "- caches route to: `App-Caches/...`",
        "",
        "## Priority Review Areas",
        "",
        "- remaining suspicious planned destinations: {0}".format(len(suspicious_entries)),
        "- remaining grouped mtime patterns: {0}".format(len(mtime_groups)),
        "- Google Photos folders: {0}".format(len(google_summary)),
        "- Google Photos received_* folders: {0}".format(len(received_groups)),
        "- Google Photos sidecar-only groups: {0}".format(len(sidecar_gaps)),
        "- focused 2014 Google Photos review matches: {0}".format(len(focused_matches)),
        "",
        "## Top Remaining mtime Groups",
        "",
    ]

    for item in mtime_groups[:10]:
        lines.append(
            "- {0} files | {1} | {2}".format(item["count"], item["folder"], item["pattern"])
        )

    lines.extend(
        [
            "",
            "## Top Google Photos Folders",
            "",
        ]
    )
    for item in google_summary[:10]:
        lines.append(
            "- {0} | media={1} sidecars={2} edited={3} received={4}".format(
                item["folder"],
                item["media"],
                item["sidecars"],
                item["edited"],
                item["received"],
            )
        )

    lines.extend(
        [
            "",
            "## Focused 2014 Review",
            "",
            "- filtered dates: `2014-05-28`, `2014-06-21`, `2014-07-19`",
            "- non-Takeout folder filter: `/home/gabriel/Pictures/20140723 and earlier`",
        ]
    )
    for item in focused_matches[:10]:
        lines.append(
            "- {0} | {1} | google={2} rest={3}".format(
                item["date"],
                item["name"],
                item["google_count"],
                item["rest_count"],
            )
        )

    lines.extend(
        [
            "",
            "## Package Files",
            "",
            "- `README.md`",
            "- `mtime-summary.json`",
            "- `suspicious-destinations.json`",
            "- `google-photos-summary.json`",
            "- `google-photos-received.json`",
            "- `google-photos-sidecar-gaps.json`",
            "- `google-photos-matches.json`",
            "- `google-photos-2014-review.json`",
            "",
        ]
    )
    return "\n".join(lines) + "\n"


def collect_destination_root_counts(report_data: Dict[str, object]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for file_record in report_data.get("files", []):
        destination = file_record.get("proposed_relative_destination")
        if not destination:
            continue
        root = Path(str(destination)).parts[0]
        counts[root] = counts.get(root, 0) + 1
    return dict(sorted(counts.items(), key=lambda item: (-item[1], item[0])))
