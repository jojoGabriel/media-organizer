#!/usr/bin/env bash
set -euo pipefail

# Manual cleanup driver generated from the reviewed manifests and notes.
# Default behavior is dry-run. To execute moves into quarantine:
#   APPLY=1 ./manual_cleanup_commands_2026-04-14.sh
#
# Files are moved into a quarantine tree instead of being deleted outright:
#   $HOME/media-organizer-quarantine-2026-04-14

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPORTS_DIR="$SCRIPT_DIR/reports"
GOOGLE_ROOT="$HOME/Pictures/google-takeout/Takeout/Google Photos"
QUARANTINE_ROOT="$HOME/media-organizer-quarantine-2026-04-14"
APPLY="${APPLY:-0}"

run_mv() {
  local src="$1"
  local dest="$QUARANTINE_ROOT$src"

  if [[ ! -e "$src" ]]; then
    printf 'MISSING %s\n' "$src"
    return 0
  fi

  if [[ "$APPLY" == "1" ]]; then
    mkdir -p "$(dirname "$dest")"
    mv -vn -- "$src" "$dest"
  else
    printf 'mv -vn -- %q %q\n' "$src" "$dest"
  fi
}

move_manifest_files() {
  local folder="$1"
  local manifest="$2"
  while IFS= read -r name; do
    [[ -n "$name" ]] || continue
    run_mv "$GOOGLE_ROOT/$folder/$name"
  done < "$manifest"
}

move_manifest_files_under_root() {
  local root="$1"
  local manifest="$2"
  while IFS= read -r name; do
    [[ -n "$name" ]] || continue
    run_mv "$root/$name"
  done < "$manifest"
}

move_top_level_files() {
  local folder="$1"
  shift
  local name
  for name in "$@"; do
    run_mv "$folder/$name"
  done
}

move_recursive_files() {
  local folder="$1"
  if [[ ! -d "$folder" ]]; then
    printf 'MISSING %s\n' "$folder"
    return 0
  fi
  while IFS= read -r -d '' path; do
    run_mv "$path"
  done < <(find "$folder" -type f -print0)
}

move_top_level_all_files() {
  local folder="$1"
  if [[ ! -d "$folder" ]]; then
    printf 'MISSING %s\n' "$folder"
    return 0
  fi
  while IFS= read -r -d '' path; do
    run_mv "$path"
  done < <(find "$folder" -mindepth 1 -maxdepth 1 -type f -print0)
}

move_top_level_all_except() {
  local folder="$1"
  local keep_name="$2"
  if [[ ! -d "$folder" ]]; then
    printf 'MISSING %s\n' "$folder"
    return 0
  fi
  while IFS= read -r -d '' path; do
    run_mv "$path"
  done < <(find "$folder" -mindepth 1 -maxdepth 1 -type f ! -name "$keep_name" -print0)
}

move_matching_range() {
  local folder="$1"
  local prefix="$2"
  local ext="$3"
  local start="$4"
  local end="$5"
  local n
  for ((n = start; n <= end; n++)); do
    printf -v file '%s%04d%s' "$prefix" "$n" "$ext"
    run_mv "$folder/$file"
  done
}

printf '# %s\n' "Manual cleanup commands"
printf '# APPLY=%s\n' "$APPLY"
printf '# QUARANTINE_ROOT=%s\n' "$QUARANTINE_ROOT"

