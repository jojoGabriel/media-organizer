#!/usr/bin/env bash
set -euo pipefail

QUARANTINE_ROOT="/home/gabriel/media-organizer-quarantine-2026-04-14/non-takeout-2007-10-06-batch"

FILES=(
  "/home/gabriel/Pictures/Photos/2007/2007-11-03--17.02.27/DSCF0650.JPG"
  "/home/gabriel/Pictures/Photos/2007/2007-11-03--17.02.27/DSCF0649.JPG"
  "/home/gabriel/Pictures/Photos/2007/2007-11-03--17.02.27/DSCF0645.JPG"
  "/home/gabriel/Pictures/Photos/2007/2007-11-03--17.02.27/DSCF0648.JPG"
  "/home/gabriel/Pictures/Photos/2007/2007-11-03--17.02.27/DSCF0646.JPG"
  "/home/gabriel/Pictures/Photos/2007/2007-11-03--17.02.27/DSCF0647.JPG"
)

mkdir -p "$QUARANTINE_ROOT"

for src in "${FILES[@]}"; do
  dst="$QUARANTINE_ROOT$src"
  mkdir -p "$(dirname "$dst")"
  mv "$src" "$dst"
done
