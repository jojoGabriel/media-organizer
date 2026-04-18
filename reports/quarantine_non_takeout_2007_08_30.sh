#!/usr/bin/env bash
set -euo pipefail

QUARANTINE_ROOT="/home/gabriel/media-organizer-quarantine-2026-04-14/non-takeout-2007-08-30-batch"

FILES=(
  "/home/gabriel/Pictures/Photos/2007/2007-09-06--17.41.40/DSCF0541.JPG"
  "/home/gabriel/Pictures/Photos/2007/2007-09-06--17.41.40/DSCF0543.JPG"
)

mkdir -p "$QUARANTINE_ROOT"

for src in "${FILES[@]}"; do
  dst="$QUARANTINE_ROOT$src"
  mkdir -p "$(dirname "$dst")"
  mv "$src" "$dst"
done
