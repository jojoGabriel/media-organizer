# Manual Cleanup Checklist - 2026-04-14

Manual execution plan for the safe cleanup work already identified in the
project notes and manifests.

This is not a tool apply phase. Perform these actions manually outside the
organizer.

## Scope

Use these source artifacts:

- `CLEANUP_CANDIDATES_2026-04-11.md`
- `GOOGLE_PHOTOS_SAFE_DATES_2026-04-11.md`
- `SESSION_NOTES_2026-04-14.md`
- `reports/google-takeout-safe-pass-photos-from-2014-non-takeout-backed.txt`
- `reports/google-takeout-safe-pass-25th.txt`
- `reports/google-takeout-safe-pass-photos-from-2013.txt`
- `reports/google-takeout-safe-pass-failed-videos.txt`
- `reports/google-takeout-safe-pass-untitled-4.txt`
- `reports/google-takeout-safe-pass-untitled-4-edited.txt`
- `reports/google-takeout-safe-pass-untitled.txt`
- `reports/google-takeout-safe-pass-untitled-1.txt`
- `reports/google-takeout-safe-pass-untitled-2.txt`
- `reports/google-takeout-safe-pass-untitled-3.txt`
- `reports/google-takeout-safe-pass-photos-from-2015.txt`
- `reports/google-takeout-safe-pass-photos-from-2016.txt`
- `reports/google-takeout-safe-pass-starvedrock.txt`
- `reports/google-takeout-safe-pass-jab.txt`
- `reports/google-takeout-safe-pass-jojo-joy.txt`
- `reports/google-takeout-safe-pass-jonel-26-received.txt`
- `reports/google-takeout-safe-pass-wednesday-morning-in-chicago-edited.txt`
- `reports/google-takeout-safe-pass-trip-to-los-angeles-and-anaheim-edited.txt`
- `reports/google-takeout-safe-pass-weekend-in-fish-creek-edited.txt`
- `reports/google-takeout-safe-pass-weekend-in-niagara-falls-and-scarborough-edited.txt`
- `reports/google-takeout-safe-pass-memories-together-edited.txt`
- `reports/google-takeout-conditional-pass-memories-together-plain.txt`
- `reports/google-takeout-conditional-pass-jonel-26-plain.txt`
- `reports/google-takeout-conditional-pass-weekend-in-fish-creek-plain.txt`
- `reports/google-takeout-safe-pass-weekend-in-fish-creek-keep-overrides.txt`
- `reports/google-takeout-conditional-pass-weekend-in-niagara-falls-and-scarborough-plain.txt`
- `reports/google-takeout-safe-pass-weekend-in-niagara-falls-and-scarborough-overlay.txt`
- `reports/google-takeout-conditional-pass-wednesday-morning-in-chicago-plain.txt`
- `reports/google-takeout-conditional-pass-trip-to-los-angeles-and-anaheim-plain.txt`
- `reports/mackinac-safe-pass-plain.txt`

## Do First

- Make sure the canonical keeper copies still exist before deleting any
  duplicate Takeout files.
- Start with the smallest exact filename manifests before touching large folder
  deletes.
- Keep all actions reversible if possible.

## Safe To Execute Now

### Google Takeout exact filename manifests

Process these by deleting or otherwise removing the Takeout-side duplicate
copies named in each manifest:

- `reports/google-takeout-safe-pass-photos-from-2014-non-takeout-backed.txt`
- `reports/google-takeout-safe-pass-25th.txt`
- `reports/google-takeout-safe-pass-photos-from-2013.txt`
- `reports/google-takeout-safe-pass-failed-videos.txt`
- `reports/google-takeout-safe-pass-untitled-4.txt`
- `reports/google-takeout-safe-pass-untitled-4-edited.txt`
- `reports/google-takeout-safe-pass-untitled.txt`
- `reports/google-takeout-safe-pass-untitled-1.txt`
- `reports/google-takeout-safe-pass-untitled-2.txt`
- `reports/google-takeout-safe-pass-untitled-3.txt`
- `reports/google-takeout-safe-pass-photos-from-2015.txt`
- `reports/google-takeout-safe-pass-photos-from-2016.txt`
- `reports/google-takeout-safe-pass-starvedrock.txt`
- `reports/google-takeout-safe-pass-jab.txt`
- `reports/google-takeout-safe-pass-jojo-joy.txt`
- `reports/google-takeout-safe-pass-jonel-26-received.txt`
- `reports/google-takeout-safe-pass-wednesday-morning-in-chicago-edited.txt`
- `reports/google-takeout-safe-pass-trip-to-los-angeles-and-anaheim-edited.txt`
- `reports/google-takeout-safe-pass-weekend-in-fish-creek-edited.txt`
- `reports/google-takeout-safe-pass-weekend-in-niagara-falls-and-scarborough-edited.txt`
- `reports/google-takeout-safe-pass-memories-together-edited.txt`
- `reports/google-takeout-conditional-pass-memories-together-plain.txt`
- `reports/google-takeout-conditional-pass-jonel-26-plain.txt`
- `reports/google-takeout-conditional-pass-weekend-in-fish-creek-plain.txt`
- `reports/google-takeout-safe-pass-weekend-in-fish-creek-keep-overrides.txt`
- `reports/google-takeout-conditional-pass-weekend-in-niagara-falls-and-scarborough-plain.txt`
- `reports/google-takeout-safe-pass-weekend-in-niagara-falls-and-scarborough-overlay.txt`
- `reports/google-takeout-conditional-pass-wednesday-morning-in-chicago-plain.txt`
- `reports/google-takeout-conditional-pass-trip-to-los-angeles-and-anaheim-plain.txt`

### Mackinac exact filename manifest

Process these by removing the duplicate-side files from
`/home/gabriel/Pictures/mackinac/`:

- `reports/mackinac-safe-pass-plain.txt`

### Local duplicate cleanup candidates

Execute the clear safe deletions from `CLEANUP_CANDIDATES_2026-04-11.md`:

- `morePics` bulk numbered duplicates, `IMG142.jpg`, `IMG143.jpg`,
  `Thumbs.db`
- loose duplicate files in `/home/gabriel/Pictures/Photos`
- bad duplicate spillover in `/home/gabriel/Pictures/1903/12/31`
- `.wdmc` cache content in the bad `1903` bucket
- `Screenshots` junk files and `.wdmc` cache content
- the clearly marked duplicate mirror folders under `Photos/2006`,
  `Photos/2007`, `Photos/2008`, and `Photos/2009`

## Keep

Do not remove these items from `Weekend in Fish Creek`:

- `IMG_20140719_165758-SMILE.jpg`
- `IMG_20140719_190437-MOTION.gif`

## Still Deferred

Do not act on these yet unless reviewed explicitly:

- all `-edited` Google Photos items
- all `received_*` Google Photos items
- all `metadata.json` Takeout folder metadata files
- sidecar-gap-heavy cases
- anything marked "keep for now" or "manual review" in
  `CLEANUP_CANDIDATES_2026-04-11.md`

## Order Of Operations

1. Execute the small exact Takeout manifests first.
2. Execute the four reviewed mixed-folder plain manifests.
3. Execute the other larger safe Takeout manifests.
4. Execute the local non-Takeout duplicate cleanup candidates.
5. Execute the `mackinac` exact manifest.
6. Stop.
7. Rerun a fresh hashed scan before making any new organizer decisions.

## After Cleanup

Run a new hashed scan and write a new report version. Use that fresh report as
the new baseline for any further duplicate or destination review.
