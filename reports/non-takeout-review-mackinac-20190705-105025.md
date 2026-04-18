# Non-Takeout Duplicate Review: Mackinac 20190705_105025 Group

Source report: `reports/scan-hash-v59.json`

## Summary

- duplicate groups: 1
- duplicate files: 3
- source paths:
  - `/home/gabriel/Pictures/2019/07/05/20190705_105025(1).jpg`
  - `/home/gabriel/Pictures/mackinac/20190705_105025(1).jpg`
  - `/home/gabriel/Pictures/mackinac/20190705_105025.jpg`
- pattern: exact duplicate content split across one dated-folder copy and two `(...)(1)` suffixed copies, with one unsuffixed base filename present in the `mackinac` folder
- review goal: keep the unsuffixed filename as canonical and quarantine both suffixed duplicate counterparts
- inferred date consistency: all 3 files infer to `2019-07-05` from `filename`

## Recommendation

- keep: `/home/gabriel/Pictures/mackinac/20190705_105025.jpg`
- quarantine:
  - `/home/gabriel/Pictures/2019/07/05/20190705_105025(1).jpg`
  - `/home/gabriel/Pictures/mackinac/20190705_105025(1).jpg`

## Rationale

- the user explicitly chose the unsuffixed filename as canonical
- both suffixed `(...)(1)` copies are exact duplicates of the unsuffixed base file
- that rule resolves the otherwise conflicting folder-versus-filename ambiguity in this group

## Group List

### dup-0001 | 20190705_105025 family

- path: `/home/gabriel/Pictures/mackinac/20190705_105025.jpg`
  proposed: `Library/2019/2019-07-05_mackinac/20190705_105025.jpg`
  date source: `filename`
- path: `/home/gabriel/Pictures/2019/07/05/20190705_105025(1).jpg`
  proposed: `Library/2019/2019-07-05_Pictures/20190705_105025(1).jpg`
  date source: `filename`
- path: `/home/gabriel/Pictures/mackinac/20190705_105025(1).jpg`
  proposed: `Library/2019/2019-07-05_mackinac/20190705_105025(1).jpg`
  date source: `filename`
