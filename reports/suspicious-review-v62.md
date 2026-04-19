# Suspicious Destination Review - v62

Review source:

- `reports/scan-hash-v62.json`
- `reports/final-review-v62/suspicious-destinations.json`

This review covers the `15` remaining suspicious planned destinations. These
are not duplicate problems. They are planner cases where the proposed
`Library/YYYY/YYYY-MM-DD_source/...` path is based on `mtime` and may not match
the real organizer intent.

## Recommended disposition by folder

### Pexels

Case:

- `/home/gabriel/Pictures/Pexels/pexels-cottonbro-5876759.jpg`

Current proposal:

- `Library/2022/2022-01-12_Pexels/pexels-cottonbro-5876759.jpg`

Recommendation:

- keep this out of the date-bucket library review for now
- treat `Pexels/` as a likely downloads/reference folder rather than personal
  camera chronology

Reason:

- the filename carries no organizer date
- the only date is `mtime`
- the folder name strongly suggests stock/download source semantics

### Screenshots

Cases:

- `/home/gabriel/Pictures/Screenshots/Screenshot (1).png`
- `/home/gabriel/Pictures/Screenshots/problem.jpg`

Current proposal:

- `Library/2014/2014-06-17_Screenshots/...`

Recommendation:

- keep these in manual review
- do not treat `2014-06-17` as trustworthy event date
- if a future planner exception is added, `Screenshots/` should probably route
  outside the dated personal-photo library

Reason:

- these names do not encode capture date
- neighboring files in the same folder include explicit desktop screenshot
  naming patterns, which supports a utility/screenshots bucket rather than a
  personal event bucket

### Wallpapers

Cases:

- `/home/gabriel/Pictures/Wallpapers/NayTay.png`
- `/home/gabriel/Pictures/Wallpapers/lola1.jpg`

Current proposal:

- `Library/2020/2020-04-12_Wallpapers/...`
- `Library/2015/2015-06-27_Wallpapers/...`

Recommendation:

- treat `Wallpapers/` as a non-library bucket
- keep current `mtime` dates as weak reference only

Reason:

- the folder intent is explicit
- wallpapers are typically assets or reference images, not dated photo events

### googleEarth

Case:

- `/home/gabriel/Pictures/googleEarth/joy house.png`

Current proposal:

- `Library/2021/2021-07-14_googleEarth/joy house.png`

Recommendation:

- likely safe to treat the `mtime` date as meaningful here
- if this folder gets a planner exception, move the whole `googleEarth/`
  folder as a utility/reference bucket instead of a dated photo bucket

Reason:

- neighboring files are named `Screenshot from 2021-07-14 ...` and
  `Screenshot from 2021-07-15 ...`
- the flagged file mtime `2021-07-14` is consistent with that cluster
- the suspiciousness is more about destination shape than incorrect date

### Loose-root image

Case:

- `/home/gabriel/Pictures/joy.png`

Current proposal:

- `Library/2016/2016-06-10_Pictures/joy.png`

Recommendation:

- keep in manual review
- avoid using `Pictures` as a final source label
- this needs either a specific destination override or a human decision on
  whether it belongs in a reference/misc bucket

Reason:

- both the date and source label are weak
- this is the clearest example where the fallback `root folder` label is not a
  good organizer result

### morePics survivors

Cases:

- `/home/gabriel/Pictures/morePics/Gary and Mom.jpg`
- `/home/gabriel/Pictures/morePics/Lola 000529.jpg`
- `/home/gabriel/Pictures/morePics/Lola 081099 Back.jpg`
- `/home/gabriel/Pictures/morePics/Lola 081099 Front.jpg`
- `/home/gabriel/Pictures/morePics/Lola 082299.jpg`
- `/home/gabriel/Pictures/morePics/j01.jpg`
- `/home/gabriel/Pictures/morePics/j02.jpg`

Current proposal:

- dated `Library/..._morePics/...` buckets based on `mtime`

Recommendation:

- keep all of these in manual review
- do not trust the current `mtime` dates as organizer dates
- use these as the first candidates for either:
  - manual dating and relabeling, or
  - a future `Scans` / `Family-Scans` / `Reference-Photos` style bucket if
    exact dates cannot be recovered

Reason:

- the folder was already flagged earlier as a manual-review hold area
- filenames such as `Lola 081099 Back.jpg` and `Lola 081099 Front.jpg`
  strongly imply older scan/photo dates not represented by current mtimes
- these are likely scanned legacy photos rather than 2011-2012 captures

### Loose-root video

Case:

- `/home/gabriel/Videos/cs50w-project1.mp4`

Current proposal:

- `Library/2019/2019-09-16_Videos/cs50w-project1.mp4`

Recommendation:

- do not keep this in the dated media library
- treat it as a project/output candidate
- add it to a future project-routing review rather than a photo-date review

Reason:

- the filename clearly looks like a coursework or project artifact
- the weak `Videos` source label is a fallback, not meaningful organizer intent

## Recommended next organizer step

The cleanest next pass after this review is:

1. manually classify these suspicious cases into:
   - reference/download buckets
   - project/output buckets
   - legacy scanned-photo buckets
2. only after that, consider adding planner exceptions for the folder classes
   that are now clearly not part of the dated personal-photo library:
   - `Pexels`
   - `Screenshots`
   - `Wallpapers`
   - `googleEarth`
3. keep `morePics`, `joy.png`, and `cs50w-project1.mp4` as explicit manual
   decisions rather than automatic date-bucket moves

## Outcome

No duplicate cleanup action is needed here.

The main result of this review is that the suspicious set is small, bounded,
and mostly explained by fallback planner behavior rather than hidden duplicate
or safety issues.
