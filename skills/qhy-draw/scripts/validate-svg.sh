#!/bin/bash
set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

if [ $# -lt 1 ]; then
  echo "Usage: $0 <svg-file>"
  exit 1
fi

resolve_python() {
  if command -v python3 >/dev/null 2>&1; then
    command -v python3
    return
  fi
  if command -v python >/dev/null 2>&1; then
    command -v python
    return
  fi
  if [ -x "/c/Users/haoyu/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe" ]; then
    echo "/c/Users/haoyu/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe"
    return
  fi
  if [ -x "C:/Users/haoyu/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe" ]; then
    echo "C:/Users/haoyu/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe"
    return
  fi
  return 1
}

PYTHON_BIN="$(resolve_python || true)"
if [ -z "${PYTHON_BIN:-}" ]; then
  echo -e "${RED}Error: Python runtime not found${NC}"
  exit 1
fi

SVG_FILE="$1"

if [ ! -f "$SVG_FILE" ]; then
  echo -e "${RED}Error: File not found: $SVG_FILE${NC}"
  exit 1
fi

echo "Validating SVG: $SVG_FILE"
FAILURES=0

echo -n "Checking XML parse... "
if "$PYTHON_BIN" - "$SVG_FILE" <<'PY'
from pathlib import Path
import sys
import xml.etree.ElementTree as ET
ET.fromstring(Path(sys.argv[1]).read_text(encoding='utf-8'))
PY
then
  echo -e "${GREEN}OK${NC}"
else
  echo -e "${RED}FAIL${NC}"
  FAILURES=$((FAILURES + 1))
fi

echo -n "Checking svg root... "
if grep -q "<svg" "$SVG_FILE"; then
  echo -e "${GREEN}OK${NC}"
else
  echo -e "${RED}FAIL${NC}"
  FAILURES=$((FAILURES + 1))
fi

echo -n "Checking closing tag... "
if grep -q "</svg>" "$SVG_FILE"; then
  echo -e "${GREEN}OK${NC}"
else
  echo -e "${RED}FAIL${NC}"
  FAILURES=$((FAILURES + 1))
fi

echo -n "Checking marker references... "
if "$PYTHON_BIN" - "$SVG_FILE" <<'PY'
from pathlib import Path
import re
import sys
text = Path(sys.argv[1]).read_text(encoding='utf-8')
refs = set(re.findall(r'marker-(?:start|mid|end)="url\(#([^)]+)\)"', text))
defs = set(re.findall(r'<marker[^>]*id="([^"]+)"', text))
missing = sorted(refs - defs)
if missing:
    print("missing:" + ",".join(missing))
    raise SystemExit(1)
PY
then
  echo -e "${GREEN}OK${NC}"
else
  echo -e "${RED}FAIL${NC}"
  FAILURES=$((FAILURES + 1))
fi

if command -v rsvg-convert >/dev/null 2>&1; then
  echo -n "Checking rsvg-convert render... "
  TMP_PNG="${TMPDIR:-/tmp}/qhy-draw-validate.png"
  if rsvg-convert "$SVG_FILE" -o "$TMP_PNG" >/dev/null 2>&1; then
    rm -f "$TMP_PNG"
    echo -e "${GREEN}OK${NC}"
  else
    echo -e "${RED}FAIL${NC}"
    FAILURES=$((FAILURES + 1))
  fi
else
  echo -e "${YELLOW}Skipping rsvg-convert check${NC}"
fi

if [ "$FAILURES" -gt 0 ]; then
  echo -e "${RED}Validation failed with ${FAILURES} issue(s).${NC}"
  exit 1
fi

echo -e "${GREEN}Validation complete.${NC}"
