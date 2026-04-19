# Final Review Package

Source report: `reports/scan-hash-v70-post-verify.json`

## Scan Summary

- total files: 74693
- images: 8940
- videos: 339
- sidecars: 8115
- caches: 55924
- unknown: 1375

## Planned Structure

- destination roots: App-Caches=55387, Library=9134, Exports=8115, Projects=633, Reference=506, Shared=163
- main library shape: `Library/YYYY/YYYY-MM-DD_source/...`
- shared branches in use: `Shared/Jonel/...`, `Shared/Samyra/...`
- sidecars route to: `Exports/...`
- caches route to: `App-Caches/...`

## Priority Review Areas

- remaining suspicious planned destinations: 88
- remaining grouped mtime patterns: 34
- Google Photos folders: 36
- Google Photos received_* folders: 6
- Google Photos sidecar-only groups: 732
- focused 2014 Google Photos review matches: 0

## Top Remaining mtime Groups

- 65 files | /home/gabriel/Videos/Pictures/nanay80 | <digits>_<digits>_<digits>_n.jpg
- 2 files | /home/gabriel/Videos/Pictures/morePics | j<digits>.jpg
- 2 files | /home/gabriel/Videos/Pictures/morePics | Lola <digits>.jpg
- 2 files | /home/gabriel/Videos/Pictures/nanay80 | B<digits>.jpg
- 2 files | /home/gabriel/Videos/Pictures/nanay80 | C<digits>.jpg
- 2 files | /home/gabriel/Videos/Pictures/nanay80 | E<digits>.jpg
- 1 files | /home/gabriel/Videos/Pictures | joy.png
- 1 files | /home/gabriel/Videos/Pictures/ceu | beed<digits>a.jpg
- 1 files | /home/gabriel/Videos/Pictures/ceu | bukid.jpg
- 1 files | /home/gabriel/Videos/Pictures/ceu | classroom.jpg

## Top Google Photos Folders

- Photos from 2014 | media=1098 sidecars=746 edited=632 received=0
- Photos from 2022 | media=634 sidecars=634 edited=0 received=26
- Photos from 2021 | media=475 sidecars=448 edited=4 received=24
- Photos from 2018 | media=409 sidecars=402 edited=7 received=0
- Photos from 2017 | media=383 sidecars=383 edited=0 received=0
- Photos from 2024 | media=319 sidecars=319 edited=0 received=26
- Photos from 2019 | media=211 sidecars=211 edited=0 received=0
- Photos from 2013 | media=205 sidecars=121 edited=98 received=0
- Photos from 2025 | media=155 sidecars=155 edited=0 received=8
- Photos from 2015 | media=138 sidecars=173 edited=82 received=0

## Focused 2014 Review

- filtered dates: `2014-05-28`, `2014-06-21`, `2014-07-19`
- non-Takeout folder filter: `/home/gabriel/Pictures/20140723 and earlier`

## Package Files

- `README.md`
- `mtime-summary.json`
- `suspicious-destinations.json`
- `google-photos-summary.json`
- `google-photos-received.json`
- `google-photos-sidecar-gaps.json`
- `google-photos-matches.json`
- `google-photos-2014-review.json`

