# Session Notes - 2026-04-15

## Where the project stands

This session moved from cleanup follow-through into baseline correction.

The main issue from the prior session was confirmed and fixed: the active
quarantine folder had been created under `/home/gabriel/Pictures/`, which is
inside the scanned `pictures` root. That would have polluted future scans.

The quarantine tree is now normalized at:

- `/home/gabriel/media-organizer-quarantine-2026-04-14`

This merged:

- the hidden quarantine folder that had been created under `Pictures`
- the pre-existing malformed home-level quarantine directory whose name
  contained a newline

The cleanup script was also corrected so future runs quarantine to the
home-level path instead of recreating a folder under `Pictures`.

## Cleanup applied this session

This session ended up clearing the remaining plain Google Takeout exact
duplicate media that had already been reviewed or were explicitly approved
during the session.

Applied batches:

- `11` files from the first non-Takeout-backed follow-up batch:
  `Photos from 2013`, `Failed Videos`, `Untitled(4)`,
  `Weekend in Niagara Falls and Scarborough`
- `7` files from `25th`
- `5` files from `StarvedRock`
- `11` files from `Untitled` and `Untitled(1)`
- `2` overlay files from `Weekend in Niagara Falls and Scarborough`
- `4` final explicit-override files from
  `Weekend in Fish Creek`, `Untitled(2)`, and `Untitled(3)`
- `65` edited-overlay files across
  `Trip to Los Angeles and Anaheim`,
  `Wednesday morning in Chicago`,
  `Weekend in Fish Creek`,
  `Weekend in Niagara Falls and Scarborough`,
  `Memories together (5-23-2021)`,
  and `Untitled(4)`
- `2` `received_*` files from `Jonel 26`

All moved files were verified in quarantine and confirmed absent from their
original Google Takeout source paths afterward.

## Scan progression

After relocating quarantine outside the scanned roots and applying the pending
batch, a fresh hashed scan was written to:

- `reports/scan-hash-v25.json`

Compared with `reports/scan-hash-v24.json`:

- total files: `47114 -> 47103` (`-11`)
- total bytes: `137557071852 -> 137153785247` (`-403286605`)
- images: `13154 -> 13147` (`-7`)
- videos: `741 -> 737` (`-4`)
- duplicate groups: `308 -> 297` (`-11`)
- duplicate files: `620 -> 598` (`-22`)

The delta matches the applied quarantine batch exactly.

Subsequent cleanup and scan progression:

- `scan-hash-v25.json -> scan-hash-v26.json`
  after `25th`:
  total files `47103 -> 47096` (`-7`),
  images `13147 -> 13140` (`-7`),
  duplicate groups `297 -> 290` (`-7`),
  duplicate files `598 -> 584` (`-14`)
- `scan-hash-v26.json -> scan-hash-v27.json`
  after `StarvedRock`:
  total files `47096 -> 47091` (`-5`),
  images `13140 -> 13135` (`-5`),
  duplicate groups `290 -> 285` (`-5`),
  duplicate files `584 -> 574` (`-10`)
- `scan-hash-v27.json -> scan-hash-v28.json`
  after `Untitled` and `Untitled(1)`:
  total files `47091 -> 47080` (`-11`),
  images `13135 -> 13124` (`-11`),
  duplicate groups `285 -> 274` (`-11`),
  duplicate files `574 -> 552` (`-22`)
- `scan-hash-v28.json -> scan-hash-v29.json`
  after the Niagara overlay pair:
  total files `47080 -> 47078` (`-2`),
  images `13124 -> 13123` (`-1`),
  videos `737 -> 736` (`-1`),
  duplicate groups `274 -> 272` (`-2`),
  duplicate files `552 -> 548` (`-4`)
- `scan-hash-v29.json -> scan-hash-v30.json`
  after the final explicit-override batch:
  total files `47078 -> 47074` (`-4`),
  images `13123 -> 13119` (`-4`),
  duplicate groups `272 -> 268` (`-4`),
  duplicate files `548 -> 540` (`-8`)
- `scan-hash-v30.json -> scan-hash-v31.json`
  after treating edited overlays the same way as the plain overlays:
  total files `47074 -> 47009` (`-65`),
  images `13119 -> 13054` (`-65`),
  duplicate groups `268 -> 204` (`-64`),
  duplicate files `540 -> 411` (`-129`)
- `scan-hash-v31.json -> scan-hash-v32.json`
  after the final `received_*` pass from `Jonel 26`:
  total files `47009 -> 47007` (`-2`),
  images `13054 -> 13052` (`-2`),
  duplicate groups `204 -> 202` (`-2`),
  duplicate files `411 -> 407` (`-4`)

Current scan baseline:

- `reports/scan-hash-v32.json`

## Current Google Takeout remainder

From `scan-hash-v32.json`:

- plain Google Takeout duplicate groups still present: `0`
- duplicate groups involving `-edited` items: `0`
- duplicate groups involving `received_*`: `0`

The Google Takeout duplicate remainder has now been fully cleared from the scan
baseline.

## Best next step

The next step is no longer Google Takeout duplicate cleanup.

The highest-value remaining work is now review of the non-Takeout duplicate
remainder still present elsewhere in the library, using
`reports/scan-hash-v32.json` as the new baseline.
