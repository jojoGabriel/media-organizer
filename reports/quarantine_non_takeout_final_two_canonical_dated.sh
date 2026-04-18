#!/usr/bin/env bash
set -euo pipefail

QUARANTINE_ROOT="/home/gabriel/media-organizer-quarantine-2026-04-14/non-takeout-final-two-canonical-dated-batch"

FILES=(
  "/home/gabriel/Pictures/Photos/2009/01/28/fl000001.jpg"
  "/home/gabriel/Pictures/Photos/2008/2008-04-20--18.53.11/DSCF1458.JPG"
)

mkdir -p "$QUARANTINE_ROOT"

for src in "${FILES[@]}"; do
  dst="$QUARANTINE_ROOT$src"
  mkdir -p "$(dirname "$dst")"
  mv "$src" "$dst"
done
