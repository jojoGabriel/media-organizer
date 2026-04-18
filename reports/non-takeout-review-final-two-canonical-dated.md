# Non-Takeout Duplicate Review: Final Canonical Dated-Folder Pairs

Source report: `reports/scan-hash-v60.json`

## Summary

- duplicate groups: 2
- duplicate files: 4
- rule applied: prefer the canonical dated folder under `Pictures/YYYY/MM/DD`
- review goal: keep the dated-folder copy and quarantine the `Photos/...` counterpart in both remaining groups

## Group 1

- keep: `/home/gabriel/Pictures/2002/09/30/fl000001.jpg`
- quarantine: `/home/gabriel/Pictures/Photos/2009/01/28/fl000001.jpg`
- inferred date consistency: both files infer to `2002-09-30` from `metadata`
- planned destination consistency: both files plan to `Library/2002/2002-09-30_Pictures/fl000001.jpg`

## Group 2

- keep: `/home/gabriel/Pictures/2008/04/18/DSCF1458.JPG`
- quarantine: `/home/gabriel/Pictures/Photos/2008/2008-04-20--18.53.11/DSCF1458.JPG`
- inferred date consistency: both files infer to `2008-04-18` from `metadata`
- planned destination difference: the dated-folder copy plans to `Library/2008/2008-04-18_Pictures/DSCF1458.JPG`, while the timestamped import copy plans to `Library/2008/2008-04-18_2008-04-20--18.53.11/DSCF1458.JPG`

## Rationale

- both groups are exact duplicate groups from the hashed scan report
- the selected rule is to prefer the dated canonical folder
- that makes the `Photos/...` side the quarantine side in both cases
