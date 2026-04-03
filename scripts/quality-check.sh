#!/usr/bin/env bash

set -uo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
NC='\033[0m'

PASS=0
WARN=0
FAIL=0

check_pass() { echo -e "  ${GREEN}PASS${NC} $*"; ((PASS++)) || true; }
check_warn() { echo -e "  ${YELLOW}WARN${NC} $*"; ((WARN++)) || true; }
check_fail() { echo -e "  ${RED}FAIL${NC} $*"; ((FAIL++)) || true; }

if [[ $# -lt 1 ]]; then
  echo "用法：bash scripts/quality-check.sh <file.html>"
  exit 1
fi

FILE="${1}"

if [[ ! -f "${FILE}" ]]; then
  echo -e "${RED}文件不存在：${FILE}${NC}"
  exit 1
fi

echo ""
echo -e "${BOLD}qhy-card HTML 质量检查${NC}"
echo -e "  文件：${FILE}"
echo ""

EXT_LINKS=$(grep -cE 'href="https?://|src="https?://' "${FILE}" 2>/dev/null || true)
if [[ ${EXT_LINKS} -eq 0 ]]; then
  check_pass "未发现外部 CSS / JS 依赖"
else
  check_fail "发现 ${EXT_LINKS} 处外部依赖"
fi

EXT_FONT=$(grep -cE '@import url\(|fonts.googleapis|fonts.gstatic' "${FILE}" 2>/dev/null || true)
if [[ ${EXT_FONT} -eq 0 ]]; then
  check_pass "未发现远程字体依赖"
else
  check_fail "发现 ${EXT_FONT} 处远程字体依赖"
fi

EXT_IMG=$(grep -cE 'src="https?://' "${FILE}" 2>/dev/null || true)
if [[ ${EXT_IMG} -eq 0 ]]; then
  check_pass "未发现远程图片"
else
  check_fail "发现 ${EXT_IMG} 处远程图片"
fi

if grep -qi '<meta charset="utf-8"\|<meta charset=UTF-8\|<meta charset="UTF-8"' "${FILE}"; then
  check_pass "包含 UTF-8 声明"
else
  check_fail "缺少 UTF-8 声明"
fi

if grep -qi 'name="viewport"' "${FILE}"; then
  check_pass "包含 viewport 声明"
else
  check_warn "缺少 viewport 声明"
fi

if grep -q '<style' "${FILE}"; then
  check_pass "包含内联样式"
else
  check_fail "缺少 <style> 内联样式"
fi

if grep -q '@media (max-width: 768px)\|@media(max-width:768px)' "${FILE}"; then
  check_pass "包含移动端断点"
else
  check_warn "未发现 768px 断点"
fi

if grep -q 'z-content' "${FILE}"; then
  check_fail "发现 z-content 拼写错误"
else
  check_pass "未发现 z-content 拼写错误"
fi

EMPTY_UL=$(grep -cE '<ul[^>]*>[[:space:]]*</ul>' "${FILE}" 2>/dev/null || true)
if [[ ${EMPTY_UL} -eq 0 ]]; then
  check_pass "未发现空列表"
else
  check_warn "发现 ${EMPTY_UL} 处空 <ul>"
fi

UNRESOLVED=$(grep -c '{{[A-Z_]\+}}' "${FILE}" 2>/dev/null || true)
if [[ ${UNRESOLVED} -eq 0 ]]; then
  check_pass "未发现未替换模板变量"
else
  check_fail "发现 ${UNRESOLVED} 处未替换模板变量"
fi

PURE_BLACK=$(grep -c '#000000\|rgb(0,0,0)' "${FILE}" 2>/dev/null || true)
if [[ ${PURE_BLACK} -eq 0 ]]; then
  check_pass "未发现纯黑色值"
else
  check_warn "发现 ${PURE_BLACK} 处纯黑色值"
fi

FILE_SIZE_KB=$(( $(wc -c < "${FILE}") / 1024 ))
if [[ ${FILE_SIZE_KB} -le 160 ]]; then
  check_pass "文件大小 ${FILE_SIZE_KB}KB"
elif [[ ${FILE_SIZE_KB} -le 400 ]]; then
  check_warn "文件大小 ${FILE_SIZE_KB}KB，略大"
else
  check_warn "文件大小 ${FILE_SIZE_KB}KB，建议精简"
fi

echo ""
echo -e "  汇总：${GREEN}${PASS} PASS${NC}  ${YELLOW}${WARN} WARN${NC}  ${RED}${FAIL} FAIL${NC}"
echo ""

[[ ${FAIL} -eq 0 ]]
