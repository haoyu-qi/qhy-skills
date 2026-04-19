#!/usr/bin/env bash
set -euo pipefail

NAME="${1:-}"
PARENT="${2:-examples}"

if [[ -z "$NAME" ]]; then
  echo "usage: new-deck.sh <name> [parent-dir]" >&2
  exit 1
fi

HERE="$(cd "$(dirname "$0")/.." && pwd)"
TEMPLATE="$HERE/assets/deck-starter.html"
OUT_DIR="$HERE/$PARENT/$NAME"

if [[ ! -f "$TEMPLATE" ]]; then
  echo "error: template not found at $TEMPLATE" >&2
  exit 1
fi

if [[ -e "$OUT_DIR" ]]; then
  echo "error: $OUT_DIR already exists" >&2
  exit 1
fi

mkdir -p "$OUT_DIR"
cp "$TEMPLATE" "$OUT_DIR/index.html"

echo "created $OUT_DIR/index.html"
echo ""
echo "next steps:"
echo "  1. Replace placeholders in index.html"
echo "  2. Open it in a browser and verify keyboard navigation"
echo "  3. Render previews with scripts/render.sh"
