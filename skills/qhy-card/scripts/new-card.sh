#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 || $# -gt 2 ]]; then
  echo "Usage: $0 OUTPUT.html [infograph|poster|whiteboard|weekly|blueprint-manual|editorial-thesis]" >&2
  exit 2
fi

output=$1
kind=${2:-infograph}
root=$(cd "$(dirname "$0")/.." && pwd)

case "$kind" in
  infograph) template="$root/assets/infograph_template.html" ;;
  poster) template="$root/assets/poster_template.html" ;;
  whiteboard) template="$root/assets/whiteboard_template.html" ;;
  weekly) template="$root/assets/weekly_report_template.html" ;;
  blueprint-manual) template="$root/assets/blueprint_manual_template.html" ;;
  editorial-thesis) template="$root/assets/editorial_thesis_template.html" ;;
  *) echo "Unknown template: $kind" >&2; exit 2 ;;
esac

if [[ -e "$output" ]]; then
  echo "Refusing to overwrite existing file: $output" >&2
  exit 1
fi

cp "$template" "$output"
echo "Created: $output"
