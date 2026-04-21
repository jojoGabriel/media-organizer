# Next Steps (v81)

Current verified baseline:

- `reports/scan-hash-v81-post-conflicts.json`
- `reports/apply-manifest-v81-post-conflicts.json` (`0` apply operations)

## What To Back Up Now

Keep these as separate backup roots:

- `/home/gabriel/Pictures`
- `/home/gabriel/Videos`
- `/home/gabriel/organized-media-dry-run`
- `/home/gabriel/media-organizer-quarantine-2026-04-14`
- `/home/gabriel/Projects/media-organizer`

Reason:

- `Pictures` and `Videos` are still your active source trees.
- `organized-media-dry-run` is your consolidated target state.
- quarantine is still a protected holding area.
- repo contains decisions, manifests, and reproducible tooling.

## Current Library Reality

From `v81` scan:

- `Pictures`: `36,857` files (`4,454` images, `164` videos, `4,260` sidecars, `27,962` cache, `17` unknown)
- `Videos`: `31,827` files (`1` video, `3,855` sidecars, `27,962` cache, `9` unknown)
- unknown tail (`26` files) is mostly project/docs (`.kdenlive`, `.pdf`, `.xcf`, `.phd`), not junk

Interpretation:

- the planner/apply move phase is complete
- remaining work is policy cleanup and structure simplification

## Quarantine: What Can Be Done Safely

Current quarantine state:

- `/home/gabriel/media-organizer-quarantine-2026-04-14`
- `2,369` files, about `5.72 GB`
- mostly `.jpg` and `.mp4` in dated batch folders

Safe next actions:

1. Keep quarantine as read-only archive for now (no bulk delete).
2. Build a hash-compare report:
   - classify quarantine files into:
     - already represented in `organized-media-dry-run`
     - unique to quarantine
3. Only after that report:
   - move quarantine duplicates into a `ready-to-delete` list
   - keep unique quarantine files in place (or migrate to `Archive/Quarantine-Unique/`)

## Naming Fix For Target Library

`organized-media-dry-run` is now misleading because real moves were executed.

Recommended rename (after backup):

- from: `/home/gabriel/organized-media-dry-run`
- to: `/home/gabriel/organized-media-v1`

Optional compatibility symlink:

- `organized-media-dry-run -> organized-media-v1`

This keeps existing scripts working while making the folder intent clear.
