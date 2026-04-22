# Session Notes - 2026-04-22

## Backup verification and closure

### Starting state

Initial dry-run checks showed backup was not closed:

- `Number of regular files transferred: 74`
- `Total transferred file size: 9,899,714,854 bytes`

Itemized report was captured to:

- `reports/rsync-pending-transfers-2026-04-22.txt`

### Root cause analysis

The backup target filesystem was confirmed as FAT-family:

- `stat -f -c '%T' /media/gabriel/BACKUPHD250` -> `msdos`

This explained repeated metadata churn with archive mode (`-a`) due to unsupported
permission/timestamp semantics on FAT.

A FAT-safe comparison reduced the actionable delta:

- `rsync -rltDvn --size-only --delete --stats ...`
- pending changed from `74` to `1` file

### Remaining blocker identified

The final `1` file mismatch was a case-collision pair in source:

- `/home/gabriel/Media/Library/2010/2010-05-06_Pictures/DSCF6225.JPG`
- `/home/gabriel/Media/Library/2010/2010-05-06_Pictures/dscf6225.jpg`

Hashes were different, so they are not duplicates:

- `1b216f16...c5c9eed` (`DSCF6225.JPG`)
- `a841f7c4...811f6817` (`dscf6225.jpg`)

FAT cannot store two different files that differ only by letter case in the same
directory name-space.

### Corrective action

Renamed the lowercase variant in source to avoid FAT case collision:

- from: `/home/gabriel/Media/Library/2010/2010-05-06_Pictures/dscf6225.jpg`
- to:   `/home/gabriel/Media/Library/2010/2010-05-06_Pictures/dscf6225-lower.jpg`

During sync attempt, destination was discovered mounted read-only:

- `findmnt ... /media/gabriel/BACKUPHD250` showed `vfat` with `ro`
- rsync produced `Read-only file system (30)` errors

### Final verification state

After remount/write recovery on user side and rerun in FAT-safe mode, dry-run
verification closed:

- `Number of regular files transferred: 0`
- `Total transferred file size: 0 bytes`

### Commands used for stable FAT backup flow

```bash
rsync -rltDv --size-only --delete-before --info=progress2 \
  /home/gabriel/Media/ \
  /media/gabriel/BACKUPHD250/Media/
```

```bash
rsync -rltDvn --size-only --delete --stats \
  /home/gabriel/Media/ \
  /media/gabriel/BACKUPHD250/Media/
```
