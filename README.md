# Media Organizer

Safety-first tooling for scanning and planning reorganization of personal media
libraries. The current implementation is intentionally conservative:

- scans directories without modifying source files
- classifies images, videos, JSON sidecars, cache folders, and unknown files
- computes SHA-256 hashes for media files to detect duplicates
- derives date buckets from filenames first, then file modification time
- writes dry-run reports and move plans for review

## Current scope

This scaffold is designed for a mixed library like:

- `~/Pictures`
- `~/Videos`
- Google Takeout exports kept as import sources
- cache folders like `.wdmc` that should stay outside the permanent library

The tool does **not** delete or move files yet.

It now includes a conservative report-driven `apply` command that can build a
move manifest and execute it, but it defaults to dry-run mode and excludes
high-risk cases such as `mtime`-dated files, duplicate-group members,
all Google Takeout media and sidecars, Google Photos `received_*` items,
unmatched sidecars, cache files, `Projects/PleasantHarmony/...`, and unknown
files unless you opt in explicitly.

## Quick start

```bash
python3 -m media_organizer scan \
  --pictures-root ~/Pictures \
  --videos-root ~/Videos \
  --report reports/scan.json
```

That command scans both roots, hashes media files, and writes a JSON report with:

- per-file classification
- duplicate groups
- proposed destination paths
- summary counts

## Planned destination model

- Pictures
  - `Library/YYYY/YYYY-MM-DD_source/`
  - `Reference/`
  - `Exports/`
  - `App-Caches/`
- Videos
  - `Library/YYYY/YYYY-MM-DD_source/`
  - `Projects/`
  - `ScreenRecordings/`
  - `Exports/`

The current planner only generates proposed destinations. Review those plans
before adding a future move/apply phase.

## Conservative apply workflow

Build a dry-run manifest first:

```bash
python3 -m media_organizer apply \
  --report reports/scan-hash-v68.json \
  --dest-root /path/to/organized-library \
  --manifest reports/apply-manifest-v1.json
```

If the manifest looks correct, execute the same plan and capture a log:

```bash
python3 -m media_organizer apply \
  --report reports/scan-hash-v68.json \
  --dest-root /path/to/organized-library \
  --manifest reports/apply-manifest-v1.json \
  --log reports/apply-log-v1.json \
  --execute
```

The apply phase verifies source size and `modified_at` against the saved report
before moving anything, and it refuses to overwrite conflicting destination
content.

Some clearly non-chronological picture folders may route directly to
`Reference/` instead of the dated `Library/` tree when the folder intent is
explicit, for example screenshots, wallpapers, stock/reference images, or
similar utility folders. Legacy scan buckets can also route there when the
folder clearly behaves like a manual scan/archive holding area rather than a
dated camera roll. A small number of individually reviewed loose files can also
be routed directly into `Reference/Legacy-Scans/` when their current root-level
location is too weak to infer a meaningful dated library destination.

Some named shared collections may also use explicit undated branches when the
source identity is trustworthy but the inferred day is not. In those cases the
planner can route items under `Shared/<Collection>/Undated/` rather than
pretending a file modification date is the real event date.

## Notes

- Date extraction is conservative and may fall back to file modification time
  when embedded metadata is unavailable.
- Google Takeout JSON files are tracked as sidecars and linked by filename stem
  where possible.
- Cache folders such as `.wdmc` are classified separately so they do not pollute
  the permanent library plan.
- Review helpers:
  - `preview` inspects proposed destinations for specific files
  - `suspicious-report` prints suspicious destination rows from a saved report
  - `mtime-summary` groups remaining `mtime`-dated media by folder and filename
    pattern so ambiguous batches are easier to review
