#!/usr/bin/env bash

set -uo pipefail

BOLD='\033[1m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

clear
echo ""
echo -e "${BOLD}╔══════════════════════════════════════════════════╗${NC}"
echo -e "${BOLD}║              qhy-card 提示词脚手架             ║${NC}"
echo -e "${BOLD}╚══════════════════════════════════════════════════╝${NC}"
echo ""

echo -e "${BOLD}【第 1 步】选择模具${NC}"
echo ""
echo -e "  ${CYAN}1)${NC} 信息图   - 一图看懂、内容拆解、教程总览"
echo -e "  ${CYAN}2)${NC} 海报页   - 观点海报、发布封面、活动预告"
echo -e "  ${CYAN}3)${NC} 白板图   - 结构图、流程图、方法论拆解"
echo -e "  ${CYAN}4)${NC} 周报板   - 周报、月报、项目进展"
echo ""
read -rp "  请输入数字 [1-4]：" MODE_NUM

case "${MODE_NUM}" in
  2) MODE_NAME="海报页" ;;
  3) MODE_NAME="白板图" ;;
  4) MODE_NAME="周报板" ;;
  *) MODE_NAME="信息图" ;;
esac

echo ""
echo -e "  ✅ 已选择：${GREEN}${MODE_NAME}${NC}"

echo ""
echo -e "${BOLD}【第 2 步】选择视觉风格${NC}"
echo ""
echo -e "  ${CYAN}1)${NC} 暗黑科技风"
echo -e "  ${CYAN}2)${NC} 扁平现代风"
echo -e "  ${CYAN}3)${NC} 杂志质感风"
echo -e "  ${CYAN}4)${NC} 复古书卷风"
echo -e "  ${CYAN}5)${NC} 蓝图波普风"
echo -e "  ${CYAN}6)${NC} 纯白演示风"
echo -e "  ${CYAN}7)${NC} 周报模块风"
echo -e "  ${CYAN}0)${NC} 自动判断（推荐）"
echo -e "  ${CYAN}8)${NC} 先给我几个候选风格，再让我选"
echo ""
read -rp "  请输入数字 [0-8]：" STYLE_NUM

case "${STYLE_NUM}" in
  1) STYLE_NAME="暗黑科技风" ;;
  2) STYLE_NAME="扁平现代风" ;;
  3) STYLE_NAME="杂志质感风" ;;
  4) STYLE_NAME="复古书卷风" ;;
  5) STYLE_NAME="蓝图波普风" ;;
  6) STYLE_NAME="纯白演示风" ;;
  7) STYLE_NAME="周报模块风" ;;
  8) STYLE_NAME="候选推荐" ;;
  *) STYLE_NAME="自动判断" ;;
esac

echo ""
echo -e "${BOLD}【第 3 步】输入主题${NC}"
echo ""
read -rp "  主题：" TOPIC
if [[ -z "${TOPIC}" ]]; then
  TOPIC="[请填写主题]"
fi

echo ""
echo -e "${BOLD}【第 4 步】附加要求（可选）${NC}"
echo ""
echo -e "  示例：信息密集、宽一点、中文字体、无需注释"
echo ""
read -rp "  要求：" EXTRA

echo ""
echo -e "${BOLD}【第 5 步】内容来源${NC}"
echo ""
echo -e "  ${CYAN}1)${NC} Claude 自行组织内容"
echo -e "  ${CYAN}2)${NC} 我会粘贴原始内容"
echo ""
read -rp "  请选择 [1/2]：" SOURCE_NUM

PROMPT="请用 qhy-card 生成一张 HTML 视觉卡片。"
PROMPT+="
模具：${MODE_NAME}"

if [[ "${STYLE_NAME}" != "自动判断" ]]; then
  if [[ "${STYLE_NAME}" == "候选推荐" ]]; then
    PROMPT+="
先不要直接生成，请先根据主题给出 3 个合适的视觉风格方向，并分别说明为什么适合；等我选定后，再输出最终 HTML。"
  else
    PROMPT+="
风格：${STYLE_NAME}"
  fi
fi

PROMPT+="
主题：${TOPIC}"

if [[ -n "${EXTRA}" ]]; then
  PROMPT+="
要求：${EXTRA}"
fi

if [[ "${SOURCE_NUM}" == "2" ]]; then
  PROMPT+="

我附上原始内容，请直接提炼并生成：
[在此粘贴原始内容]"
fi

clear
echo ""
echo -e "${BOLD}╔══════════════════════════════════════════════════╗${NC}"
echo -e "${BOLD}║                生成的提示词                    ║${NC}"
echo -e "${BOLD}╚══════════════════════════════════════════════════╝${NC}"
echo ""
echo "${PROMPT}"
echo ""
echo -e "${BLUE}后续建议：${NC}"
echo -e "  1. 生成 HTML 后执行 ${CYAN}bash scripts/quality-check.sh output.html${NC}"
echo -e "  2. 然后执行 ${CYAN}bash scripts/preview.sh output.html${NC}"
echo ""
