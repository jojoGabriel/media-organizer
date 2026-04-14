# Google Photos Safe Dates - 2026-04-11

Date-oriented summary for the first safe Google Photos cleanup pass.

These dates come from duplicate sets where:

- a non-Takeout local canonical copy already exists, or
- a pure album overlay defers cleanly to `Photos from YYYY`

Still excluded:

- `-edited` items
- `received_*` items
- sidecar-gap-heavy cases
- most mixed album overlays until their plain subsets are separated

## Strongest Safe Date Clusters

### 2014

Highest-count safe dates from the non-Takeout-backed `Photos from 2014` subset:

- `2014-07-19`: `43`
- `2014-06-21`: `28`
- `2014-08-24`: `21`
- `2014-11-15`: `18`
- `2014-12-24`: `15`
- `2014-06-15`: `14`
- `2014-08-30`: `12`
- `2014-06-23`: `11`
- `2014-09-07`: `9`
- `2014-12-12`: `9`

Other notable safe 2014 dates:

- `2014-11-03`: `8`
- `2014-10-11`: `6`
- `2014-08-11`: `5`
- `2014-10-19`: `5`
- `2014-11-01`: `5`
- `2014-11-09`: `5`
- `2014-12-21`: `5`

Manifest:

- [google-takeout-safe-pass-photos-from-2014-non-takeout-backed.txt](/home/gabriel/Projects/media-organizer/reports/google-takeout-safe-pass-photos-from-2014-non-takeout-backed.txt)

### 2015

Highest-count safe dates from `Photos from 2015`:

- `2015-03-22`: `12`
- `2015-01-10`: `7`
- `2015-04-05`: `7`
- `2015-09-07`: `7`
- `2015-04-18`: `6`
- `2015-12-05`: `6`
- `2015-12-24`: `6`
- `2015-03-19`: `5`
- `2015-03-24`: `5`
- `2015-09-25`: `5`
- `2015-10-03`: `5`

Manifest:

- [google-takeout-safe-pass-photos-from-2015.txt](/home/gabriel/Projects/media-organizer/reports/google-takeout-safe-pass-photos-from-2015.txt)

### 2016

Safe dates from `Photos from 2016`:

- `2016-03-22`: `6`
- `2016-01-01`: `4`
- `2016-02-14`: `1`
- `2016-03-30`: `1`

Manifest:

- [google-takeout-safe-pass-photos-from-2016.txt](/home/gabriel/Projects/media-organizer/reports/google-takeout-safe-pass-photos-from-2016.txt)

### 2021 Overlay

Safe album-overlay dates from `Jab`:

- `2021-10-26`: `38`
- `2021-11-05`: `3`
- `2021-11-08`: `2`
- `2021-11-12`: `2`
- `2021-10-27`: `1`
- `2021-11-22`: `1`

Manifest:

- [google-takeout-safe-pass-jab.txt](/home/gabriel/Projects/media-organizer/reports/google-takeout-safe-pass-jab.txt)

### Conditional Mixed-Folder Dates

These are safe only for the plain-media subsets already split out of mixed
folders. Edited files, `received_*`, and `metadata.json` still stay deferred.

`Memories together (5-23-2021)` plain subset:

- `2014-06-15`: `1`
- `2014-07-19`: `1`
- `2014-12-14`: `1`
- `2016-04-17`: `1`
- `2017-05-29`: `1`
- `2017-12-25`: `1`
- `2018-04-18`: `1`
- `2018-05-28`: `1`
- `2018-08-04`: `1`
- `2018-11-28`: `1`
- `2019-03-09`: `1`
- `2019-05-20`: `1`
- `2020-12-31`: `1`
- `2021-01-31`: `1`
- `2021-05-21`: `1`

`Jonel 26` plain subset:

- `2021-04-19`: `5`

`Weekend in Fish Creek` plain subset:

- `2014-07-19`: `17`

Still deferred there:

- all `-edited` variants
- `metadata.json`

Keep in that folder:

- `IMG_20140719_165758-SMILE.jpg`
- `IMG_20140719_190437-MOTION.gif`

`Wednesday morning in Chicago` plain subset:

- `2014-05-28`: `19`

Still deferred there:

- all `-edited` variants
- `metadata.json`

`Trip to Los Angeles and Anaheim` plain subset:

- `2014-06-21`: `18`
- `2014-06-22`: `1`
- `2014-06-23`: `10`

Still deferred there:

- all `-edited` variants
- `metadata.json`

Manifests:

- [google-takeout-conditional-pass-memories-together-plain.txt](/home/gabriel/Projects/media-organizer/reports/google-takeout-conditional-pass-memories-together-plain.txt)
- [google-takeout-conditional-pass-jonel-26-plain.txt](/home/gabriel/Projects/media-organizer/reports/google-takeout-conditional-pass-jonel-26-plain.txt)
- [google-takeout-conditional-pass-weekend-in-fish-creek-plain.txt](/home/gabriel/Projects/media-organizer/reports/google-takeout-conditional-pass-weekend-in-fish-creek-plain.txt)
- [google-takeout-conditional-pass-wednesday-morning-in-chicago-plain.txt](/home/gabriel/Projects/media-organizer/reports/google-takeout-conditional-pass-wednesday-morning-in-chicago-plain.txt)
- [google-takeout-conditional-pass-trip-to-los-angeles-and-anaheim-plain.txt](/home/gabriel/Projects/media-organizer/reports/google-takeout-conditional-pass-trip-to-los-angeles-and-anaheim-plain.txt)

## Small Exact Date Buckets

Pure small overlay folders already enumerated:

- `2019-05-20` via `25th`
- `2022-05-14` via `Untitled(1)`
- `2022-05-15` via `Untitled`
- `2021-04-03` via `StarvedRock`
- `2021-09-29` via `Jojo, Joy`
- `2021-11-15` via `Jojo, Joy`
- `2022-07-04` via `Jojo, Joy`
- `2014-06-23` failed-video duplicate

See the main checklist:

- [CLEANUP_CANDIDATES_2026-04-11.md](/home/gabriel/Projects/media-organizer/CLEANUP_CANDIDATES_2026-04-11.md)
