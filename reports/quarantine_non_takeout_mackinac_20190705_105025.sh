#!/usr/bin/env bash
set -euo pipefail

QUARANTINE_ROOT="/home/gabriel/media-organizer-quarantine-2026-04-14/non-takeout-mackinac-20190705-105025-batch"

FILES=(
  "/home/gabriel/Pictures/2019/07/05/20190705_105025(1).jpg"
  "/home/gabriel/Pictures/mackinac/20190705_105025(1).jpg"
)

mkdir -p "$QUARANTINE_ROOT"

for src in "${FILES[@]}"; do
  dst="$QUARANTINE_ROOT$src"
  mkdir -p "$(dirname "$dst")"
  mv "$src" "$dst"
done
