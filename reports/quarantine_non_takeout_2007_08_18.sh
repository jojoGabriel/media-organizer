#!/usr/bin/env bash
set -euo pipefail

QUARANTINE_ROOT="/home/gabriel/media-organizer-quarantine-2026-04-14/non-takeout-2007-08-18-batch"

FILES=(
  "/home/gabriel/Pictures/Photos/2007/2007-08-26--15.46.09/DSCF0258.JPG"
  "/home/gabriel/Pictures/Photos/2007/2007-08-26--15.46.09/DSCF0264.JPG"
  "/home/gabriel/Pictures/Photos/2007/2007-08-26--15.46.09/DSCF0265.JPG"
  "/home/gabriel/Pictures/Photos/2007/2007-08-26--15.46.09/DSCF0260.JPG"
  "/home/gabriel/Pictures/Photos/2007/2007-08-26--15.46.09/DSCF0263.JPG"
  "/home/gabriel/Pictures/Photos/2007/2007-08-26--15.46.09/DSCF0259.JPG"
)

mkdir -p "$QUARANTINE_ROOT"

for src in "${FILES[@]}"; do
  dst="$QUARANTINE_ROOT$src"
  mkdir -p "$(dirname "$dst")"
  mv "$src" "$dst"
done
