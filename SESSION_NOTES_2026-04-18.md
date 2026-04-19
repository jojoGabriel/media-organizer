# Session Notes - 2026-04-18

## Where the project stands

This session resumed from the completed duplicate-cleanup baseline at:

- `reports/scan-hash-v61.json`

The immediate question was whether any of the previously identified low-risk
manual cleanup work still remained before moving into organization planning.

## What was established

### Manual cleanup driver is exhausted

The existing manual cleanup driver:

- `manual_cleanup_commands_2026-04-14.sh`

was dry-run against the live library state.

Result:

- no remaining `mv -vn` actions were produced
- the script only reported `MISSING` paths for previously reviewed items

This indicates the reviewed cleanup batches covered by that script have already
been applied or are no longer present in the live library.

### Fresh hashed scan matches the prior clean baseline

A new full hashed scan was written to:

- `reports/scan-hash-v62.json`

Compared with `reports/scan-hash-v61.json`:

- total files: `46802 -> 46802` (`0`)
- total bytes: `136734463352 -> 136734463352` (`0`)
- images: `12847 -> 12847` (`0`)
- videos: `736 -> 736` (`0`)
- sidecars: `4260 -> 4260` (`0`)
- caches: `27962 -> 27962` (`0`)
- unknown: `997 -> 997` (`0`)
- duplicate groups: `0 -> 0` (`0`)
- duplicate files: `0 -> 0` (`0`)

This confirms the duplicate-cleanup phase is still complete and no new
duplicate drift appeared between `v61` and `v62`.

### Final review package generated

A fresh review bundle was written to:

- `reports/final-review-v62/`

Key outputs:

- `reports/final-review-v62/README.md`
- `reports/final-review-v62/suspicious-destinations.json`
- `reports/final-review-v62/mtime-summary.json`
- `reports/final-review-v62/google-photos-summary.json`

## Current remaining review shape

From `reports/final-review-v62/README.md`:

- suspicious planned destinations remaining: `15`
- grouped `mtime` patterns remaining: `45`
- Google Photos folders still present in the library: `36`
- Google Photos sidecar-only groups: `732`

The current review surface is no longer duplicate removal. The remaining work
is organizer judgment around destination planning and ambiguous dating.

Most obvious current review clusters:

- `morePics` mtime-dated survivors kept earlier for manual review
- `Screenshots` survivors such as `Screenshot (1).png` and `problem.jpg`
- `Wallpapers`, `googleEarth`, and loose-root images that currently infer dates
  from `mtime`
- a small number of generic-label destination cases such as `joy.png` and
  `Videos/cs50w-project1.mp4`

## Best next step

Use `reports/scan-hash-v62.json` as the active baseline.

The next high-value work is:

1. review the `15` suspicious planned destinations
2. review the `45` grouped `mtime` patterns
3. decide folder-specific destination overrides where `mtime` is clearly not
   the right organizer date
4. only after those reviews, consider any future move/apply phase or backup
   preparation

Duplicate cleanup from this hashed scan set remains complete.

## Follow-up planner update

After the suspicious cases were reviewed, the planner was updated to route
these clearly non-chronological picture folders directly into a `Reference/`
branch instead of the dated `Library/` tree:

- `Pexels`
- `Screenshots`
- `Wallpapers`
- `googleEarth`

A fresh hashed scan was then written to:

- `reports/scan-hash-v63.json`

Compared with `reports/scan-hash-v62.json`:

- total files: `46802 -> 46802` (`0`)
- total bytes: `136734463352 -> 136734463352` (`0`)
- images: `12847 -> 12847` (`0`)
- videos: `736 -> 736` (`0`)
- sidecars: `4260 -> 4260` (`0`)
- caches: `27962 -> 27962` (`0`)
- unknown: `997 -> 997` (`0`)
- duplicate groups: `0 -> 0` (`0`)
- duplicate files: `0 -> 0` (`0`)

The scan content is unchanged, but the planned destination shape improved.

New review bundle:

- `reports/final-review-v63/`

Review improvement from `v62` to `v63`:

- suspicious planned destinations: `15 -> 9`
- grouped `mtime` patterns: `45 -> 39`

New destination root in use:

- `Reference=17`

Remaining suspicious set is now concentrated in:

- `morePics` manual-review survivors
- loose-root `joy.png`
- loose-root `Videos/cs50w-project1.mp4`

This confirms the obvious utility/reference folders have been carved out of the
dated library review surface, leaving the genuinely ambiguous cases for manual
judgment.

