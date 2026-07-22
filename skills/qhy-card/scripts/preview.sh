#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 FILE.html" >&2
  exit 2
fi

file=$1
if [[ ! -f "$file" ]]; then
  echo "File not found: $file" >&2
  exit 1
fi

case "$(uname -s)" in
  Darwin) open "$file" ;;
  Linux) xdg-open "$file" ;;
  *) echo "Open this file in a browser: $file" ;;
esac
