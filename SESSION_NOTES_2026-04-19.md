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

