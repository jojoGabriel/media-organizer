# Session Notes - 2026-04-19

## Where the project stands

This session resumed after the planner-review baseline had already been cleared
through:

- `reports/scan-hash-v68.json`
- `reports/final-review-v68/`

The work in this session was not planner triage. It was backup verification and
cleanup of a copy-paste mistake during the external backup run.

## What was established

### Accidental duplicate directory was created by a bad backup paste

A stray directory existed at:

- `/home/gabriel/Projects/media-`

This was at the same level as:

- `/home/gabriel/Projects/media-organizer`

Inspection showed it was not an empty typo folder. It contained about `128G` of
duplicate media content under:

- `/home/gabriel/Projects/media-/Videos/...`
- `/home/gabriel/Projects/media-/Videos/Pictures/...`

That tree was verified against the live source folders with dry-run `rsync`:

- `/home/gabriel/Videos/ -> /home/gabriel/Projects/media-/Videos/`
- `/home/gabriel/Pictures/ -> /home/gabriel/Projects/media-/Videos/Pictures/`

Both checks reported `0` files needing transfer, confirming the `media-` tree
was an accidental duplicate copy rather than unique data.

The directory was then deleted.

### Backup failure cause was identified

The backup target:

- `/media/gabriel/BACKUPHD250`

was confirmed to be mounted as:

- `vfat`

This explains the earlier `rsync` failure:

- `rsync: write failed ... File too large (27)`

because FAT32/vfat cannot store files larger than `4 GiB`.

The blocked files confirmed during this session were:

- `/home/gabriel/Videos/PleasantHarmony/Hymns/hymns.m4v`
- `/home/gabriel/Videos/PleasantHarmony/Hymns/hymns.mp4`
- `/home/gabriel/Videos/PleasantHarmony/Hymns/production ID_4440821 (1) (1) (1).mkv`
- `/home/gabriel/Videos/PleasantHarmony/RM221115A/Untitled Project.mp4`

Those files were intentionally excluded from the resumed backup run.

### Backup was resumed successfully with explicit excludes

The media backup was resumed manually outside the repo with the same source
roots but with explicit excludes for the FAT32-blocked files.

The resumed transfer completed successfully.

The quarantine tree and project repo were then backed up as well:

- `/home/gabriel/media-organizer-quarantine-2026-04-14`
- `/home/gabriel/Projects/media-organizer`

### Verification result

Verification on a FAT32 destination needed to be interpreted carefully because
directory metadata and timestamps do not round-trip like they would on a native
Linux filesystem.

The practical content check that mattered was:

```bash
cd /home/gabriel
rsync -rltDvn --size-only \
  --out-format='%n' \
  --exclude='*/' \
  media-organizer-quarantine-2026-04-14 \
  Projects/media-organizer \
  /media/gabriel/BACKUPHD250/
```

Result:

- no file-content differences were reported

Current practical backup state:

- `Pictures`: backed up
- `Videos`: backed up except the 4 intentionally excluded large files
- `media-organizer-quarantine-2026-04-14`: backed up
- `Projects/media-organizer`: backed up

## Important limitation

This backup is good enough for practical recovery on the current disk, but it
is constrained by the destination filesystem.

Known gap still not present on the FAT32 backup disk:

- `Videos/PleasantHarmony/Hymns/hymns.m4v`
- `Videos/PleasantHarmony/Hymns/hymns.mp4`
- `Videos/PleasantHarmony/Hymns/production ID_4440821 (1) (1) (1).mkv`
- `Videos/PleasantHarmony/RM221115A/Untitled Project.mp4`

If those `PleasantHarmony` files are later deleted manually from the live
library, do not assume they are recoverable from this backup disk unless they
have been copied elsewhere first.

## Recommendation for future backup media

For a future external backup drive:

- prefer `exfat` for a general-purpose cross-platform external disk
- prefer `ext4` for a Linux-only backup disk
- avoid `vfat` / FAT32 for this media library because of the `4 GiB` file limit

## Follow-up Google Photos review

After backup verification was closed, the remaining Google Photos review surface
from `reports/final-review-v68/` was reviewed directly.

### `received_*` review result

From `reports/final-review-v68/google-photos-received.json`:

- `43` `received_*` media files and `45` sidecars remain across `6` folders
- yearly folders involved: `Photos from 2021`, `2022`, `2023`, `2024`, `2025`
- one older folder still has sidecar-only `received_*` residue:
  `Jonel 26`

Interpretation:

