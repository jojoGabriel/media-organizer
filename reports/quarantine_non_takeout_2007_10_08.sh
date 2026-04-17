#!/usr/bin/env bash
set -euo pipefail

QUARANTINE_ROOT="/home/gabriel/media-organizer-quarantine-2026-04-14/non-takeout-2007-10-08-batch"

FILES=(
  "/home/gabriel/Pictures/Photos/2007/2007-11-03--17.02.27/DSCF0676.JPG"
  "/home/gabriel/Pictures/Photos/2007/2007-11-03--17.02.27/DSCF0662.JPG"
  "/home/gabriel/Pictures/Photos/2007/2007-11-03--17.02.27/DSCF0677.JPG"
)

mkdir -p "$QUARANTINE_ROOT"

for src in "${FILES[@]}"; do
  dst="$QUARANTINE_ROOT$src"
  mkdir -p "$(dirname "$dst")"
  mv "$src" "$dst"
done
