# Final Review Package

Source report: `reports/scan-nohash-v15.json`

## Scan Summary

- total files: 49293
- images: 15186
- videos: 818
- sidecars: 4273
- caches: 27984
- unknown: 1032

## Planned Structure

- destination roots: App-Caches=27984, Library=15037, Exports=4273, Shared=946, Projects=30, ScreenRecordings=5
- main library shape: `Library/YYYY/YYYY-MM-DD_source/...`
- shared branches in use: `Shared/Jonel/...`, `Shared/Samyra/...`
- sidecars route to: `Exports/...`
- caches route to: `App-Caches/...`

## Priority Review Areas

- remaining suspicious planned destinations: 216
- remaining grouped mtime patterns: 119
- Google Photos folders: 37
- Google Photos received_* folders: 6
- Google Photos sidecar-only groups: 478
- focused 2014 Google Photos review matches: 111

## Top Remaining mtime Groups

- 92 files | /home/gabriel/Pictures/summer2014 | MVI_<digits>.MOV
- 10 files | /home/gabriel/Videos/Kali | Panantukan Silat Level <digits>.mp<digits>
- 8 files | /home/gabriel/Videos | IMG_<digits>.MOV
- 7 files | /home/gabriel/Pictures/Samyras 16 | MVI_<digits>.MOV
- 5 files | /home/gabriel/Pictures/Pictures from ates camera | MVI_<digits>.MOV
- 5 files | /home/gabriel/Pictures/temp | Pro <digits>_<digits>.png
- 4 files | /home/gabriel/Pictures/1903/12/31 | VIDEO_<digits>.mp<digits>
- 4 files | /home/gabriel/Videos/Kali | Hammer Defense Level <digits>.mp<digits>
- 3 files | /home/gabriel/Videos/JJ1999 | JJ<digits>.mp<digits>
- 2 files | /home/gabriel/Pictures/google-takeout/Takeout/Google Photos/Jonel 26 | received_<digits>.jpeg

## Top Google Photos Folders

- Photos from 2014 | media=1402 sidecars=746 edited=632 received=0
- Photos from 2022 | media=634 sidecars=634 edited=0 received=26
- Photos from 2021 | media=475 sidecars=448 edited=4 received=24
- Photos from 2018 | media=409 sidecars=402 edited=7 received=0
- Photos from 2017 | media=383 sidecars=383 edited=0 received=0
- Photos from 2024 | media=319 sidecars=319 edited=0 received=26
- Photos from 2015 | media=258 sidecars=173 edited=82 received=0
- Photos from 2019 | media=211 sidecars=211 edited=0 received=0
- Photos from 2013 | media=207 sidecars=121 edited=98 received=0
- Photos from 2025 | media=155 sidecars=155 edited=0 received=8

## Focused 2014 Review

- filtered dates: `2014-05-28`, `2014-06-21`, `2014-07-19`
- non-Takeout folder filter: `/home/gabriel/Pictures/20140723 and earlier`
- 2014-07-19 | IMG_20140719_142707.jpg | google=6 rest=1
- 2014-05-28 | IMG_20140528_122606939.jpg | google=4 rest=1
- 2014-05-28 | IMG_20140528_134205121.jpg | google=4 rest=1
- 2014-05-28 | IMG_20140528_134246903.jpg | google=4 rest=1
- 2014-05-28 | IMG_20140528_134552739.jpg | google=4 rest=1
- 2014-05-28 | IMG_20140528_151303201.jpg | google=4 rest=1
- 2014-05-28 | IMG_20140528_151348309.jpg | google=4 rest=1
- 2014-05-28 | IMG_20140528_151458777.jpg | google=4 rest=1
- 2014-05-28 | IMG_20140528_151642776.jpg | google=4 rest=1
- 2014-05-28 | IMG_20140528_151957763.jpg | google=4 rest=1

## Package Files

- `README.md`
- `mtime-summary.json`
- `suspicious-destinations.json`
- `google-photos-summary.json`
- `google-photos-received.json`
- `google-photos-sidecar-gaps.json`
- `google-photos-matches.json`
- `google-photos-2014-review.json`