- these are not duplicate-cleanup leftovers
- they are Google Photos export artifacts for received/shared items
- keep them in the Google Photos review bucket; do not treat them as safe local
  delete candidates and do not infer web-delete safety from them

### Sidecar-gap review result

From `reports/final-review-v68/google-photos-sidecar-gaps.json`:

- total sidecar-only groups remaining: `732`

Largest buckets:

- `Photos from 2022`: `140`
- `Photos from 2014`: `105`
- `Photos from 2015`: `68`
- `Photos from 2024`: `68`
- `Archive`: `43`
- `Photos from 2021`: `38`
- `Jab`: `30`
- `Trip to Los Angeles and Anaheim`: `30`
- `Photos from 2023`: `29`
- `Photos from 2025`: `20`
- `Wednesday morning in Chicago`: `20`
- `Weekend in Fish Creek`: `20`

What this breaks down to:

- `Archive` is dominated by screenshot sidecars
- `Photos from 2021` through `2025` are dominated by burst/portrait sidecars and
  a small number of Messenger/RTC artifacts
- older event folders such as `Jab`, `Trip to Los Angeles and Anaheim`,
  `Wednesday morning in Chicago`, `Weekend in Fish Creek`,
  `Memories together (5-23-2021)`, `25th`, and `Jonel 26` are mostly
  sidecar-only residue for already reviewed Google Photos event folders

This means the remaining sidecar-gap surface is primarily export-shape residue,
not a new duplicate-removal opportunity.

### Focused 2014 comparison result

From `reports/final-review-v68/google-photos-2014-review.json`:

- focused review matches: `108`
- dates involved:
  - `2014-05-28`: `37`
  - `2014-06-21`: `28`
  - `2014-07-19`: `43`

Comparison against existing 2014 review manifests showed:

- `87` of the `108` focused matches were already covered by prior
  safe-pass/conditional-pass files
- the remaining `21` uncovered matches are all from `2014-05-28`
- all `21` have non-Takeout counterparts under:
  `/home/gabriel/Pictures/20140723 and earlier/`

To make that residue explicit, a supplemental manifest was added:

- `reports/google-takeout-conditional-pass-wednesday-morning-in-chicago-additional-plain.txt`

## Best next step

The Google Photos review surface is now reduced to policy rather than discovery:

1. keep `received_*` and sidecar-gap cases as review-only export artifacts
2. if you want explicit folder-by-folder closure, roll the supplemental
   `2014-05-28` manifest into the older Chicago review set and mark that date as
   fully reviewed
3. otherwise, the next meaningful project step is no longer more Google Photos
   inventory work; it is deciding whether to build an apply/move phase or keep
   the repo as scan-and-plan only

## Apply recovery and verification

Later in the same session, the repo moved from scan-and-plan into the real
apply phase.

### Apply command was implemented and tested

The repo now has a conservative `apply` command in:

- `media_organizer/cli.py`

Supporting tests were added in:

- `tests/test_scanner.py`

The command behavior established in this session:

- builds a move manifest from an existing scan report
- defaults to dry-run
- verifies source `size_bytes` and `modified_at` against the saved report before
  moving
- treats matching destination content as idempotent `already-present`
- supports copy-verify-delete fallback across filesystems
- writes optional manifest and execution log files

### First execute against `v68` failed because the report was stale

This command was run manually:

```bash
python3 -m media_organizer apply \
  --report reports/scan-hash-v68.json \
  --dest-root /home/gabriel/organized-media-dry-run \
  --manifest reports/apply-manifest-v68-dry-run.json \
  --log reports/apply-log-v68-execute.json \
  --execute
```

It reported:

- `Applied 0 operations successfully; 8938 conflicts/errors`

Diagnosis from the log and manifest:

- `8826` entries were `source file no longer exists`
- `104` entries were reported as `source size no longer matches the saved report`
- `8` entries were true `destination exists with different content` conflicts

Cross-checking the manifest showed the real pattern:

- `8826` operations had `source missing` and `destination already present`
- `104` had `source present` and `destination missing`
- `8` had both `source` and `destination` present

Interpretation:

- `reports/scan-hash-v68.json` was stale relative to the live library
- most of the planned payload had already been moved into
  `/home/gabriel/organized-media-dry-run`
- rerunning `apply` against `v68` was invalid and should not be repeated

Review files created from that failed execute:

- `reports/apply-log-v68-review-summary.txt`
- `reports/apply-log-v68-size-mismatches.json`
- `reports/apply-log-v68-conflicts.json`
- `reports/apply-log-v68-missing-sources.json`

### A zero-byte apply validation bug was found and fixed

