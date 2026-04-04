import argparse
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple

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
