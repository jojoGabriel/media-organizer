# Non-Takeout Duplicate Review: 2007-08-12 Batch

Source report: `reports/scan-hash-v47.json`

## Summary

- duplicate groups: 1
- duplicate files: 2
- source folders: `/home/gabriel/Pictures/Photos/2007/08/12` and `/home/gabriel/Pictures/Photos/2007/2007-08-15--19.02.45`
- pattern: same-content duplicates split between the canonical dated folder and the timestamped import folder
- review goal: keep the canonical dated folder and quarantine the duplicate counterpart from the timestamped import folder
- inferred date consistency: both files infer to `2007-08-12` from `metadata`

## Recommendation

- keep: `/home/gabriel/Pictures/Photos/2007/08/12/DSCF0077.JPG`
- quarantine: `/home/gabriel/Pictures/Photos/2007/2007-08-15--19.02.45/DSCF0077.JPG`

## Group List

### dup-0003 | DSCF0077.JPG

- path: `/home/gabriel/Pictures/Photos/2007/08/12/DSCF0077.JPG`
  proposed: `Library/2007/2007-08-12_Pictures/DSCF0077.JPG`
  date source: `metadata`
- path: `/home/gabriel/Pictures/Photos/2007/2007-08-15--19.02.45/DSCF0077.JPG`
  proposed: `Library/2007/2007-08-12_2007-08-15--19.02.45/DSCF0077.JPG`
  date source: `metadata`