One of the `v68` size-mismatch cases:

- `/home/gabriel/Pictures/2011/03/31/DSCF6801.JPG`

was checked directly and found to be:

- still present
- legitimately `0` bytes
- also recorded as `0` bytes in the saved scan report

This exposed a bug in `verify_source_matches_report()`:

- `operation.get("size_bytes") or -1` treated `0` as if the report size were
  missing
- zero-byte files were therefore falsely rejected as size mismatches

Fix applied:

- `media_organizer/cli.py` now distinguishes `None` from `0`
- a regression test for zero-byte files was added to
  `tests/test_scanner.py`

Test status after the fix:

- `python3 -m unittest tests.test_scanner`
- `65` tests, `OK`

### Fresh scan `v69` was generated and executed successfully

A fresh full-hash scan was run:

- `reports/scan-hash-v69.json`

Result:

- `84091` files scanned

Then a fresh dry-run manifest was built:

- `reports/apply-manifest-v69-dry-run.json`

Manifest shape before execute:

- `9398` apply operations
- `74693` skipped items
- all `9398` sources existed
- `8769` destinations already existed
- `629` destinations were still missing

Important structural discovery:

- most pending sources now lived under `/home/gabriel/Videos/Pictures/...`

This was consistent with the earlier partial move state.

The fresh execute command:

```bash
python3 -m media_organizer apply \
  --report reports/scan-hash-v69.json \
  --dest-root /home/gabriel/organized-media-dry-run \
  --manifest reports/apply-manifest-v69-dry-run.json \
  --log reports/apply-log-v69-execute.json \
  --execute
```

Final result:

- `Applied 9398 operations successfully; 0 conflicts/errors`

The process looked I/O-bound while running:

- `ps` showed `D+`

but it completed successfully and did not need intervention.

### Post-run verification `v70` confirmed apply completion

A post-apply verification scan was run:

- `reports/scan-hash-v70-post-verify.json`

Result:

- `74693` files scanned

Then a verification dry-run manifest was built:

- `reports/apply-manifest-v70-post-verify.json`

Verification result:

- `0` remaining apply operations
- `74693` skipped items only

Skip breakdown after the successful apply:

- `cache`: `55924`
- `duplicate-group`: `9046`
- `google-takeout`: `4240`
- `unmatched-sidecar`: `2262`
- `sidecar-target-not-selected`: `1573`
- `no-destination`: `755`
- `unknown-category`: `620`
- `mtime-date`: `265`
- `pleasantharmony`: `8`

Interpretation:

- under the current conservative rules, the move/apply phase to
  `/home/gabriel/organized-media-dry-run` is complete
- there are no remaining standard-library moves pending
- the next work is policy review of the excluded buckets, not more apply work

### Duplicate review package was generated from the post-verify state

A built-in final review bundle was generated for `v70`:

- `reports/final-review-v70-duplicates/`

That bundle did not include a duplicate-specific JSON, so a focused duplicate
report was created directly from `reports/scan-hash-v70-post-verify.json`:

- `reports/duplicate-review-v70.json`
- `reports/duplicate-review-v70-summary.txt`

Duplicate review summary:

- `4626` duplicate groups
- `9252` duplicate files
- about `12.1 GB` potential reclaim if keeping one file per group

The largest duplicate groups are dominated by mirrored Google Takeout videos
that exist in both:

- `/home/gabriel/Pictures/google-takeout/...`
- `/home/gabriel/Videos/Pictures/google-takeout/...`

Examples called out during the session:

- `dup-4482`: `VID_20220915_141013280.mp4`
- `dup-0997`: `VID_20220909_124255254.mp4`
- `dup-3122`: `VID_20220909_124029024.mp4`
- `dup-0115`: `VID_20220909_115338086.mp4`
- `dup-3576`: `VID_20220909_124636616.mp4`

## Recommended resume point for next session

If resuming later, do not revisit the `v68` apply failure. That issue is
resolved.

Current authoritative state is:

- successful execute log:
  `reports/apply-log-v69-execute.json`
- clean post-run verification:
  `reports/scan-hash-v70-post-verify.json`
  and `reports/apply-manifest-v70-post-verify.json`
- duplicate review output:
  `reports/duplicate-review-v70.json`
  and `reports/duplicate-review-v70-summary.txt`

Best next step when resuming:

1. continue duplicate review from `reports/duplicate-review-v70.json`
2. start with the highest reclaim mirrored Google Takeout pairs
3. only after duplicate policy is settled, consider `mtime-date` or
   `unknown-category`
