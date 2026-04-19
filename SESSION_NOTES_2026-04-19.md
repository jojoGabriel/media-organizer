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

## Duplicate and unknown cleanup continuation

The session continued well past the initial `v70` duplicate-review state.

### Safe Google Takeout mirror duplicates were confirmed and deleted

The `v70` duplicate review was narrowed to exact two-path mirror pairs:

- keep side:
  `/home/gabriel/Pictures/google-takeout/...`
- delete side:
  `/home/gabriel/Videos/Pictures/google-takeout/...`

Focused review files created:

- `reports/duplicate-review-v70-safe-mirrors.json`
- `reports/duplicate-review-v70-safe-mirrors.txt`
- `reports/duplicate-review-v70-safe-mirrors-top50.txt`

Confirmed-safe delete plan created:

- `reports/duplicate-review-v70-safe-mirrors-delete-plan.json`
- `reports/duplicate-review-v70-safe-mirrors-delete-paths.txt`
- `reports/duplicate-review-v70-safe-mirrors-delete-summary.txt`

Cleanup result:

- `4515` mirror files deleted from
  `/home/gabriel/Videos/Pictures/google-takeout/...`
- `0` listed paths remained after verification

### Post-cleanup `v71` verified the large duplicate bucket was gone

Verification scan:

- `reports/scan-hash-v71-post-dup-cleanup.json`

Result compared to `v70`:

- duplicate groups: `4626 -> 111`
- duplicate files: `9252 -> 222`

Interpretation:

- the large mirrored Google Takeout duplicate bucket was removed cleanly
- the remaining `111` groups were still mirror pairs, but outside Google
  Takeout

### Remaining non-Takeout mirror duplicates were confirmed and deleted

A fresh duplicate review from `v71` was created:

- `reports/duplicate-review-v71.json`
- `reports/duplicate-review-v71-summary.txt`

That remaining duplicate surface was:

- `111` groups
- `222` files
- about `35.6 MB` potential reclaim

Pattern:

- keep `/home/gabriel/Pictures/...`
- delete `/home/gabriel/Videos/Pictures/...`

Delete plan created:

- `reports/duplicate-review-v71-mirrors-delete-plan.json`
- `reports/duplicate-review-v71-mirrors-delete-paths.txt`
- `reports/duplicate-review-v71-mirrors-delete-summary.txt`

Cleanup result:

- `111` mirror files deleted from `/home/gabriel/Videos/Pictures/...`
- `0` listed paths remained after verification

### `v72` verified duplicate cleanup completion

Verification scan:

- `reports/scan-hash-v72-post-mirror-cleanup.json`

Result:

- duplicate groups: `0`
- duplicate files: `0`

Interpretation:

- duplicate cleanup is complete within the current scan scope

### Unknown-category review replaced the earlier mtime plan

The earlier assumption that `mtime-date` should be the next bucket turned out to
be weak once the post-duplicate library state was inspected.

Raw `mtime` review from `v72`:

- `reports/mtime-review-v72.json`
- `reports/mtime-review-v72-summary.txt`
- `reports/mtime-review-v72-actionable.json`
- `reports/mtime-review-v72-actionable-summary.txt`

What that showed:

- raw `date_source = mtime`: `4398` files
- but `3548` of those were `cache`
- non-cache remainder: `850`
- most of that remainder was still `unknown`, not straightforward media

So the next real cleanup bucket became `unknown-category`, not `mtime-date`.

### Unknown-category review from `v72`

Unknown review files created:

- `reports/unknown-review-v72.json`
- `reports/unknown-review-v72-summary.txt`

Initial `v72` unknown state:

- `1375` files
- about `2.54 GB`

The bucket broke down mostly into:

- `.db`: `672` (mostly `Thumbs.db`)
- `.au`: `565` (mostly PleasantHarmony)
- `.pdf`: `30`
- `.mp3`: `23`
- `.xml`: `20`
- `.kdenlive`: `12`

Interpretation:

- the obvious junk pass was `Thumbs.db`
- PleasantHarmony needed to be isolated as project/audio material, not deleted

### `Thumbs.db` cleanup and `v73` verification

Delete plan created:

- `reports/thumbs-db-delete-plan-v72.json`
- `reports/thumbs-db-delete-paths-v72.txt`
- `reports/thumbs-db-delete-summary-v72.txt`

Cleanup result:

