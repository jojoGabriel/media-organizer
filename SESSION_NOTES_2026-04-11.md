# Session Notes - 2026-04-11

## Where the project stands

This session stayed in analysis mode. No media files were moved or deleted.
The organizer is still a safety-first dry-run planner, and the work this
session was focused on turning duplicate analysis into concrete cleanup notes
and filename manifests.

Main current note files:

- [CLEANUP_CANDIDATES_2026-04-11.md](/home/gabriel/Projects/media-organizer/CLEANUP_CANDIDATES_2026-04-11.md)
- [GOOGLE_PHOTOS_SAFE_DATES_2026-04-11.md](/home/gabriel/Projects/media-organizer/GOOGLE_PHOTOS_SAFE_DATES_2026-04-11.md)

## Current artifacts to keep

Primary analysis inputs:

- `reports/scan-hash-v21.json`
- `reports/duplicate-review-v1/`
- `reports/final-review-package-v2/`

Generated cleanup manifests this session:

- `reports/google-takeout-safe-pass-photos-from-2015.txt`
- `reports/google-takeout-safe-pass-jab.txt`
- `reports/google-takeout-safe-pass-jojo-joy.txt`
- `reports/google-takeout-safe-pass-photos-from-2016.txt`
- `reports/google-takeout-safe-pass-photos-from-2014-non-takeout-backed.txt`
- `reports/google-takeout-conditional-pass-memories-together-plain.txt`
- `reports/google-takeout-conditional-pass-jonel-26-plain.txt`

## What was established

### Local duplicate cleanup

The obvious non-Google duplicate cleanup is now documented in
`CLEANUP_CANDIDATES_2026-04-11.md`, including:

- `morePics` numbered duplicate runs plus `IMG142.jpg`, `IMG143.jpg`,
  `Thumbs.db`
- loose duplicate files in `/home/gabriel/Pictures/Photos`
- the bad `1903/12/31` spillover videos:
  `VIDEO_070.mp4`, `VIDEO_076.mp4`, `VIDEO_077.mp4`, `VIDEO_078.mp4`
- `Screenshots` cache junk like `desktop.ini`, `Thumbs.db`, `.wdmc/`
- many duplicate mirror folders under `Photos/2006`, `Photos/2007`,
  `Photos/2008`, and `Photos/2009`

No deletion was performed. These are still manual cleanup candidates only.

### Google Takeout policy

The current keeper policy is now explicit:

1. prefer non-Takeout local canonical copies when they exist
2. otherwise prefer `Photos from YYYY`
3. treat album folders as overlays
4. defer `-edited` items
5. defer `received_*`
6. defer sidecar-gap-heavy cases

### Google Takeout exact manifests

Small exact batches already enumerated:

- `25th`
- `Untitled`
- `Untitled(1)`
- `StarvedRock`
- `Jojo, Joy`
- `Failed Videos`

Larger first safe pass batches already enumerated by filename manifest:

- `Photos from 2015`
- `Jab`
- `Photos from 2016`
- plain non-Takeout-backed subset of `Photos from 2014`

### Mixed Google folders refined

`Memories together (5-23-2021)` is no longer just a cautionary folder.

- `15` plain media names are now extracted into
  `reports/google-takeout-conditional-pass-memories-together-plain.txt`
- those plain items safely defer to either non-Takeout copies or
  `Photos from YYYY`
- still deferred there:
  `IMG_20140615_105848-edited.jpg`,
  `IMG_20140719_142707-edited.jpg`,
  `IMG_20141214_114926-edited.jpg`,
  `metadata.json`

`Jonel 26` is also partially resolved.

- `5` plain media names are now extracted into
  `reports/google-takeout-conditional-pass-jonel-26-plain.txt`
- those plain items defer to `Photos from 2021`
- still deferred there:
  `received_265835921918004.jpeg`,
  `received_894992108014883.jpeg`,
  `metadata.json`

## Date-based Google cleanup note

`GOOGLE_PHOTOS_SAFE_DATES_2026-04-11.md` now gives a date-oriented summary for
later Google Photos cleanup.

Strong date clusters already called out there:

- major 2014 non-Takeout-backed dates
- major 2015 non-Takeout-backed dates
- smaller 2016 safe dates
- `Jab` 2021 overlay dates
- small exact overlay dates for `25th`, `Untitled`, `Untitled(1)`,
  `StarvedRock`, and `Jojo, Joy`
- conditional mixed-folder dates for the plain subsets of
  `Memories together (5-23-2021)` and `Jonel 26`

## Recommended next step

When work resumes, the highest-value continuation is:

1. extract exact plain-media subsets from the remaining mixed 2014 overlay
   folders:
   `Weekend in Fish Creek`,
   `Wednesday morning in Chicago`,
   `Trip to Los Angeles and Anaheim`
2. separate those into:
   `non-Takeout wins`,
   `Photos from 2014 wins`,
   `edited or sidecar-gap defer`
3. add new manifests if the plain subsets are clean enough
4. keep all `-edited`, `received_*`, and sidecar-gap cases deferred

## Safety reminder

This session created notes and manifests only.
No files were moved, renamed, or deleted.
