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
  - `Exports/`
  - `App-Caches/`
- Videos
  - `Library/YYYY/YYYY-MM-DD_source/`
  - `Projects/`
  - `ScreenRecordings/`
  - `Exports/`

The current planner only generates proposed destinations. Review those plans
before adding a future move/apply phase.

## Notes

- Date extraction is conservative and may fall back to file modification time
  when embedded metadata is unavailable.
- Google Takeout JSON files are tracked as sidecars and linked by filename stem
  where possible.
- Cache folders such as `.wdmc` are classified separately so they do not pollute
  the permanent library plan.

