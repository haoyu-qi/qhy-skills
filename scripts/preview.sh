#!/usr/bin/env bash
# =============================================================================
# preview.sh — 快速在浏览器中预览生成的 HTML 文件
# 用法：bash scripts/preview.sh <file.html>
# =============================================================================

set -euo pipefail

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # 无颜色

print_info()    { echo -e "${BLUE}[INFO]${NC}  $*"; }
print_ok()      { echo -e "${GREEN}[OK]${NC}    $*"; }
print_warn()    { echo -e "${YELLOW}[WARN]${NC}  $*"; }
print_error()   { echo -e "${RED}[ERROR]${NC} $*"; }

# ─── 参数检查 ───────────────────────────────────────────────────────────────
if [[ $# -lt 1 ]]; then
  echo ""
  echo "  📋 用法："
  echo "     bash scripts/preview.sh <file.html>"
  echo ""
  echo "  示例："
  echo "     bash scripts/preview.sh output.html"
  echo "     bash scripts/preview.sh ~/Desktop/my-card.html"
  echo ""
  exit 1
fi

FILE="${1}"

# ─── 文件存在检查 ────────────────────────────────────────────────────────────
if [[ ! -f "${FILE}" ]]; then
  print_error "文件不存在：${FILE}"
  exit 1
fi

# 转换为绝对路径
ABS_PATH="$(cd "$(dirname "${FILE}")" && pwd)/$(basename "${FILE}")"

# ─── 文件大小检查 ────────────────────────────────────────────────────────────
FILE_SIZE_KB=$(( $(wc -c < "${FILE}") / 1024 ))
print_info "文件：${ABS_PATH}"
print_info "大小：${FILE_SIZE_KB} KB"

if [[ ${FILE_SIZE_KB} -gt 500 ]]; then
  print_warn "文件较大（${FILE_SIZE_KB}KB），可能包含内联图片，预览可能稍慢"
fi

# ─── 打开浏览器 ──────────────────────────────────────────────────────────────
OS="$(uname -s)"

case "${OS}" in
  Darwin)   # macOS
    print_info "正在 macOS 下打开浏览器..."
    open "file://${ABS_PATH}"
    ;;
  Linux)
    if command -v xdg-open &>/dev/null; then
      xdg-open "file://${ABS_PATH}"
    elif command -v google-chrome &>/dev/null; then
      google-chrome "file://${ABS_PATH}"
    else
      print_error "无法找到可用的浏览器，请手动打开：file://${ABS_PATH}"
      exit 1
    fi
    ;;
  CYGWIN*|MINGW*|MSYS*)  # Windows
    start "file://${ABS_PATH}"
    ;;
  *)
    print_warn "未知操作系统（${OS}），请手动在浏览器中打开："
    echo "  file://${ABS_PATH}"
    exit 0
    ;;
esac

print_ok "已在默认浏览器中打开 ✨"
echo ""
echo "  💡 提示：如果浏览器未打开，请手动复制以下地址："
echo "     file://${ABS_PATH}"
echo ""
