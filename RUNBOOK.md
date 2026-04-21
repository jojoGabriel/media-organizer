# Media Organizer Runbook

Repeatable workflow for maintaining `~/Pictures` and `~/Videos`, importing new media, moving safe files into `~/organized-media-dry-run`, and backing up.

## 0) Rules

- Always run a **hashed scan** (do not use `--skip-hash`) before decisions.
- Run `apply` in dry-run first; use `--execute` only when intended.
- Do not bulk-delete unless a file has explicit evidence (usually hash match).
- Keep all action logs in `reports/`.

## 1) Paths Used In This Project

- Source roots:
  - `~/Pictures`
  - `~/Videos`
- Organized library root:
  - `~/organized-media-dry-run`
- Project repo:
  - `~/Projects/media-organizer`
- Quarantine root (current):
  - `~/media-organizer-quarantine-2026-04-14`
- Main backup drive (current):
  - `/media/gabriel/BACKUPHD250`

## 2) Preflight (every session)

```bash
cd ~/Projects/media-organizer
git status --short
```

Note:
- This shows which reports/notes were created in the last run.

## 3) Standard Verification Scan + Dry-Run Apply

### 3.1 Create a new hashed scan report

```bash
cd ~/Projects/media-organizer
python3 -m media_organizer scan \
  --pictures-root ~/Pictures \
  --videos-root ~/Videos \
  --report reports/scan-hash-vNN-description.json
```

Notes:
- Replace `vNN-description` with a new version label.
- This is the source of truth for counts, duplicates, and planned destinations.

### 3.2 Build apply manifest in dry-run mode

```bash
cd ~/Projects/media-organizer
python3 -m media_organizer apply \
  --report reports/scan-hash-vNN-description.json \
  --dest-root ~/organized-media-dry-run \
  --manifest reports/apply-manifest-vNN-description.json
```

Notes:
- If this prints `Built 0 apply operations`, organizer state is currently closed.
- If non-zero, review report before deciding whether to execute.

### 3.3 Optional execute (only if approved)

```bash
cd ~/Projects/media-organizer
python3 -m media_organizer apply \
  --report reports/scan-hash-vNN-description.json \
  --dest-root ~/organized-media-dry-run \
  --manifest reports/apply-manifest-vNN-description.json \
  --log reports/apply-log-vNN-description.json \
  --execute
```

## 4) If You Add New Files Directly To Pictures/Videos

Run section 3 again. That is enough for normal ingestion.

Optional quick count check:

```bash
find ~/Pictures -type f | wc -l
find ~/Videos -type f | wc -l
```

## 5) If You Attach Another Drive To Extract Pictures/Videos

Use a two-step intake: inspect, then copy with `rsync` dry-run first.

### 5.1 Identify mounted drive and filesystem

```bash
lsblk -f
```

Notes:
- Confirm mount path and filesystem type before copy.
- If FAT32 (`vfat`), remember 4 GiB single-file limit.

### 5.2 Dry-run copy from external drive into intake folder

```bash
mkdir -p ~/Pictures/import-intake/$(date +%F)-external
rsync -avhn --info=progress2 \
  /media/gabriel/DRIVE_LABEL/path/to/export/ \
  ~/Pictures/import-intake/$(date +%F)-external/
```

### 5.3 Real copy after review

```bash
rsync -avh --info=progress2 \
  /media/gabriel/DRIVE_LABEL/path/to/export/ \
  ~/Pictures/import-intake/$(date +%F)-external/
```

Then run section 3.

## 6) Google Takeout: Move Unique Media Into Organized Library

Use this when Takeout contains media you want in the library, but only if not already represented by content.

Script:
- `scripts/move_takeout_unique_to_library.py`

Command:

```bash
cd ~/Projects/media-organizer
python3 scripts/move_takeout_unique_to_library.py \
  --scan-report reports/scan-hash-vNN-description.json \
  --organized-root ~/organized-media-dry-run \
  --output-prefix reports/takeout-unique-to-library-move-vNN
```

What it does:
- Reads Takeout image/video entries from the scan report.
- Compares each candidate against existing organized-library content (size + SHA-256).
- Moves only files with no content match.
- Leaves already-represented files untouched.
- Writes:
  - `reports/takeout-unique-to-library-move-vNN.json`
  - `reports/takeout-unique-to-library-move-vNN.txt`

After running it, run section 3 again to refresh baseline.

## 7) Quarantine Workflow

### 7.1 Check remaining quarantine files

```bash
find ~/media-organizer-quarantine-2026-04-14 -type f | wc -l
find ~/media-organizer-quarantine-2026-04-14 -type f | sort
```

### 7.2 Delete only with explicit content evidence

Example hash check:

```bash
sha256sum \
  ~/media-organizer-quarantine-2026-04-14/path/file.ext \
  ~/organized-media-dry-run/path/file.ext
```

If hashes match and policy says duplicate-side file should be dropped, delete that quarantine copy.

## 8) Backup (incremental, same drive)

Use this after any meaningful moves/imports.

```bash
cd /home/gabriel
rsync -aHv --info=progress2 \
  --exclude='Videos/PleasantHarmony/Hymns/hymns.m4v' \
  --exclude='Videos/PleasantHarmony/Hymns/hymns.mp4' \
  --exclude='Videos/PleasantHarmony/Hymns/production ID_4440821 (1) (1) (1).mkv' \
  --exclude='Videos/PleasantHarmony/RM221115A/Untitled Project.mp4' \
  Pictures Videos organized-media-dry-run Projects/media-organizer \
  /media/gabriel/BACKUPHD250/
```

Notes:
- `organized-media-dry-run` is included because this is where integrated files land.
- Excludes are required for current FAT32 backup target.

Optional verification pass:

```bash
cd /home/gabriel
rsync -rltDvn --size-only \
  --out-format='%n' \
  --exclude='*/' \
  Pictures Videos organized-media-dry-run Projects/media-organizer \
  /media/gabriel/BACKUPHD250/
```

## 9) End-of-Session Checklist

- Create/append `SESSION_NOTES_YYYY-MM-DD.md` with:
  - commands run
  - report files produced
  - counts (`moved`, `skipped`, `errors`)
  - backup outcome
- Confirm close condition:
  - latest apply dry-run is `0` operations, or intentional non-zero with documented plan.

## 10) Command Template Quick Copy

```bash
# 1) scan
python3 -m media_organizer scan --pictures-root ~/Pictures --videos-root ~/Videos --report reports/scan-hash-vNN.json

# 2) apply dry-run
python3 -m media_organizer apply --report reports/scan-hash-vNN.json --dest-root ~/organized-media-dry-run --manifest reports/apply-manifest-vNN.json

# 3) takeout unique move (optional)
python3 scripts/move_takeout_unique_to_library.py --scan-report reports/scan-hash-vNN.json --organized-root ~/organized-media-dry-run --output-prefix reports/takeout-unique-to-library-move-vNN

# 4) rescan after changes
python3 -m media_organizer scan --pictures-root ~/Pictures --videos-root ~/Videos --report reports/scan-hash-vNN-post.json

# 5) backup
cd /home/gabriel && rsync -aHv --info=progress2 --exclude='Videos/PleasantHarmony/Hymns/hymns.m4v' --exclude='Videos/PleasantHarmony/Hymns/hymns.mp4' --exclude='Videos/PleasantHarmony/Hymns/production ID_4440821 (1) (1) (1).mkv' --exclude='Videos/PleasantHarmony/RM221115A/Untitled Project.mp4' Pictures Videos organized-media-dry-run Projects/media-organizer /media/gabriel/BACKUPHD250/
```
