# Session Notes - 2026-04-05

## Where the project stands

The media organizer is still a safety-first dry-run planner. It scans media,
classifies files, links Google Takeout sidecars, infers dates, detects
duplicates when hashing is enabled, and proposes destinations. It still does
not move, rename, or delete real files.

Main code paths:

- `media_organizer/cli.py`
- `media_organizer/scanner.py`
- `tests/test_scanner.py`

## Code changes now in progress

Scanner behavior improved this session:

- added embedded video metadata date inference via `ffprobe`
- `summer2014` videos now resolve from metadata instead of `mtime`
- `Tito Osias` now routes to `Shared/Tito-Osias/...`
- `ceu` now routes to `Shared/CEU/...`
- `PleasantHarmony` project assets stay together under `Projects/...`
  for mixed project files, not just videos
- `.wdmc` cache content now routes to `App-Caches/...` even when it lives
  inside a project folder under `Videos`

Verification:

- `python3 -m unittest tests.test_scanner`
- current result: `49 tests`, `OK`

## Keep these artifacts

Primary current artifacts:

- `reports/scan-hash-v21.json`
- `reports/duplicate-review-v1/`
- `reports/scan-nohash-v20.json`
- `reports/final-review-package-v2/`

Older incremental reports from this session are still present:

- `reports/scan-nohash-v16.json`
- `reports/scan-nohash-v17.json`
- `reports/scan-nohash-v18.json`
- `reports/scan-nohash-v19.json`

Working guidance:

- use `reports/scan-hash-v21.json` for duplicate review
- use `reports/duplicate-review-v1/conflicting-destinations.json`
  as the fastest duplicate worklist
- keep `reports/scan-nohash-v20.json` around because earlier suspicious-folder
  review notes refer to it

## Current hashed scan summary

From `reports/scan-hash-v21.json`:

- generated at: `2026-04-05T20:36:59Z`
- total files: `49212`
- images: `15136`
- videos: `816`
- sidecars: `4260`
- caches: `27984`
- unknown: `1016`
- duplicate groups: `2056`
- duplicate files: `4213`

## Duplicate review package summary

From `reports/duplicate-review-v1/`:

- groups touching current review folders: `1851`
- groups with conflicting planned destinations: `2031`
- groups with 3 or more files: `95`

Review tag counts:

- `photos_root`: `1232`
- `google_takeout`: `617`
- `morePics`: `144`
- `bad_1903_bucket`: `4`

Best files to start with later:

- `reports/duplicate-review-v1/conflicting-destinations.json`
- `reports/duplicate-review-v1/review-folder-groups.json`
- `reports/duplicate-review-v1/README.md`

## Folder review results

### `morePics`

`/home/gabriel/Pictures/morePics` is mostly fine now.

- most numbered files already infer to `2006-01-01` or `2007-01-01`
  from filename patterns
- `Thumbs.db` looks disposable
- the remaining unresolved items are still the same `7` image files,
  all dated only by `mtime`
- those `7` files had no EXIF date tags
- those `7` files did not have exact duplicate matches elsewhere in
  `Pictures` when checked manually

Remaining unresolved `morePics` files:

- `Gary and Mom.jpg`
- `Lola 000529.jpg`
- `Lola 081099 Back.jpg`
- `Lola 081099 Front.jpg`
- `Lola 082299.jpg`
- `j01.jpg`
- `j02.jpg`

### `Photos`

`/home/gabriel/Pictures/Photos` is mostly organized, but the loose top-level
items and duplicate spillover still need decisions.

Strong cleanup candidates found:

- `dscf4994-0.jpg` is empty
- `dscf4994-1.jpg` is empty
- `Thumbs.db` is disposable
- `temp/Thumbs.db` is disposable
- `.comments/*.xml` are gzipped Picasa comment metadata with minimal payload
  like `Keywords=Film`

Loose duplicate findings:

- `dscf4994.jpg` matches `Photos/2009/04/09/dscf4994.jpg`
- `dscf5074.jpg` matches `Pictures/2009/04/12/dscf5074.jpg`
- `dscf5452.jpg`, `dscf5452-81.jpg`, and `dscf5452-82.jpg`
  all match `Photos/2009/07/07/dscf5452-83.jpg`
- `impo ige.jpg`, `inang luisa.jpg`, `ingkong dianong.jpg`,
  and `tatang gelacio.jpg` match copies in `Pictures/2009/01/25/`
- `temp/DSCF1376.JPG` matches `Pictures/2008/04/17/DSCF1376.JPG`
  and `Photos/2008/2008-04-20--18.53.11/DSCF1376.JPG`

Likely keepers from the loose `Photos` root:

- `dscf5041.jpg`
- `dscf5075.jpg`

Important video note:

- `Photos/2007/Beng/VIDEO_070.mp4` has no usable embedded creation tags
- it still infers `2007-10-08` from `mtime`
- it is an exact duplicate of `/home/gabriel/Pictures/1903/12/31/VIDEO_070.mp4`
- the `1903/12/31` copy is very likely the bad one to remove later

## Remaining big review areas

Still worth focused attention:

- `/home/gabriel/Pictures/Screenshots`
- `/home/gabriel/Pictures/1903/12/31`
- duplicate groups in `Photos`
- duplicate groups in `morePics`
- duplicate groups involving Google Takeout folders

## Recommended next steps

When work resumes:

1. open `reports/duplicate-review-v1/conflicting-destinations.json`
   and start with tags `bad_1903_bucket`, `morePics`, and `photos_root`
2. make keep-vs-delete decisions for the obvious `Photos` loose duplicates
   and zero-byte files
3. review `/home/gabriel/Pictures/1903/12/31`, especially `VIDEO_070.mp4`
   and any other duplicate spillover there
4. review `/home/gabriel/Pictures/Screenshots` as likely disposable material
5. after any real cleanup outside the tool, rerun a fresh hashed scan
   and write a new report version

Optional future improvement:

- add a dedicated CLI `duplicates-report` command so duplicate review does not
  require opening raw JSON files

## Safety reminder

No apply phase exists yet. Everything remains dry-run planning and review only.
No files were moved or deleted by the tool in this session.
