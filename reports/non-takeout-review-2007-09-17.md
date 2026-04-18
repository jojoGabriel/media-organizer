# Non-Takeout Duplicate Review: 2007-09-17 Batch

Source report: `reports/scan-hash-v46.json`

## Summary

- duplicate groups: 1
- duplicate files: 2
- source folders: `/home/gabriel/Pictures/2007/09/17` and `/home/gabriel/Pictures/Photos/2007/2007-11-03--17.02.27`
- pattern: same-content duplicates split between the canonical dated folder and the timestamped import folder
- review goal: keep the canonical dated folder and quarantine the duplicate counterpart from the timestamped import folder
- inferred date consistency: both files infer to `2007-09-17` from `metadata`

## Recommendation

- keep: `/home/gabriel/Pictures/2007/09/17/DSCF0595.JPG`
- quarantine: `/home/gabriel/Pictures/Photos/2007/2007-11-03--17.02.27/DSCF0595.JPG`

## Group List

### dup-0001 | DSCF0595.JPG

- path: `/home/gabriel/Pictures/2007/09/17/DSCF0595.JPG`
  proposed: `Library/2007/2007-09-17_Pictures/DSCF0595.JPG`
  date source: `metadata`
- path: `/home/gabriel/Pictures/Photos/2007/2007-11-03--17.02.27/DSCF0595.JPG`
  proposed: `Library/2007/2007-09-17_2007-11-03--17.02.27/DSCF0595.JPG`
  date source: `metadata`
