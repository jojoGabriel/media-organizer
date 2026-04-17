# Session Notes - 2026-04-16

## Where the project stands

This session picked up from the non-Takeout duplicate review baseline at:

- `reports/scan-hash-v32.json`

The work stayed focused on low-risk duplicate batches where:

- the duplicate pairs were exact hash matches
- inferred dates matched on both sides
- the only planning difference was a cleaner canonical folder versus a
  timestamped import folder or a renamed-copy suffix

The `Shared/Tito-Osias` ownership conflict batch was intentionally deferred.

## Cleanup applied this session

Applied non-Takeout batches:

- `62` files from
  `Pictures/Photos/2007/2007-08-26--15.46.09`
  against `Pictures/Photos/2007/08/26`
- `26` files from
  `Pictures/Photos/2007/2007-11-03--17.02.27`
  against `Pictures/2007/10/14`
- `15` files from
  `Pictures/Photos/2008/2008-04-20--18.53.11`
  against `Pictures/2008/04/19`
- `13` files from
  `Pictures/Photos/2008/12/17`
  against `Pictures/2008/12/17`
- `10` internal renamed-copy files from
  `Pictures/Photos/2008/04/22`
  where the `-1` suffixed duplicate was quarantined and the base filename kept
- `6` files from
  `Pictures/Photos/2007/2007-11-03--17.02.27`
  against `Pictures/2007/10/06`

Artifacts written during the session:

- `reports/non-takeout-review-2007-08-26.md`
- `reports/quarantine_non_takeout_2007_08_26.sh`
- `reports/non-takeout-review-2007-10-14.md`
- `reports/quarantine_non_takeout_2007_10_14.sh`
- `reports/non-takeout-review-2008-04-19.md`
- `reports/quarantine_non_takeout_2008_04_19.sh`
- `reports/non-takeout-review-2008-12-17.md`
- `reports/quarantine_non_takeout_2008_12_17.sh`
- `reports/non-takeout-review-2008-04-22-internal.md`
- `reports/quarantine_non_takeout_2008_04_22_internal.sh`
- `reports/non-takeout-review-2007-10-06.md`
- `reports/quarantine_non_takeout_2007_10_06.sh`

Two extracted review batches initially included one stale filename each and were
corrected before the final follow-up scans:

- `2008-04-19`:
  scripted `DSCF1473.JPG` was corrected to `DSCF1465.JPG`
- `2008-12-17`:
  scripted `dscf3574.jpg` was corrected to `dscf3568.jpg`

## Scan progression

Session progression from the `v32` baseline:

- `scan-hash-v32.json -> scan-hash-v33.json`
  after clearing the `2007-08-26` pair set:
  total files `47007 -> 46945` (`-62`),
  images `13052 -> 12990` (`-62`),
  duplicate groups `202 -> 140` (`-62`),
  duplicate files `407 -> 283` (`-124`)
- `scan-hash-v33.json -> scan-hash-v34.json`
  after clearing the `2007-10-14` pair set:
  total files `46945 -> 46919` (`-26`),
  images `12990 -> 12964` (`-26`),
  duplicate groups `140 -> 114` (`-26`),
  duplicate files `283 -> 231` (`-52`)
- `scan-hash-v34.json -> scan-hash-v35.json`
  after clearing the `2008-04-19` pair set:
  total files `46919 -> 46904` (`-15`),
  images `12964 -> 12949` (`-15`),
  duplicate groups `114 -> 99` (`-15`),
  duplicate files `231 -> 201` (`-30`)
- `scan-hash-v35.json -> scan-hash-v36.json`
  after clearing the `2008-12-17` pair set:
  total files `46904 -> 46891` (`-13`),
  images `12949 -> 12936` (`-13`),
  duplicate groups `99 -> 86` (`-13`),
  duplicate files `201 -> 175` (`-26`)
- `scan-hash-v36.json -> scan-hash-v37.json`
  after clearing the internal `2008-04-22` renamed-copy set:
  total files `46891 -> 46881` (`-10`),
  images `12936 -> 12926` (`-10`),
  duplicate groups `86 -> 76` (`-10`),
  duplicate files `175 -> 155` (`-20`)
- `scan-hash-v37.json -> scan-hash-v38.json`
  after clearing the `2007-10-06` pair set:
  total files `46881 -> 46875` (`-6`),
  images `12926 -> 12920` (`-6`),
  duplicate groups `76 -> 70` (`-6`),
  duplicate files `155 -> 143` (`-12`)

Current scan baseline:

- `reports/scan-hash-v38.json`

## Current non-Takeout remainder

From `scan-hash-v38.json`:

- duplicate groups remaining: `70`
- duplicate files remaining: `143`

Top remaining low-risk review batches:

- `6` groups:
  `Pictures/2007/10/27 <-> Photos/2007/2007-11-03--17.02.27`
- `5` groups:
  `Pictures/2007/10/19 <-> Photos/2007/2007-11-03--17.02.27`
- `4` groups:
  `Pictures/2007/09/30 <-> Photos/2007/2007-11-03--17.02.27`

Deferred higher-risk batch:

- `8` groups:
  `Pictures/2014/08/31 <-> Pictures/Tito Osias`
  because it crosses `Library/...` versus `Shared/Tito-Osias/...`

## Best next step

Continue draining the remaining `2007-11-03--17.02.27` low-risk duplicates in
descending batch size before touching the `Tito Osias` ownership conflict.
