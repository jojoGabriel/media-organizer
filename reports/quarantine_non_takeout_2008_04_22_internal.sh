#!/usr/bin/env bash
set -euo pipefail

QUARANTINE_ROOT="/home/gabriel/media-organizer-quarantine-2026-04-14/non-takeout-2008-04-22-internal-batch"

FILES=(
  "/home/gabriel/Pictures/Photos/2008/04/22/dscf1516-1.jpg"
  "/home/gabriel/Pictures/Photos/2008/04/22/dscf1518-1.jpg"
  "/home/gabriel/Pictures/Photos/2008/04/22/dscf1515-1.jpg"
  "/home/gabriel/Pictures/Photos/2008/04/22/dscf1494-1.jpg"
  "/home/gabriel/Pictures/Photos/2008/04/22/dscf1517-1.jpg"
  "/home/gabriel/Pictures/Photos/2008/04/22/dscf1507-1.jpg"
  "/home/gabriel/Pictures/Photos/2008/04/22/dscf1500-1.jpg"
  "/home/gabriel/Pictures/Photos/2008/04/22/dscf1510-1.jpg"
  "/home/gabriel/Pictures/Photos/2008/04/22/dscf1496-1.jpg"
  "/home/gabriel/Pictures/Photos/2008/04/22/dscf1498-1.jpg"
)

mkdir -p "$QUARANTINE_ROOT"

for src in "${FILES[@]}"; do
  dst="$QUARANTINE_ROOT$src"
  mkdir -p "$(dirname "$dst")"
  mv "$src" "$dst"
done