## Follow-up planner update 2

The next manual-review pass established that the `morePics` folder behaves like
an old scan/archive bucket rather than a dated event folder. The planner was
updated to route:

- `morePics -> Reference/Legacy-Scans/morePics/`

After that, the root-level coursework files:

- `cs50w-project0.mp4`
- `cs50w-project1.mp4`

were reviewed and routed into:

- `Projects/cs50w/`

These are treated as project outputs rather than dated library media.

A fresh hashed scan was then written to:

- `reports/scan-hash-v65.json`

Compared with `reports/scan-hash-v64.json`:

- total files: `46802 -> 46802` (`0`)
- total bytes: `136734463352 -> 136734463352` (`0`)
- images: `12847 -> 12847` (`0`)
- videos: `736 -> 736` (`0`)
- sidecars: `4260 -> 4260` (`0`)
- caches: `27962 -> 27962` (`0`)
- unknown: `997 -> 997` (`0`)
- duplicate groups: `0 -> 0` (`0`)
- duplicate files: `0 -> 0` (`0`)

New review bundle:

- `reports/final-review-v65/`

Review improvement from `v63` to `v65`:

- suspicious planned destinations: `9 -> 1`
- grouped `mtime` patterns: `39 -> 34`

Destination roots in active use from `v65`:

- `Reference=516`
- `Projects=654`

## Current best next step

At this point the remaining suspicious destination set is down to a single
file:

- `/home/gabriel/Pictures/joy.png`

That item does not yet have enough folder context to justify an automatic
planner override.

The next review work is therefore:

1. decide the final destination class for `joy.png`
2. after that, continue with the remaining non-suspicious `mtime` review
   surface, especially:
   - `ceu`
   - project asset folders under `Videos/PleasantHarmony/...`

## Follow-up planner update 3

`joy.png` was explicitly classified as an old scanned photo with uncertain real
date and routed to:

- `Reference/Legacy-Scans/loose-root/joy.png`

A fresh hashed scan was then written to:

- `reports/scan-hash-v66.json`

Compared with `reports/scan-hash-v65.json`:

- total files: `46802 -> 46802` (`0`)
- total bytes: `136734463352 -> 136734463352` (`0`)
- images: `12847 -> 12847` (`0`)
- videos: `736 -> 736` (`0`)
- sidecars: `4260 -> 4260` (`0`)
- caches: `27962 -> 27962` (`0`)
- unknown: `997 -> 997` (`0`)
- duplicate groups: `0 -> 0` (`0`)
- duplicate files: `0 -> 0` (`0`)

New review bundle:

- `reports/final-review-v66/`

Review improvement from `v65` to `v66`:

- suspicious planned destinations: `1 -> 0`
- grouped `mtime` patterns: `34 -> 33`

Destination roots in active use from `v66`:

- `Reference=517`
- `Projects=654`

## Current best next step

The suspicious destination queue is now cleared.

The next organizer review work is the remaining grouped `mtime` surface,
starting with the largest still-visible clusters:

1. `ceu`
2. `Videos/PleasantHarmony/...` asset and project-support files

Duplicate cleanup remains complete, and the planner no longer has unresolved
generic fallback destinations in the current scan baseline.

## Follow-up planner update 4

The `ceu` folder was reviewed as a coherent shared collection with weak date
evidence:

- all `15` files had no EXIF date
- all file mtimes clustered on `2016-05-10`
- filenames and folder identity were coherent enough to keep the set under
  `Shared/CEU`
- the day itself did not look trustworthy enough for a dated event bucket

The planner was updated to route:

- `ceu -> Shared/CEU/Undated/`

A fresh hashed scan was then written to:

- `reports/scan-hash-v67.json`

Compared with `reports/scan-hash-v66.json`:

- total files: `46802 -> 46802` (`0`)
- total bytes: `136734463352 -> 136734463352` (`0`)
- images: `12847 -> 12847` (`0`)
- videos: `736 -> 736` (`0`)
- sidecars: `4260 -> 4260` (`0`)
- caches: `27962 -> 27962` (`0`)
- unknown: `997 -> 997` (`0`)
- duplicate groups: `0 -> 0` (`0`)
- duplicate files: `0 -> 0` (`0`)

New review bundle:

- `reports/final-review-v67/`

Review improvement from `v66` to `v67`:

- suspicious planned destinations: `0 -> 0`
- grouped `mtime` patterns: `33 -> 18`

