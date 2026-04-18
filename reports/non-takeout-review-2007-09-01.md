# Non-Takeout Duplicate Review: 2007-09-01 Batch

Source report: `reports/scan-hash-v50.json`

## Summary

- duplicate groups: 1
- duplicate files: 2
- source folders: `/home/gabriel/Pictures/Photos/2007/09/01` and `/home/gabriel/Pictures/Photos/2007/2007-09-06--17.41.40`
- pattern: same-content duplicates split between the canonical dated folder and the timestamped import folder
- review goal: keep the canonical dated folder and quarantine the duplicate counterpart from the timestamped import folder
- inferred date consistency: both files infer to `2007-08-31` from `metadata` even though one source folder is named `2007/09/01`

## Recommendation

- keep: `/home/gabriel/Pictures/Photos/2007/09/01/DSCF0545.JPG`
- quarantine: `/home/gabriel/Pictures/Photos/2007/2007-09-06--17.41.40/DSCF0545.JPG`

## Group List

### dup-0011 | DSCF0545.JPG

- path: `/home/gabriel/Pictures/Photos/2007/09/01/DSCF0545.JPG`
  proposed: `Library/2007/2007-08-31_Pictures/DSCF0545.JPG`
  date source: `metadata`
- path: `/home/gabriel/Pictures/Photos/2007/2007-09-06--17.41.40/DSCF0545.JPG`
  proposed: `Library/2007/2007-08-31_2007-09-06--17.41.40/DSCF0545.JPG`
  date source: `metadata`
