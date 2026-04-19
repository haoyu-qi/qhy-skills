#!/bin/bash
set -euo pipefail

STYLE="1"
WIDTH="1920"
VALIDATE=true
TYPE=""
OUTPUT_PATH=""

usage() {
  cat <<EOF
Usage: $0 [OPTIONS]

Options:
  -t, --type TYPE       Diagram type
  -s, --style STYLE     Style number (1-7, default: 1)
  -o, --output PATH     SVG output path
  -w, --width WIDTH     PNG width (default: 1920)
  --no-validate         Skip SVG validation
  -h, --help            Show help
EOF
  exit 0
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    -t|--type) TYPE="$2"; shift 2 ;;
    -s|--style) STYLE="$2"; shift 2 ;;
    -o|--output) OUTPUT_PATH="$2"; shift 2 ;;
    -w|--width) WIDTH="$2"; shift 2 ;;
    --no-validate) VALIDATE=false; shift ;;
    -h|--help) usage ;;
    *) echo "Unknown option: $1"; usage ;;
  esac
done

if [ -z "$TYPE" ]; then
  echo "Error: --type is required"
  exit 1
fi

if [ -z "$OUTPUT_PATH" ]; then
  OUTPUT_PATH="./${TYPE}-style${STYLE}.svg"
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SVG_FILE="$OUTPUT_PATH"
PNG_FILE="${SVG_FILE%.svg}.png"

if [ ! -f "$SVG_FILE" ]; then
  echo "SVG not found: $SVG_FILE"
  echo "Generate it first with generate-from-template.py or by hand."
  exit 1
fi

if [ "$VALIDATE" = true ]; then
  "$SCRIPT_DIR/validate-svg.sh" "$SVG_FILE"
fi

if command -v rsvg-convert >/dev/null 2>&1; then
  rsvg-convert -w "$WIDTH" "$SVG_FILE" -o "$PNG_FILE"
  echo "PNG exported: $PNG_FILE"
else
  echo "rsvg-convert not found; skipped PNG export."
fi
