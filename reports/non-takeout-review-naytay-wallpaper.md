# Non-Takeout Duplicate Review: NayTay Wallpaper Pair

Source report: `reports/scan-hash-v57.json`

## Summary

- duplicate groups: 1
- duplicate files: 2
- source paths: `/home/gabriel/Pictures/NayTay.png` and `/home/gabriel/Pictures/Wallpapers/NayTay.png`
- pattern: exact duplicate file split between the `Pictures` root and the semantically-specific `Wallpapers` folder
- review goal: keep the copy in the clearer destination folder and quarantine the root-level duplicate
- inferred date consistency: both files infer to `2020-04-12` from `mtime`

## Recommendation

- keep: `/home/gabriel/Pictures/Wallpapers/NayTay.png`
- quarantine: `/home/gabriel/Pictures/NayTay.png`

## Rationale

- unlike the earlier mirror-folder cases, this pair is not a dated import-vs-library split
- the `Wallpapers` location is the clearer intentional home for this asset
- keeping the root-level copy would preserve a duplicate in a less-specific location

## Group List

### dup-0003 | NayTay.png

- path: `/home/gabriel/Pictures/NayTay.png`
  proposed: `Library/2020/2020-04-12_Pictures/NayTay.png`
  date source: `mtime`
- path: `/home/gabriel/Pictures/Wallpapers/NayTay.png`
  proposed: `Library/2020/2020-04-12_Wallpapers/NayTay.png`
  date source: `mtime`
