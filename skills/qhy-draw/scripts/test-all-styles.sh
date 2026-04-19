#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
OUT_DIR="$SKILL_DIR/test-output"

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
  echo "Python runtime not found"
  exit 1
fi

mkdir -p "$OUT_DIR"

PASS=0
FAIL=0

for fixture in "$SKILL_DIR"/fixtures/*.json; do
  [ -e "$fixture" ] || continue
  name="$(basename "$fixture" .json)"
  svg="$OUT_DIR/$name.svg"
  echo "Generating $name"
  if "$PYTHON_BIN" "$SCRIPT_DIR/generate-from-template.py" auto "$svg" "$fixture"; then
    if "$SCRIPT_DIR/validate-svg.sh" "$svg"; then
      PASS=$((PASS + 1))
    else
      FAIL=$((FAIL + 1))
    fi
  else
    FAIL=$((FAIL + 1))
  fi
done

echo "Passed: $PASS"
echo "Failed: $FAIL"

if [ "$FAIL" -gt 0 ]; then
  exit 1
fi