- `668` `Thumbs.db` files deleted
- `0` listed paths remained after verification

Verification scan:

- `reports/scan-hash-v73-post-thumbs-cleanup.json`

Result compared to `v72`:

- total files: `70067 -> 69399`
- unknown files: `1375 -> 707`

Interpretation:

- the obvious unknown junk bucket was removed cleanly

### PleasantHarmony unknowns were isolated and retained

PleasantHarmony-only unknown review files:

- `reports/pleasantharmony-unknown-review-v73.json`
- `reports/pleasantharmony-unknown-review-v73-summary.txt`

Result:

- `606` files
- about `2.43 GB`

Breakdown:

- `.au`: `565`
- `.mp3`: `23`
- `.mka`: `5`
- `.wav`: `3`
- small tail: `.kdenlive`, `.aup`, `.ogg`, `.osp`, `.svg`

Interpretation:

- PleasantHarmony unknowns are mostly real project/audio assets
- they should be preserved or reclassified later, not deleted in a junk pass

### Non-PleasantHarmony unknowns were inspected and split

Remainder review files:

- `reports/non-pleasantharmony-unknown-review-v73.json`
- `reports/non-pleasantharmony-unknown-review-v73-summary.txt`

Remainder at that point:

- `101` files
- about `65 MB`

Classification file created:

- `reports/non-pleasantharmony-unknown-classified-v73.json`

Classification result:

- `44` mirror copies under `/home/gabriel/Videos/Pictures/...`
- `25` metadata/cache-style files
- `32` likely keep/project/document files

### Non-PleasantHarmony mirror unknowns were deleted

Delete plan created:

- `reports/non-pleasantharmony-unknown-mirrors-delete-plan-v73.json`
- `reports/non-pleasantharmony-unknown-mirrors-delete-paths-v73.txt`
- `reports/non-pleasantharmony-unknown-mirrors-delete-summary-v73.txt`

Cleanup result:

- `44` mirror files deleted from `/home/gabriel/Videos/Pictures/...`
- `0` listed paths remained after verification

Verification scan:

- `reports/scan-hash-v74-post-nonph-mirror-cleanup.json`

Result compared to `v73`:

- total files: `69399 -> 69355`
- unknown files: `707 -> 663`

### Final metadata-style unknown tail was reviewed and cleaned

A final small metadata-style review file was created:

- `reports/unknown-metadata-review-v74.json`
- `reports/unknown-metadata-review-v74-summary.txt`

That tail was only `16` files:

- `2` PhotoDirector cache DBs
- `10` `.comments/*.xml`
- `2` `.lvix`
- `2` aborted Kdenlive `.log`

The `.log` files were opened directly and were confirmed to be tiny
aborted-render logs:

- `Started render process ...`
- `Job aborted by user`

Final delete list created:

- `reports/final-metadata-delete-v74.txt`

Cleanup result:

- all `16` files deleted
- `0` listed paths remained after verification

### `v75` established the post-metadata-cleanup baseline

Final re-baseline scan:

- `reports/scan-hash-v75-post-metadata-cleanup.json`

Baseline at that point:

- total files: `69339`
- duplicate groups: `0`
- duplicate files: `0`
- caches: `55924`
- unknowns: `647`

Remaining unknown extensions at `v75`:

- `.au`: `565`
- `.mp3`: `23`
- `.pdf`: `15`
- no-extension: `14`
- `.kdenlive`: `12`
- `.mka`: `5`
- `.wav`: `3`
- `.wmv`: `2`
- `.aup`: `2`
- `.phd`: `1`
- `.xcf`: `1`
- `.flv`: `1`
- `.ogg`: `1`
- `.osp`: `1`
- `.svg`: `1`

Interpretation:

- the remaining unknowns are now almost entirely real asset/project material,
  not obvious junk
- destructive cleanup should stop here unless there is a separate policy
  decision about PleasantHarmony or project-document formats

### PleasantHarmony was then intentionally deleted and `v76` became the current baseline

After the `v75` baseline was established, the user explicitly decided not to
keep the `PleasantHarmony` project.

Action taken:

- deleted `/home/gabriel/Videos/PleasantHarmony`

Verification:

- the directory no longer existed
- no other `PleasantHarmony` directory was found under `/home/gabriel` in the
  checked scope

Final re-baseline scan after that deletion:

- `reports/scan-hash-v76-post-pleasantharmony-delete.json`

