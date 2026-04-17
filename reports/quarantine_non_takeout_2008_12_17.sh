#!/usr/bin/env bash
set -euo pipefail

QUARANTINE_ROOT="/home/gabriel/media-organizer-quarantine-2026-04-14/non-takeout-2008-12-17-batch"

FILES=(
  "/home/gabriel/Pictures/Photos/2008/12/17/dscf3577.jpg"
  "/home/gabriel/Pictures/Photos/2008/12/17/dscf3576.jpg"
  "/home/gabriel/Pictures/Photos/2008/12/17/dscf3572.jpg"
  "/home/gabriel/Pictures/Photos/2008/12/17/dscf3569.jpg"
  "/home/gabriel/Pictures/Photos/2008/12/17/dscf3575.jpg"
  "/home/gabriel/Pictures/Photos/2008/12/17/dscf3578.jpg"
  "/home/gabriel/Pictures/Photos/2008/12/17/dscf3567.jpg"
  "/home/gabriel/Pictures/Photos/2008/12/17/dscf3573.jpg"
  "/home/gabriel/Pictures/Photos/2008/12/17/dscf3564.jpg"
  "/home/gabriel/Pictures/Photos/2008/12/17/dscf3566.jpg"
  "/home/gabriel/Pictures/Photos/2008/12/17/dscf3571.jpg"
  "/home/gabriel/Pictures/Photos/2008/12/17/dscf3560.jpg"
  "/home/gabriel/Pictures/Photos/2008/12/17/dscf3568.jpg"
)

mkdir -p "$QUARANTINE_ROOT"

for src in "${FILES[@]}"; do
  dst="$QUARANTINE_ROOT$src"
  mkdir -p "$(dirname "$dst")"
  mv "$src" "$dst"
done
