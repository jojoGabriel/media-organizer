#!/usr/bin/env bash
set -euo pipefail

# Safe organization commands generated from unknown-no-destination-v76.
# This script only performs low-risk keep/move/rename operations.
# It does not delete cache candidates.

mkdir -p /home/gabriel/Videos/digitalDiary
if [ -f '/home/gabriel/Videos/digitalDiary/speedReader' ]; then mv -n '/home/gabriel/Videos/digitalDiary/speedReader' '/home/gabriel/Videos/digitalDiary/speedReader.mp4'; fi

mkdir -p /home/gabriel/Videos/Projects/Kdenlive
for f in '/home/gabriel/Videos/Kden/'*.kdenlive '/home/gabriel/Videos/YTintroTemplate-3000.kdenlive'; do [ -f "$f" ] && mv -n "$f" '/home/gabriel/Videos/Projects/Kdenlive/'; done

mkdir -p /home/gabriel/Pictures/Projects/PhotoDirector/gabriel
if [ -f '/home/gabriel/Pictures/PhotoDirector/3.0/gabriel/gabriel.phd' ]; then mv -n '/home/gabriel/Pictures/PhotoDirector/3.0/gabriel/gabriel.phd' '/home/gabriel/Pictures/Projects/PhotoDirector/gabriel/'; fi

mkdir -p /home/gabriel/Pictures/Projects/GIMP/mothers-day
if [ -f "/home/gabriel/Pictures/Photos/2010/05/09/mother's day.xcf" ]; then mv -n "/home/gabriel/Pictures/Photos/2010/05/09/mother's day.xcf" '/home/gabriel/Pictures/Projects/GIMP/mothers-day/'; fi

mkdir -p /home/gabriel/Pictures/Reference/Documents
if [ -f '/home/gabriel/Pictures/Scanned Document.pdf' ]; then mv -n '/home/gabriel/Pictures/Scanned Document.pdf' '/home/gabriel/Pictures/Reference/Documents/'; fi
