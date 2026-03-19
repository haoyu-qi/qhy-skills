#!/usr/bin/env bash
# =============================================================================
# quality-check.sh — 对生成的 HTML 信息图进行质量检查
# 用法：bash scripts/quality-check.sh <file.html>
#
# 检查项目：
#   [1] 外部 CSS/JS 依赖（CDN 链接）
#   [2] 外部图片引用（src="http..."）
#   [3] <style> 内联样式存在
#   [4] 响应式断点
#   [5] UTF-8 编码声明
#   [6] viewport meta 标签
#   [7] z-content 拼写错误（应为 z-index）
#   [8] 空 <ul> 标签
#   [9] 文件大小（建议 <300KB）
# =============================================================================

set -uo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m'

PASS=0
WARN=0
FAIL=0

check_pass() { echo -e "  ${GREEN}✅ PASS${NC} $*"; ((PASS++)) || true; }
check_warn() { echo -e "  ${YELLOW}⚠️  WARN${NC} $*"; ((WARN++)) || true; }
check_fail() { echo -e "  ${RED}❌ FAIL${NC} $*"; ((FAIL++)) || true; }

# ─── 参数检查 ───────────────────────────────────────────────────────────────
if [[ $# -lt 1 ]]; then
  echo ""
  echo "  📋 用法："
  echo "     bash scripts/quality-check.sh <file.html>"
  echo ""
  exit 1
fi

FILE="${1}"

if [[ ! -f "${FILE}" ]]; then
  echo -e "${RED}[ERROR]${NC} 文件不存在：${FILE}"
  exit 1
fi

echo ""
echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BOLD}  🔍 信息图质量检查报告${NC}"
echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "  文件：${FILE}"
echo ""

# ─── 检查 [1]：外部 CSS/JS ──────────────────────────────────────────────────
EXT_CSS=$(grep -c 'href="https\?://' "${FILE}" 2>/dev/null || true)
EXT_JS=$(grep -c 'src="https\?://' "${FILE}" 2>/dev/null || true)
TOTAL_EXT=$((EXT_CSS + EXT_JS))

if [[ ${TOTAL_EXT} -eq 0 ]]; then
  check_pass "无外部 CSS/JS 依赖"
else
  check_fail "发现 ${TOTAL_EXT} 处外部依赖（违反零外部依赖规则）"
  grep -n 'href="https\?://\|src="https\?://' "${FILE}" | head -5 | while read -r line; do
    echo -e "       ${YELLOW}→${NC} ${line}"
  done
fi

# ─── 检查 [2]：外部图片 ─────────────────────────────────────────────────────
EXT_IMG=$(grep -cE 'src="https?://' "${FILE}" 2>/dev/null || true)
EXT_IMG_LOCAL=$(grep -cE 'src="(?!data:)[^"]*\.(png|jpg|jpeg|gif|webp|svg)"' "${FILE}" 2>/dev/null || true)

if [[ ${EXT_IMG} -eq 0 && ${EXT_IMG_LOCAL} -eq 0 ]]; then
  check_pass "无外部图片引用"
elif [[ ${EXT_IMG} -gt 0 ]]; then
  check_fail "发现 ${EXT_IMG} 处外部图片 URL（图片无法在离线环境显示）"
else
  check_warn "发现 ${EXT_IMG_LOCAL} 处本地图片路径（确保文件与 HTML 同目录）"
fi

# ─── 检查 [3]：<style> 内联 CSS ──────────────────────────────────────────────
if grep -q '<style' "${FILE}"; then
  check_pass "包含 <style> 内联样式"
else
  check_fail "缺少 <style> 标签（所有 CSS 应内联）"
fi

# ─── 检查 [4]：响应式断点 ───────────────────────────────────────────────────
if grep -q 'max-width.*768px\|min-width.*768px' "${FILE}"; then
  check_pass "包含响应式断点 @media (max-width: 768px)"
else
  check_warn "未发现 768px 响应式断点（移动端可能显示异常）"
fi

# ─── 检查 [5]：charset 声明 ─────────────────────────────────────────────────
if grep -qi 'charset.*utf-8\|charset="utf-8"' "${FILE}"; then
  check_pass "包含 UTF-8 编码声明"
else
  check_fail "缺少 <meta charset=\"UTF-8\">（中文可能乱码）"
fi

# ─── 检查 [6]：viewport meta ────────────────────────────────────────────────
if grep -qi 'name="viewport"' "${FILE}"; then
  check_pass "包含 viewport meta 标签"
else
  check_warn "缺少 viewport meta（移动端可能缩放异常）"
fi

# ─── 检查 [7]：z-content 拼写错误 ───────────────────────────────────────────
if grep -q 'z-content' "${FILE}"; then
  Z_LINES=$(grep -n 'z-content' "${FILE}" | head -3)
  check_fail "发现 'z-content' 拼写错误（应为 'z-index'）:\n$(echo "${Z_LINES}" | sed 's/^/       → /')"
else
  check_pass "无 z-content 拼写错误"
fi

# ─── 检查 [8]：空 <ul> 标签 ─────────────────────────────────────────────────
EMPTY_UL=$(grep -cE '<ul[^>]*>\s*</ul>' "${FILE}" 2>/dev/null || true)
if [[ ${EMPTY_UL} -eq 0 ]]; then
  check_pass "无空 <ul> 标签"
else
  check_warn "发现 ${EMPTY_UL} 处空 <ul> 标签"
fi

# ─── 检查 [9]：文件大小 ────────────────────────────────────────────────────
FILE_SIZE_KB=$(( $(wc -c < "${FILE}") / 1024 ))
if [[ ${FILE_SIZE_KB} -le 100 ]]; then
  check_pass "文件大小：${FILE_SIZE_KB}KB（优秀）"
elif [[ ${FILE_SIZE_KB} -le 300 ]]; then
  check_pass "文件大小：${FILE_SIZE_KB}KB（正常）"
elif [[ ${FILE_SIZE_KB} -le 600 ]]; then
  check_warn "文件大小：${FILE_SIZE_KB}KB（偏大，可能有大量内联数据）"
else
  check_warn "文件大小：${FILE_SIZE_KB}KB（较大，建议检查是否有不必要的内联资源）"
fi

# ─── 汇总 ──────────────────────────────────────────────────────────────────
echo ""
echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "  结果汇总：${GREEN}✅ ${PASS} 通过${NC}  ${YELLOW}⚠️  ${WARN} 警告${NC}  ${RED}❌ ${FAIL} 失败${NC}"
echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

if [[ ${FAIL} -eq 0 && ${WARN} -eq 0 ]]; then
  echo -e "  🎉 ${GREEN}完美！所有检查项均通过。${NC}"
elif [[ ${FAIL} -eq 0 ]]; then
  echo -e "  👍 ${YELLOW}基本合格，建议修复警告项后再分享。${NC}"
else
  echo -e "  🔧 ${RED}有 ${FAIL} 项需要修复，请根据上方提示调整 HTML。${NC}"
fi
echo ""

# 有失败项时返回非零退出码
[[ ${FAIL} -eq 0 ]]
