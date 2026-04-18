# Non-Takeout Duplicate Review: Jonel / Ates Camera Copy-Folder Pair

Source report: `reports/scan-hash-v58.json`

## Summary

- duplicate groups: 1
- duplicate files: 2
- source folders:
  - `/home/gabriel/Pictures/Pictures from ates camera/199_0510`
  - `/home/gabriel/Pictures/Pictures from ates camera/199_0510 - Copy`
- pattern: exact duplicate file split between the base folder and an explicit ` - Copy` folder
- review goal: keep the base folder copy and quarantine the explicit copy-folder duplicate
- merged context: this folder is treated as part of the `Jonel` bucket
- inferred date consistency: both files infer to `2014-05-10` from `metadata`

## Recommendation

- keep: `/home/gabriel/Pictures/Pictures from ates camera/199_0510/IMG_0438.JPG`
- quarantine: `/home/gabriel/Pictures/Pictures from ates camera/199_0510 - Copy/IMG_0438.JPG`

## Rationale

- both files plan to the same `Shared/Jonel/2014/2014-05-10_Jonel/IMG_0438.JPG` destination
- the only distinction is the explicit ` - Copy` folder suffix
- within the merged `Jonel` context, the non-copy folder is the cleaner canonical keep side

## Group List

### dup-0003 | IMG_0438.JPG

- path: `/home/gabriel/Pictures/Pictures from ates camera/199_0510/IMG_0438.JPG`
  proposed: `Shared/Jonel/2014/2014-05-10_Jonel/IMG_0438.JPG`
  date source: `metadata`
- path: `/home/gabriel/Pictures/Pictures from ates camera/199_0510 - Copy/IMG_0438.JPG`
  proposed: `Shared/Jonel/2014/2014-05-10_Jonel/IMG_0438.JPG`
  date source: `metadata`
