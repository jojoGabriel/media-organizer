# Session Notes - 2026-04-14

## Where the project stands

This continuation started in analysis mode, then moved into manual cleanup
execution outside the organizer.

The organizer still did not move or delete files itself, but reviewed cleanup
batches were manually moved into a quarantine folder outside the scanned roots.

The immediate follow-up from `SESSION_NOTES_2026-04-11.md` was completed for
the three remaining mixed 2014 Google Photos overlay folders called out there:

- `Weekend in Fish Creek`
- `Wednesday morning in Chicago`
- `Trip to Los Angeles and Anaheim`

Primary analysis inputs used:

- `reports/scan-hash-v21.json`
- `reports/scan-hash-v24.json`

## What was established

### Wednesday morning in Chicago

This folder now has a clean plain-media subset backed by non-Takeout local
copies under `/home/gabriel/Pictures/20140723 and earlier/`.

- safe plain subset count: `19`
- composition: `16` images, `3` videos
- manifest:
  `reports/google-takeout-conditional-pass-wednesday-morning-in-chicago-plain.txt`

Still deferred there:

- all `-edited` variants
- `metadata.json`

### Trip to Los Angeles and Anaheim

This folder now has a clean plain-media subset backed by non-Takeout local
copies under `/home/gabriel/Pictures/20140723 and earlier/`.

- safe plain subset count: `29`
- composition: `20` images, `9` videos
- manifest:
  `reports/google-takeout-conditional-pass-trip-to-los-angeles-and-anaheim-plain.txt`

Still deferred there:

- all `-edited` variants
- `metadata.json`

### Weekend in Fish Creek

Most of this folder also cleanly defers to non-Takeout local copies under
`/home/gabriel/Pictures/20140723 and earlier/`.

- safe plain subset count: `17`
- manifest:
  `reports/google-takeout-conditional-pass-weekend-in-fish-creek-plain.txt`

Still deferred there:

- all `-edited` variants
- `metadata.json`

Keep in `Weekend in Fish Creek`:

- `IMG_20140719_165758-SMILE.jpg`
- `IMG_20140719_190437-MOTION.gif`

## New artifacts

- `reports/google-takeout-conditional-pass-weekend-in-fish-creek-plain.txt`
- `reports/google-takeout-conditional-pass-wednesday-morning-in-chicago-plain.txt`
- `reports/google-takeout-conditional-pass-trip-to-los-angeles-and-anaheim-plain.txt`
- `reports/mackinac-safe-pass-plain.txt`
- `reports/scan-hash-v24.json`

## Manual cleanup executed

Two manual quarantine passes were executed outside the tool:

- the reviewed Google Takeout and local duplicate batches from the first
  manifest/script pass
- the `mackinac` exact manifest pass

The quarantine folder was moved outside the scanned roots so follow-up scans
would reflect the real library state.

## Post-cleanup scan result

After the first cleanup pass, `scan-hash-v23.json` became the first true
post-cleanup baseline.

After the `mackinac` pass, the current baseline is now
`reports/scan-hash-v24.json`.

Compared with `scan-hash-v21.json`:

- total files: `49212 -> 47114` (`-2098`)
- images: `15136 -> 13154` (`-1982`)
- videos: `816 -> 741` (`-75`)
- caches: `27984 -> 27962` (`-22`)
- unknown: `1016 -> 997` (`-19`)
- duplicate groups: `2056 -> 308` (`-1748`)
- duplicate files: `4213 -> 620` (`-3593`)
- total bytes removed from scanned roots: `4908989903`

Compared with `scan-hash-v23.json`:

- total files: `47307 -> 47114` (`-193`)
- images: `13347 -> 13154` (`-193`)
- duplicate groups: `501 -> 308` (`-193`)
- duplicate files: `1006 -> 620` (`-386`)
- total bytes removed from scanned roots: `549681376`

The cleanup materially reduced the duplicate problem. Most remaining duplicate
groups are still images rather than videos.

## New likely-safe duplicate batch

`mackinac` was executed as the second clean manual pass.

- `193` exact duplicate-side files were moved out of the scanned roots
- one odd three-file case still remains for manual review:
  `20190705_105025(1).jpg` / `20190705_105025.jpg`

## Current remaining duplicate shape

From `scan-hash-v24.json`, the biggest remaining duplicate clusters are now:

- `Photos/2007/2007-08-26--15.46.09`
- `Photos/2007/08/26`
- `Photos/2007/2007-11-03--17.02.27`
- Google Takeout `Photos from 2014` edited duplicates
- Google Takeout overlay duplicates in
  `Trip to Los Angeles and Anaheim`,
  `Weekend in Fish Creek`,
  `Wednesday morning in Chicago`,
  `Weekend in Niagara Falls and Scarborough`

Google Takeout remainder split:

- plain duplicate groups still present: `42`
- duplicate groups involving `-edited` items: `64`

## Best next step

The highest-value next step is now a focused review of the remaining duplicate
set in `scan-hash-v24.json`, starting with whichever of these you want to
tackle first:

Recommended order:

1. remaining plain Google Takeout duplicate groups (`42`) for another likely
   exact-manifest pass
2. the `Photos/2007` duplicate mirror folders
3. keep all Google Takeout `-edited`, `received_*`, and `metadata.json` cases
   deferred unless reviewed explicitly
4. after any real cleanup, rerun a fresh hashed scan and write a new report
   version before making further organizer decisions

## Safety reminder

This session created notes and manifests, and real files were manually moved
to quarantine outside the scanned roots.
No organizer apply phase exists yet.
