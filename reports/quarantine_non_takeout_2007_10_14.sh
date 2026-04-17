#!/usr/bin/env bash
set -euo pipefail

QUARANTINE_ROOT="/home/gabriel/media-organizer-quarantine-2026-04-14/non-takeout-2007-10-14-batch"

FILES=(
  "/home/gabriel/Pictures/Photos/2007/2007-11-03--17.02.27/DSCF0689.JPG"
  "/home/gabriel/Pictures/Photos/2007/2007-11-03--17.02.27/DSCF0702.JPG"
  "/home/gabriel/Pictures/Photos/2007/2007-11-03--17.02.27/DSCF0679.JPG"
  "/home/gabriel/Pictures/Photos/2007/2007-11-03--17.02.27/DSCF0690.JPG"
  "/home/gabriel/Pictures/Photos/2007/2007-11-03--17.02.27/DSCF0705.JPG"
  "/home/gabriel/Pictures/Photos/2007/2007-11-03--17.02.27/DSCF0701.JPG"
  "/home/gabriel/Pictures/Photos/2007/2007-11-03--17.02.27/DSCF0685.JPG"
  "/home/gabriel/Pictures/Photos/2007/2007-11-03--17.02.27/DSCF0708.JPG"
  "/home/gabriel/Pictures/Photos/2007/2007-11-03--17.02.27/DSCF0703.JPG"
  "/home/gabriel/Pictures/Photos/2007/2007-11-03--17.02.27/DSCF0695.JPG"
  "/home/gabriel/Pictures/Photos/2007/2007-11-03--17.02.27/DSCF0692.JPG"
  "/home/gabriel/Pictures/Photos/2007/2007-11-03--17.02.27/DSCF0696.JPG"
  "/home/gabriel/Pictures/Photos/2007/2007-11-03--17.02.27/DSCF0686.JPG"
  "/home/gabriel/Pictures/Photos/2007/2007-11-03--17.02.27/DSCF0681.JPG"
  "/home/gabriel/Pictures/Photos/2007/2007-11-03--17.02.27/DSCF0687.JPG"
  "/home/gabriel/Pictures/Photos/2007/2007-11-03--17.02.27/DSCF0682.JPG"
  "/home/gabriel/Pictures/Photos/2007/2007-11-03--17.02.27/DSCF0706.JPG"
  "/home/gabriel/Pictures/Photos/2007/2007-11-03--17.02.27/DSCF0707.JPG"
  "/home/gabriel/Pictures/Photos/2007/2007-11-03--17.02.27/DSCF0688.JPG"
  "/home/gabriel/Pictures/Photos/2007/2007-11-03--17.02.27/DSCF0700.JPG"
  "/home/gabriel/Pictures/Photos/2007/2007-11-03--17.02.27/DSCF0704.JPG"
  "/home/gabriel/Pictures/Photos/2007/2007-11-03--17.02.27/DSCF0698.JPG"
  "/home/gabriel/Pictures/Photos/2007/2007-11-03--17.02.27/DSCF0699.JPG"
  "/home/gabriel/Pictures/Photos/2007/2007-11-03--17.02.27/DSCF0693.JPG"
  "/home/gabriel/Pictures/Photos/2007/2007-11-03--17.02.27/DSCF0680.JPG"
  "/home/gabriel/Pictures/Photos/2007/2007-11-03--17.02.27/DSCF0694.JPG"
)

mkdir -p "$QUARANTINE_ROOT"

for src in "${FILES[@]}"; do
  dst="$QUARANTINE_ROOT$src"
  mkdir -p "$(dirname "$dst")"
  mv "$src" "$dst"
done
