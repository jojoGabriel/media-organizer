#!/usr/bin/env python3
"""Move Google Takeout media into organized library only when content is unique.

This script reads an existing scan JSON report, selects Takeout media records
(image/video), and compares each source file against files already present under
an organized library root. Files that do not have a content match are moved to
their planned destination.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class MoveResult:
    source: str
    destination: str
    reason: str


@dataclass
class SkipResult:
    source: str
    reason: str
    matched_existing: Optional[str] = None
    destination: Optional[str] = None


@dataclass
class ErrorResult:
    source: str
    destination: str
    error: str


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_report(path: Path) -> Dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def build_size_index(root: Path) -> Dict[int, List[Path]]:
    by_size: Dict[int, List[Path]] = defaultdict(list)
    for dirpath, _, filenames in os.walk(root):
        for filename in filenames:
            candidate = Path(dirpath) / filename
            try:
                by_size[candidate.stat().st_size].append(candidate)
            except OSError:
                continue
    return by_size


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Move Google Takeout media into organized library only when content "
            "does not already exist there."
        )
    )
    parser.add_argument("--scan-report", required=True, help="Path to scan JSON report.")
    parser.add_argument(
        "--organized-root",
        default="/home/gabriel/organized-media-dry-run",
        help="Organized library root. Default: /home/gabriel/organized-media-dry-run",
    )
    parser.add_argument(
        "--takeout-prefix",
        default="/home/gabriel/Pictures/google-takeout/Takeout/Google Photos/",
        help="Absolute source prefix for Google Takeout media paths.",
    )
    parser.add_argument(
        "--output-prefix",
        required=True,
        help=(
            "Output report prefix path without extension. "
            "Example: reports/takeout-unique-to-library-move-v2"
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    scan_report = Path(args.scan_report).expanduser().resolve()
    organized_root = Path(args.organized_root).expanduser().resolve()
    takeout_prefix = str(Path(args.takeout_prefix).expanduser())

    output_prefix = Path(args.output_prefix).expanduser()
    output_json = output_prefix.with_suffix(".json")
    output_txt = output_prefix.with_suffix(".txt")

    report = load_report(scan_report)
    files = report.get("files", [])

    candidates = [
        row
        for row in files
        if row.get("category") in ("image", "video")
        and str(row.get("path", "")).startswith(takeout_prefix)
        and row.get("proposed_relative_destination")
    ]

    by_size = build_size_index(organized_root)

    hash_cache: Dict[str, str] = {}

    def digest(path: Path) -> str:
        key = str(path)
        cached = hash_cache.get(key)
        if cached is not None:
            return cached
        value = sha256(path)
        hash_cache[key] = value
        return value

    moved: List[MoveResult] = []
    skipped_existing: List[SkipResult] = []
    skipped_missing: List[SkipResult] = []
    skipped_dest_same: List[SkipResult] = []
    conflicts: List[MoveResult] = []
    errors: List[ErrorResult] = []

    for row in candidates:
        source = Path(str(row["path"]))
        destination = organized_root / str(row["proposed_relative_destination"])

        if not source.exists():
            skipped_missing.append(SkipResult(source=str(source), reason="missing_source"))
            continue

        match_path: Optional[Path] = None
        source_size = source.stat().st_size
        possible = by_size.get(source_size, [])
        if possible:
            source_digest = digest(source)
            for existing_path in possible:
                try:
                    if digest(existing_path) == source_digest:
                        match_path = existing_path
                        break
                except OSError:
                    continue

        if match_path is not None:
            skipped_existing.append(
                SkipResult(
                    source=str(source),
                    reason="content_match_exists",
                    matched_existing=str(match_path),
                )
            )
            continue

        try:
            destination.parent.mkdir(parents=True, exist_ok=True)

            if destination.exists():
                try:
                    if digest(source) == digest(destination):
                        skipped_dest_same.append(
                            SkipResult(
                                source=str(source),
                                destination=str(destination),
                                reason="destination_same_content",
                            )
                        )
                        continue
                except OSError:
                    pass

                relative_takeout = source.relative_to(Path(takeout_prefix))
                reroute = organized_root / "Archive" / "Takeout-Unique-Conflicts" / relative_takeout
                reroute.parent.mkdir(parents=True, exist_ok=True)
                if reroute.exists():
                    stem = reroute.stem
                    suffix = reroute.suffix
                    index = 1
                    while True:
                        candidate = reroute.with_name(f"{stem}_SRC-CONFLICT-{index}{suffix}")
                        if not candidate.exists():
                            reroute = candidate
                            break
                        index += 1

                shutil.move(str(source), str(reroute))
                moved.append(MoveResult(source=str(source), destination=str(reroute), reason="dest_conflict_rerouted"))
                conflicts.append(MoveResult(source=str(source), destination=str(reroute), reason="dest_conflict_rerouted"))
            else:
                shutil.move(str(source), str(destination))
                moved.append(MoveResult(source=str(source), destination=str(destination), reason="unique_vs_organized"))

        except Exception as exc:  # pylint: disable=broad-except
            errors.append(ErrorResult(source=str(source), destination=str(destination), error=str(exc)))

    output = {
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "source_report": str(scan_report),
        "organized_root": str(organized_root),
        "takeout_prefix": takeout_prefix,
        "candidate_count": len(candidates),
        "moved_count": len(moved),
        "skipped_existing_content_match_count": len(skipped_existing),
        "skipped_missing_source_count": len(skipped_missing),
        "skipped_destination_same_content_count": len(skipped_dest_same),
        "conflict_reroutes_count": len(conflicts),
        "error_count": len(errors),
        "moved": [entry.__dict__ for entry in moved],
        "skipped_existing_content_match": [entry.__dict__ for entry in skipped_existing],
        "skipped_missing_source": [entry.__dict__ for entry in skipped_missing],
        "skipped_destination_same_content": [entry.__dict__ for entry in skipped_dest_same],
        "conflicts": [entry.__dict__ for entry in conflicts],
        "errors": [entry.__dict__ for entry in errors],
    }

    output_json.parent.mkdir(parents=True, exist_ok=True)
    with output_json.open("w", encoding="utf-8") as handle:
        json.dump(output, handle, indent=2)
        handle.write("\n")

    with output_txt.open("w", encoding="utf-8") as handle:
        handle.write("takeout unique to library move\n")
        handle.write(f"source_report: {scan_report}\n")
        handle.write(f"organized_root: {organized_root}\n")
        handle.write(f"takeout_prefix: {takeout_prefix}\n")
        handle.write(f"candidate_count: {len(candidates)}\n")
        handle.write(f"moved: {len(moved)}\n")
        handle.write(f"skipped_existing_content_match: {len(skipped_existing)}\n")
        handle.write(f"skipped_missing_source: {len(skipped_missing)}\n")
        handle.write(f"skipped_destination_same_content: {len(skipped_dest_same)}\n")
        handle.write(f"conflict_reroutes: {len(conflicts)}\n")
        handle.write(f"errors: {len(errors)}\n")

    print(f"candidate_count={len(candidates)}")
    print(f"moved={len(moved)}")
    print(f"skipped_existing_content_match={len(skipped_existing)}")
    print(f"skipped_missing_source={len(skipped_missing)}")
    print(f"skipped_destination_same_content={len(skipped_dest_same)}")
    print(f"conflict_reroutes={len(conflicts)}")
    print(f"errors={len(errors)}")
    print(output_json)
    print(output_txt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
