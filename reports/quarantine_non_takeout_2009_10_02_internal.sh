#!/usr/bin/env bash
set -euo pipefail

QUARANTINE_ROOT="/home/gabriel/media-organizer-quarantine-2026-04-14/non-takeout-2009-10-02-internal-batch"

FILES=(
  "/home/gabriel/Pictures/Photos/2009/10/02/dscf6043-1.jpg"
  "/home/gabriel/Pictures/Photos/2009/10/02/dscf6043-2.jpg"
)

mkdir -p "$QUARANTINE_ROOT"

for src in "${FILES[@]}"; do
  dst="$QUARANTINE_ROOT$src"
  mkdir -p "$(dirname "$dst")"
  mv "$src" "$dst"
done
