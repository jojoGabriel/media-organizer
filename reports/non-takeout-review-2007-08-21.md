# Non-Takeout Duplicate Review: 2007-08-21 Batch

Source report: `reports/scan-hash-v51.json`

## Summary

- duplicate groups: 1
- duplicate files: 2
- source folders: `/home/gabriel/Pictures/Photos/2007/08/21` and `/home/gabriel/Pictures/Photos/2007/2007-08-26--15.46.09`
- pattern: same-content duplicates split between the canonical dated folder and the timestamped import folder
- review goal: keep the canonical dated folder and quarantine the duplicate counterpart from the timestamped import folder
- inferred date consistency: both files infer to `2007-08-20` from `metadata` even though one source folder is named `2007/08/21`

## Recommendation

- keep: `/home/gabriel/Pictures/Photos/2007/08/21/DSCF0292.JPG`
- quarantine: `/home/gabriel/Pictures/Photos/2007/2007-08-26--15.46.09/DSCF0292.JPG`

## Group List

### dup-0011 | DSCF0292.JPG

- path: `/home/gabriel/Pictures/Photos/2007/08/21/DSCF0292.JPG`
  proposed: `Library/2007/2007-08-20_Pictures/DSCF0292.JPG`
  date source: `metadata`
- path: `/home/gabriel/Pictures/Photos/2007/2007-08-26--15.46.09/DSCF0292.JPG`
  proposed: `Library/2007/2007-08-20_2007-08-26--15.46.09/DSCF0292.JPG`
  date source: `metadata`
