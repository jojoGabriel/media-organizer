#!/usr/bin/env bash
set -euo pipefail

QUARANTINE_ROOT="/home/gabriel/media-organizer-quarantine-2026-04-14/non-takeout-tito-osias-2014-08-31-batch"

FILES=(
  "/home/gabriel/Pictures/2014/08/31/IMG_20140831_141344.jpg"
  "/home/gabriel/Pictures/2014/08/31/IMG_20140831_141318.jpg"
  "/home/gabriel/Pictures/2014/08/31/IMG_20140831_141653.jpg"
  "/home/gabriel/Pictures/2014/08/31/IMG_20140831_143206.jpg"
  "/home/gabriel/Pictures/2014/08/31/IMG_20140831_141607.jpg"
  "/home/gabriel/Pictures/2014/08/31/IMG_20140831_140532.jpg"
  "/home/gabriel/Pictures/2014/08/31/IMG_20140831_141155.jpg"
  "/home/gabriel/Pictures/2014/08/31/IMG_20140831_141142.jpg"
)

mkdir -p "$QUARANTINE_ROOT"

for src in "${FILES[@]}"; do
  dst="$QUARANTINE_ROOT$src"
  mkdir -p "$(dirname "$dst")"
  mv "$src" "$dst"
done
