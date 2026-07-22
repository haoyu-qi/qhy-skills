#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 FILE.html" >&2
  exit 2
fi

file=$1
errors=0

check_required() {
  local pattern=$1
  local label=$2
  if ! rg -q "$pattern" "$file"; then
    echo "FAIL: missing $label"
    errors=$((errors + 1))
  fi
}

check_forbidden() {
  local pattern=$1
  local label=$2
  if rg -q "$pattern" "$file"; then
    echo "FAIL: found $label"
    errors=$((errors + 1))
  fi
}

check_required '<meta charset="UTF-8">' 'UTF-8 meta tag'
check_required 'name="viewport"' 'viewport meta tag'
check_required '@media[[:space:]]*\(max-width:[[:space:]]*768px\)' '768px mobile breakpoint'
check_forbidden 'https?://' 'external URL dependency'
check_forbidden '#000000([;"[:space:]]|$)' 'pure black color'
check_forbidden '\{\{[A-Z0-9_]+\}\}' 'unreplaced template placeholder'

if [[ $errors -gt 0 ]]; then
  echo "Quality check failed: $errors issue(s)"
  exit 1
fi

echo "Quality check passed: $file"
