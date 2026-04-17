#!/usr/bin/env bash
set -euo pipefail

QUARANTINE_ROOT="/home/gabriel/media-organizer-quarantine-2026-04-14/non-takeout-2008-04-19-batch"

FILES=(
  "/home/gabriel/Pictures/Photos/2008/2008-04-20--18.53.11/DSCF1462.JPG"
  "/home/gabriel/Pictures/Photos/2008/2008-04-20--18.53.11/DSCF1477.JPG"
  "/home/gabriel/Pictures/Photos/2008/2008-04-20--18.53.11/DSCF1472.JPG"
  "/home/gabriel/Pictures/Photos/2008/2008-04-20--18.53.11/DSCF1463.JPG"
  "/home/gabriel/Pictures/Photos/2008/2008-04-20--18.53.11/DSCF1476.JPG"
  "/home/gabriel/Pictures/Photos/2008/2008-04-20--18.53.11/DSCF1461.JPG"
  "/home/gabriel/Pictures/Photos/2008/2008-04-20--18.53.11/DSCF1467.JPG"
  "/home/gabriel/Pictures/Photos/2008/2008-04-20--18.53.11/DSCF1471.JPG"
  "/home/gabriel/Pictures/Photos/2008/2008-04-20--18.53.11/DSCF1466.JPG"
  "/home/gabriel/Pictures/Photos/2008/2008-04-20--18.53.11/DSCF1469.JPG"
  "/home/gabriel/Pictures/Photos/2008/2008-04-20--18.53.11/DSCF1474.JPG"
  "/home/gabriel/Pictures/Photos/2008/2008-04-20--18.53.11/DSCF1468.JPG"
  "/home/gabriel/Pictures/Photos/2008/2008-04-20--18.53.11/DSCF1465.JPG"
  "/home/gabriel/Pictures/Photos/2008/2008-04-20--18.53.11/DSCF1464.JPG"
  "/home/gabriel/Pictures/Photos/2008/2008-04-20--18.53.11/DSCF1475.JPG"
)

mkdir -p "$QUARANTINE_ROOT"

for src in "${FILES[@]}"; do
  dst="$QUARANTINE_ROOT$src"
  mkdir -p "$(dirname "$dst")"
  mv "$src" "$dst"
done
