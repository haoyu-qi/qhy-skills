#!/usr/bin/env bash
set -euo pipefail

FILE="${1:-}"
COUNT="${2:-1}"
OUT="${3:-}"

if [[ -z "$FILE" ]]; then
  echo "usage: render.sh <file> [N|all] [out-dir]" >&2
  exit 1
fi

if [[ ! -f "$FILE" ]]; then
  echo "error: $FILE not found" >&2
  exit 1
fi

detect_browser() {
  local candidates=(
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"
    "/usr/bin/google-chrome"
    "/usr/bin/chromium"
    "/usr/bin/chromium-browser"
  )

  for candidate in "${candidates[@]}"; do
    if [[ -x "$candidate" ]]; then
      echo "$candidate"
      return 0
    fi
  done

  return 1
}

BROWSER="$(detect_browser || true)"
if [[ -z "$BROWSER" ]]; then
  echo "error: Chrome/Chromium/Edge not found" >&2
  exit 1
fi

if [[ "$COUNT" == "all" ]]; then
  COUNT="$(grep -Eo 'class="[^"]*\bslide\b[^"]*"' "$FILE" | wc -l | tr -d ' ')"
  [[ -z "$COUNT" || "$COUNT" -lt 1 ]] && COUNT=1
elif ! [[ "$COUNT" =~ ^[0-9]+$ ]]; then
  echo "error: count must be a positive integer or 'all'" >&2
  exit 1
fi

ABS="$(cd "$(dirname "$FILE")" && pwd)/$(basename "$FILE")"
STEM="$(basename "${FILE%.*}")"

render_one() {
  local url="$1"
  local target="$2"
  mkdir -p "$(dirname "$target")"
  "$BROWSER" \
    --headless=new \
    --disable-gpu \
    --hide-scrollbars \
    --disable-crash-reporter \
    --disable-features=Crashpad \
    --no-first-run \
    --window-size=1920,1080 \
    --screenshot="$target" \
    "$url" >/dev/null 2>&1
  echo "rendered $target"
}

if [[ "$COUNT" == "1" ]]; then
  if [[ -z "$OUT" ]]; then
    OUT="$(dirname "$FILE")/${STEM}.png"
  elif [[ "${OUT##*.}" != "png" ]]; then
    OUT="$OUT/${STEM}.png"
  fi
  render_one "file://$ABS" "$OUT"
else
  if [[ -z "$OUT" ]]; then
    OUT="$(dirname "$FILE")/${STEM}-png"
  fi
  mkdir -p "$OUT"
  for ((i=1; i<=COUNT; i++)); do
    render_one "file://$ABS#/$i" "$OUT/${STEM}_$(printf '%02d' "$i").png"
  done
fi

echo "done: rendered $COUNT slide(s) from $FILE"