Destination roots in active use from `v67`:

- `Shared=1034`
- `Projects=654`
- `Reference=517`

## Current best next step

The remaining `mtime` review surface is now concentrated almost entirely in:

1. `Videos/PleasantHarmony/...` asset and project-support files
2. the root-level `cs50w-project*` pair already routed to `Projects/cs50w/`

The next high-value work is to decide whether project-routed items under
`Projects/...` should remain in the `mtime` review summary at all, or whether
explicit project destinations should be treated as resolved in the same way as
reference and undated shared overrides.

## Follow-up planner update 5

The remaining `mtime` review queue after `v67` consisted entirely of files that
already had explicit `Projects/...` destinations. Those were project assets and
outputs rather than unresolved organizer-date problems.

The `mtime` review helper was updated to treat `Projects/...` destinations as
resolved, the same way it already treated:

- `Reference/...`
- `Shared/nanayCora80th/...`
- `Shared/CEU/Undated/...`

A fresh hashed scan was then written to:

- `reports/scan-hash-v68.json`

Compared with `reports/scan-hash-v67.json`:

- total files: `46802 -> 46802` (`0`)
- total bytes: `136734463352 -> 136734463352` (`0`)
- images: `12847 -> 12847` (`0`)
- videos: `736 -> 736` (`0`)
- sidecars: `4260 -> 4260` (`0`)
- caches: `27962 -> 27962` (`0`)
- unknown: `997 -> 997` (`0`)
- duplicate groups: `0 -> 0` (`0`)
- duplicate files: `0 -> 0` (`0`)

New review bundle:

- `reports/final-review-v68/`

Review improvement from `v67` to `v68`:

- suspicious planned destinations: `0 -> 0`
- grouped `mtime` patterns: `18 -> 0`

## Current best next step

The destination-review queues are now cleared in the current baseline:

- duplicate groups: `0`
- suspicious planned destinations: `0`
- grouped `mtime` patterns: `0`

The next work is no longer planner triage. The remaining review surfaces are:

1. Google Photos-specific follow-up views still captured in the final package:
   - sidecar-only groups
   - received_* folders
   - focused 2014 Google Photos comparisons
2. any future apply/move implementation, if the organizer is going to move
   files instead of only planning destinations
3. backup preparation after destination/planning confidence is high enough

## Backup handoff note

The actual backup step was started manually outside the repo with:

- `cd /home/gabriel && rsync -aHv --info=progress2 Pictures Videos /media/gabriel/BACKUPHD250/`

Important scope note:

- that command backs up `/home/gabriel/Pictures` and `/home/gabriel/Videos`
- it does **not** include the home-level quarantine tree:
  `/home/gabriel/media-organizer-quarantine-2026-04-14`
- it also does **not** include the project repo:
  `/home/gabriel/Projects/media-organizer`

Based on the reviewed cleanup workflow, the minimum backup set that matters for
recovery is:

- `/home/gabriel/Pictures`
- `/home/gabriel/Videos`
- `/home/gabriel/media-organizer-quarantine-2026-04-14`
- `/home/gabriel/Projects/media-organizer`

Reason:

- the reviewed duplicate removals were performed by moving files into
  `/home/gabriel/media-organizer-quarantine-2026-04-14/...`
- every `reports/quarantine_non_takeout_*.sh` script uses that home-level
  quarantine root
- the project repo preserves the scan baselines, review reports, notes, and
  quarantine scripts needed to explain or reproduce cleanup decisions

When the running `rsync` finishes, the next safe checks are:

1. non-destructive compare for `Pictures` and `Videos` with an `rsync` dry-run
2. non-destructive compare/copy for:
   - `media-organizer-quarantine-2026-04-14`
   - `Projects/media-organizer`

Suggested follow-up commands after the current transfer completes:

```bash
cd /home/gabriel
rsync -aHvn --delete Pictures Videos /media/gabriel/BACKUPHD250/
rsync -aHvn --delete media-organizer-quarantine-2026-04-14 Projects/media-organizer /media/gabriel/BACKUPHD250/
```

Interpretation:

- no transfer output means the destination matches for rsync's comparison rules
- delete lines in dry-run output mean the destination contains extra files
- transfer lines mean the destination is missing files or differs from source

If backup continues tomorrow, resume from this point rather than re-opening the
planner review. The planning baseline is already cleared through:

- `reports/scan-hash-v68.json`
- `reports/final-review-v68/`
