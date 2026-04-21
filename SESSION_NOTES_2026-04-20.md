# Session Notes - 2026-04-20

## Baseline closeout

Post-conflict baseline established with:

- `reports/scan-hash-v81-post-conflicts.json`
- `reports/apply-manifest-v81-post-conflicts.json`

Verification result:

- `Built 0 apply operations and skipped 68684 files`

Interpretation:

- under current planner/apply rules, there are no pending organizer moves

## Conflict pair review decisions

Source of conflicts:

- `reports/apply-log-v80-execute.json`
- `reports/conflict-resolution-v80.json`

Manual image-pair review was completed for the `8` `_SRC-CONFLICT` pairs in:

- `/home/gabriel/organized-media-dry-run/Library/2007/...`

Decision summary:

- `7` pairs were pixel-identical (metadata-only file differences)
  - action: keep canonical destination file and delete `_SRC-CONFLICT` copy
- `1` pair (`DSCF0920`) was not pixel-identical even after rotation checks
  - action: keep both files for later manual content selection

## Scanner and test updates

Code updates made in this session:

- `media_organizer/config.py`
  - added `.wmv` and `.flv` to recognized video extensions
- `media_organizer/scanner.py`
  - classify PhotoDirector `*_cache` payloads as `cache`
  - preserve destination mapping for files already under structured roots
    (`Projects/`, `Reference/`, `Shared/`, `Library/`, `App-Caches/`, `Exports/`, `ScreenRecordings/`)
- `tests/test_scanner.py`
  - regression tests for the above classification and destination behaviors

Test status:

- `python3 -m unittest tests.test_scanner`
- `Ran 68 tests` / `OK`