printf '\n# Google Takeout exact manifests\n'
move_manifest_files "25th" "$REPORTS_DIR/google-takeout-safe-pass-25th.txt"
move_manifest_files "Photos from 2013" "$REPORTS_DIR/google-takeout-safe-pass-photos-from-2013.txt"
move_manifest_files "Photos from 2014" "$REPORTS_DIR/google-takeout-safe-pass-photos-from-2014-non-takeout-backed.txt"
move_manifest_files "Failed Videos" "$REPORTS_DIR/google-takeout-safe-pass-failed-videos.txt"
move_manifest_files "Untitled(4)" "$REPORTS_DIR/google-takeout-safe-pass-untitled-4.txt"
move_manifest_files "Untitled(4)" "$REPORTS_DIR/google-takeout-safe-pass-untitled-4-edited.txt"
move_manifest_files "Untitled" "$REPORTS_DIR/google-takeout-safe-pass-untitled.txt"
move_manifest_files "Untitled(1)" "$REPORTS_DIR/google-takeout-safe-pass-untitled-1.txt"
move_manifest_files "Untitled(2)" "$REPORTS_DIR/google-takeout-safe-pass-untitled-2.txt"
move_manifest_files "Untitled(3)" "$REPORTS_DIR/google-takeout-safe-pass-untitled-3.txt"
move_manifest_files "Photos from 2015" "$REPORTS_DIR/google-takeout-safe-pass-photos-from-2015.txt"
move_manifest_files "Photos from 2016" "$REPORTS_DIR/google-takeout-safe-pass-photos-from-2016.txt"
move_manifest_files "StarvedRock" "$REPORTS_DIR/google-takeout-safe-pass-starvedrock.txt"
move_manifest_files "Jab" "$REPORTS_DIR/google-takeout-safe-pass-jab.txt"
move_manifest_files "Jojo, Joy" "$REPORTS_DIR/google-takeout-safe-pass-jojo-joy.txt"
move_manifest_files "Jonel 26" "$REPORTS_DIR/google-takeout-safe-pass-jonel-26-received.txt"
move_manifest_files "Wednesday morning in Chicago" "$REPORTS_DIR/google-takeout-safe-pass-wednesday-morning-in-chicago-edited.txt"
move_manifest_files "Trip to Los Angeles and Anaheim" "$REPORTS_DIR/google-takeout-safe-pass-trip-to-los-angeles-and-anaheim-edited.txt"
move_manifest_files "Weekend in Fish Creek" "$REPORTS_DIR/google-takeout-safe-pass-weekend-in-fish-creek-edited.txt"
move_manifest_files "Weekend in Niagara Falls and Scarborough" "$REPORTS_DIR/google-takeout-safe-pass-weekend-in-niagara-falls-and-scarborough-edited.txt"
move_manifest_files "Memories together (5-23-2021)" "$REPORTS_DIR/google-takeout-safe-pass-memories-together-edited.txt"
move_manifest_files "Memories together (5-23-2021)" "$REPORTS_DIR/google-takeout-conditional-pass-memories-together-plain.txt"
move_manifest_files "Jonel 26" "$REPORTS_DIR/google-takeout-conditional-pass-jonel-26-plain.txt"
move_manifest_files "Weekend in Fish Creek" "$REPORTS_DIR/google-takeout-conditional-pass-weekend-in-fish-creek-plain.txt"
move_manifest_files "Weekend in Fish Creek" "$REPORTS_DIR/google-takeout-safe-pass-weekend-in-fish-creek-keep-overrides.txt"
move_manifest_files "Weekend in Niagara Falls and Scarborough" "$REPORTS_DIR/google-takeout-conditional-pass-weekend-in-niagara-falls-and-scarborough-plain.txt"
move_manifest_files "Weekend in Niagara Falls and Scarborough" "$REPORTS_DIR/google-takeout-safe-pass-weekend-in-niagara-falls-and-scarborough-overlay.txt"
move_manifest_files "Wednesday morning in Chicago" "$REPORTS_DIR/google-takeout-conditional-pass-wednesday-morning-in-chicago-plain.txt"
move_manifest_files "Trip to Los Angeles and Anaheim" "$REPORTS_DIR/google-takeout-conditional-pass-trip-to-los-angeles-and-anaheim-plain.txt"

printf '\n# Local duplicate cleanup candidates\n'

move_top_level_files "$HOME/Pictures/morePics" \
  "IMG142.jpg" \
  "IMG143.jpg" \
  "Thumbs.db"
while IFS= read -r -d '' path; do
  run_mv "$path"
done < <(find "$HOME/Pictures/morePics" -mindepth 1 -maxdepth 1 -type f \( -name '2006*.jpg' -o -name '2007*.jpg' \) -print0)

move_top_level_files "$HOME/Pictures/Photos" \
  "Thumbs.db" \
  "dscf4994-0.jpg" \
  "dscf4994-1.jpg" \
  "dscf4994.jpg" \
  "dscf5074.jpg" \
  "dscf5452.jpg" \
  "dscf5452-81.jpg" \
  "dscf5452-82.jpg" \
  "impo ige.jpg" \
  "inang luisa.jpg" \
  "ingkong dianong.jpg" \
  "tatang gelacio.jpg"
move_top_level_files "$HOME/Pictures/Photos/temp" \
  "Thumbs.db" \
  "DSCF1376.JPG"