Current authoritative baseline at the end of the session:

- total files: `68707`
- duplicates: `0`
- `PleasantHarmony` no longer present in the live library

Interpretation:

- `v76` is the right comparison baseline for future external disks
- any future appearance of `PleasantHarmony` on another disk should be treated
  as intentionally deleted project content, not as an unexpected missing file

## Updated resume point

Current authoritative state is now:

- successful apply execute:
  `reports/apply-log-v69-execute.json`
- duplicate-clean baseline:
  `reports/scan-hash-v72-post-mirror-cleanup.json`
- post-unknown-clean baseline:
  `reports/scan-hash-v75-post-metadata-cleanup.json`
- current final baseline:
  `reports/scan-hash-v76-post-pleasantharmony-delete.json`
- PleasantHarmony unknown review:
  `reports/pleasantharmony-unknown-review-v73.json`
- non-PleasantHarmony classification:
  `reports/non-pleasantharmony-unknown-classified-v73.json`

Best next step when resuming:

1. use `reports/scan-hash-v76-post-pleasantharmony-delete.json` as the live
   library comparison baseline
2. if working with another disk, compare it against `v76` and the keep/delete
   policies recorded here
3. do not reopen duplicate cleanup or the stale `v68` apply issue

## Note for future external disks

If additional hard disks are reviewed later, do not start from scratch.

Use this session's decisions as the policy baseline:

- current authoritative scan baseline:
  `reports/scan-hash-v76-post-pleasantharmony-delete.json`
- duplicates have already been resolved in the live library:
  duplicate groups = `0`
- mirrored copies under `/home/gabriel/Videos/Pictures/...` were treated as
  secondary copies and removed when confirmed against `/home/gabriel/Pictures/...`
- `PleasantHarmony` was intentionally deleted from the live library:
  `/home/gabriel/Videos/PleasantHarmony`
- remaining `unknown` files at `v75` were mostly real asset/project/document
  formats, not obvious junk

For future disk comparisons, the important question is not just
"does this file exist?" but:

- is the disk copy an older mirror of something already kept in the live
  library?
- is it content that was intentionally deleted from the live library
  (for example `PleasantHarmony`) and should therefore be treated as an archive
  decision rather than an accidental missing file?
- is it a file type that was intentionally preserved even though it stayed in
  `unknown`?

When resuming work on another disk later, start by comparing that disk against
the `v76` baseline and against the keep/delete policies recorded here.

## Quarantine folder inspection and cleanup

The quarantine folder was inspected directly:

- `/home/gabriel/media-organizer-quarantine-2026-04-14`

State at inspection time:

- `2410` files
- about `5.73 GB`

Top-level structure showed this is still a deliberate holding area, not random
leftovers. It contains:

- many named `non-takeout-...-batch` folders
- `home/gabriel/Pictures/...`
- internal metadata under `.media-organizer-quarantine-2026-04-14/`

High-level composition:

- `photos_tree`: `1134` files, about `1.46 GB`
- `google_takeout`: `680` files, about `3.17 GB`
- `morePics`: `153` files, about `239 MB`
- `.wdmc` cache: `22` files
- Windows metadata: `19` files
- small other tail: `4` files, about `36 MB`

File types in quarantine at inspection time:

- `2301` `.jpg`
- `77` `.mp4`
- very small tail of `.db`, `.jpeg`, `.gif`, `.avi`, `.png`, `.ini`

Interpretation:

- quarantine should still be treated as a preserved archive/review bucket
- it should not be deleted wholesale
- only obvious junk inside quarantine was safe to remove immediately

### Quarantine junk pass

An explicit junk delete list was created:

- `reports/quarantine-junk-delete-v76.txt`

That list contained only:

- `Thumbs.db`
- `desktop.ini`
- `.wdmc` cache files

Cleanup result:

- `41` files deleted from quarantine
- `0` listed paths remained after verification

This cleanup did **not** touch the actual quarantined media batches.

## Stop point for commit

Safe stop point at the end of this session:

- current live-library baseline:
  `reports/scan-hash-v76-post-pleasantharmony-delete.json`
- session notes updated through quarantine inspection and cleanup
- quarantine media preserved, junk-only pass completed

If resuming later before working on another disk:

1. use `v76` as the live-library baseline
2. treat quarantine as preserved archive material
3. compare any future disk against `v76` and against the policies recorded in
   these notes
