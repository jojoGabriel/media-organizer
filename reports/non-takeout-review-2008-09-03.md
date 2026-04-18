# Non-Takeout Duplicate Review: 2008-09-03 Batch

Source report: `reports/scan-hash-v44.json`

## Summary

- duplicate groups: 1
- duplicate files: 2
- source folders: `/home/gabriel/Pictures/2008/09/03` and `/home/gabriel/Pictures/Photos/2008/09/03`
- pattern: same-content duplicates split between the canonical dated folder and the mirrored `Photos` dated folder
- review goal: keep the canonical dated folder and quarantine the duplicate counterpart from the mirrored `Photos` folder
- inferred date consistency: both files infer to `2008-09-03` from `path`

## Recommendation

- keep: `/home/gabriel/Pictures/2008/09/03/pic-0519.jpg`
- quarantine: `/home/gabriel/Pictures/Photos/2008/09/03/pic-0519.jpg`

## Group List

### dup-0001 | pic-0519.jpg

- path: `/home/gabriel/Pictures/2008/09/03/pic-0519.jpg`
  proposed: `Library/2008/2008-09-03_Pictures/pic-0519.jpg`
  date source: `path`
- path: `/home/gabriel/Pictures/Photos/2008/09/03/pic-0519.jpg`
  proposed: `Library/2008/2008-09-03_Pictures/pic-0519.jpg`
  date source: `path`