move_top_level_files "$HOME/Pictures/1903/12/31" \
  "Thumbs.db" \
  "VIDEO_070.mp4" \
  "VIDEO_076.mp4" \
  "VIDEO_077.mp4" \
  "VIDEO_078.mp4"
move_recursive_files "$HOME/Pictures/1903/12/31/.wdmc"

move_top_level_files "$HOME/Pictures/Screenshots" \
  "desktop.ini" \
  "Thumbs.db"
move_recursive_files "$HOME/Pictures/Screenshots/.wdmc"

move_top_level_files "$HOME/Pictures/Photos/2007/Jun" "Thumbs.db"
move_matching_range "$HOME/Pictures/Photos/2007/Jun" "DSCF" ".JPG" 720 875

move_top_level_files "$HOME/Pictures/Photos/2007/2007-11-03--17.02.27" \
  "DSCF0779.JPG" \
  "DSCF0784.JPG" \
  "DSCF0802.JPG" \
  "DSCF0803.JPG" \
  "DSCF0827.JPG" \
  "DSCF0836.JPG" \
  "DSCF0854.JPG" \
  "DSCF0855.JPG" \
  "DSCF0859.JPG" \
  "Thumbs.db"

move_top_level_files "$HOME/Pictures/Photos/2007/2007-08-15--19.02.45" \
  "DSCF0142.JPG" \
  "DSCF0164.AVI" \
  "DSCF0185.AVI" \
  "DSCF0191.AVI" \
  "Thumbs.db"

move_matching_range "$HOME/Pictures/Photos/2008/2008-04-20--18.53.11" "DSCF" ".JPG" 1286 1454

move_top_level_all_files "$HOME/Pictures/Photos/2007/Dennis"
move_top_level_all_files "$HOME/Pictures/Photos/2009/dennis"
move_top_level_files "$HOME/Pictures/Photos/2007/2007-09-06--17.41.40" "PIC-0115.JPG"
move_top_level_all_files "$HOME/Pictures/Photos/2008/2008-04-16--21.19.57"
move_top_level_all_files "$HOME/Pictures/Photos/2007/2007-08-20--19.51.33"
move_top_level_all_files "$HOME/Pictures/Photos/2007/2007-09-09--17.34.58"
move_top_level_all_files "$HOME/Pictures/Photos/2007/2008-01-27--16.03.47"
move_top_level_all_except "$HOME/Pictures/Photos/2007/04/07" "200700044.jpg"
move_top_level_all_except "$HOME/Pictures/Photos/2007/08/14" "DSCF0142 (DSCF0142B.JPG).JPG"
move_top_level_all_files "$HOME/Pictures/Photos/2006/08/08"
move_top_level_all_files "$HOME/Pictures/Photos/2006/12/16"
move_top_level_all_files "$HOME/Pictures/Photos/2007/04/08"
move_top_level_all_files "$HOME/Pictures/Photos/2007/08/13"
move_top_level_all_files "$HOME/Pictures/Photos/2007/08/15"
move_top_level_all_files "$HOME/Pictures/Photos/2007/08/17"
move_top_level_all_files "$HOME/Pictures/Photos/2007/08/25"
move_top_level_all_files "$HOME/Pictures/Photos/2007/09/06"
move_top_level_all_files "$HOME/Pictures/Photos/2007/11/23"
move_top_level_all_files "$HOME/Pictures/Photos/2007/Beng"
move_top_level_all_files "$HOME/Pictures/Photos/2007/2007-11-24--11.46.02"
move_top_level_all_files "$HOME/Pictures/Photos/2007/2007-11-26--20.05.44"
move_top_level_all_files "$HOME/Pictures/Photos/2007/2007-12-13--18.20.12"
move_top_level_all_files "$HOME/Pictures/Photos/2008/07/28"
move_top_level_all_files "$HOME/Pictures/Photos/2009/08/30"
move_top_level_all_files "$HOME/Pictures/Photos/2009/10/01"
move_top_level_all_files "$HOME/Pictures/Photos/2009/10/04"

printf '\n# Mackinac exact manifest\n'
move_manifest_files_under_root "$HOME/Pictures/mackinac" "$REPORTS_DIR/mackinac-safe-pass-plain.txt"

printf '\n# Deferred by policy: -edited, received_*, metadata.json, sidecar-gap cases\n'
