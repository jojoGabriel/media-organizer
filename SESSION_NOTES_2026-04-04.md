# Session Notes - 2026-04-04

## Where the project stands

The media organizer is still a safety-first dry-run planner. It scans media,
classifies files, links Google Takeout sidecars, infers dates, and proposes
destinations. It still does not move, rename, or delete real files.

Main code paths:

- `media_organizer/cli.py`
- `media_organizer/scanner.py`
- `tests/test_scanner.py`

## What was accomplished

Major review tooling added:

- `preview`
- `suspicious-report`
- `mtime-summary`
- `google-photos-summary`
- `google-photos-folder`
- `google-photos-received`
- `google-photos-sidecar-gaps`
- `google-photos-compare`
- `final-review-package`

Major date inference improvements:

- path inference for `YYYY/MM/DD`
- path inference for compact `YYYYMM`
- path inference for compact `YYYYMMDD`
- path inference for date-prefixed folders like `2008-04-20--18.53.11`
- path inference for `Photos from YYYY`
- path inference for `YYYY/<month-name>`
- narrow path inference for `Pictures from ates camera/NNN_MMDD`
- filename inference for Unix timestamps like `FB_IMG_1620441643131.jpg`
- filename year-only fallback for numeric sequence files like `200600001.jpg`
- EXIF metadata date inference for images

Major destination planning changes:

- `Jonel` routes to `Shared/Jonel/...`
- `Pictures from ates camera/*` also routes to `Shared/Jonel/...`
- `Samyras 16` routes to `Shared/Samyra/...`
- `nanay80` now routes as a direct folder override to `Shared/nanayCora80th/...`

Google Photos review work:

- added high-level Takeout summary reporting
- added per-folder grouping for edited/original pairs and sidecars
- added `received_*` review
- added sidecar-only gap review
- added compare view between Google Photos and the rest of the library
- added filtered export support for focused duplicate-review batches

## Latest kept artifacts

Keep these:

- `reports/scan-nohash-v15.json`
- `reports/final-review-package-v2/`

Important focused artifact:

- `reports/final-review-package-v2/google-photos-2014-review.json`

## Current planned structure

Main buckets:

- `Library/YYYY/YYYY-MM-DD_source/...`
- `Shared/Jonel/YYYY/YYYY-MM-DD_Jonel/...`
- `Shared/Samyra/YYYY/YYYY-MM-DD_Samyra/...`
- `Shared/nanayCora80th/...`
- `Exports/...`
- `App-Caches/...`
- `Projects/...`
- `ScreenRecordings/...`

## Current review package summary

From `reports/final-review-package-v2/README.md`:

- total files: `49293`
- images: `15186`
- videos: `818`
- sidecars: `4273`
- caches: `27984`
- remaining suspicious planned destinations: `216`
- remaining grouped `mtime` patterns: `119`
- Google Photos folders: `37`
- Google Photos `received_*` folders: `6`
- Google Photos sidecar-only groups: `478`
- focused 2014 Google Photos review matches: `111`

## What still needs review

Main unresolved planning folders:

- `/home/gabriel/Pictures/summer2014`
- `/home/gabriel/Pictures/temp`
- `/home/gabriel/Pictures/ceu`
- `/home/gabriel/Pictures/google-takeout/Takeout/Google Photos/T3 (Total  Tabata Training) Series 1`
- `/home/gabriel/Videos`
- `/home/gabriel/Pictures/morePics`
- `/home/gabriel/Pictures/nasa`
- `/home/gabriel/Videos/PleasantHarmony`
- `/home/gabriel/Pictures/Photos`
- `/home/gabriel/Videos/Tutorial/installAnaconda`
- `/home/gabriel/Pictures/1903/12/31`
- `/home/gabriel/Videos/JJ1999`

Important note:

- `nanay80` now has a direct destination override to
  `Shared/nanayCora80th/...`
- the refreshed `v15` report and `v2` package already include that change

## Recommended next step

When work resumes:

1. regenerate the latest report after the `nanay80` override
2. review unresolved planning folders, starting with `summer2014`
3. continue Google Photos cleanup from the focused 2014 review batch

## Safety reminder

No apply phase exists yet. Everything remains dry-run planning and review only.
