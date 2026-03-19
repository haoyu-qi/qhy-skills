#!/usr/bin/env bash
# =============================================================================
# new-card.sh — 交互式信息图创建脚手架
# 用法：bash scripts/new-card.sh
#
# 引导用户选择风格、输入主题，最终生成可直接发给 Claude 的提示词
# =============================================================================

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
echo -e "${BOLD}║     🎨 信息图生成脚手架 — infographic-card      ║${NC}"
echo -e "${BOLD}╚══════════════════════════════════════════════════╝${NC}"
echo ""

# ─── 步骤 1：风格选择 ────────────────────────────────────────────────────────
echo -e "${BOLD}【第 1 步】选择视觉风格${NC}"
echo ""
echo -e "  ${CYAN}1)${NC} 暗黑科技风  — 产品介绍、功能列表、版本日志"
echo -e "  ${CYAN}2)${NC} 扁平现代风  — AI 产品、性能跑分、技术指标"
echo -e "  ${CYAN}3)${NC} 杂志质感风  — 深度报道、社论、调研分析"
echo -e "  ${CYAN}4)${NC} 复古书卷风  — 书籍解析、读书笔记、文学内容"
echo -e "  ${CYAN}5)${NC} 蓝图波普风  — 选购指南、横向对比、避坑干货"
echo -e "  ${CYAN}6)${NC} 纯白演示风  — 季度汇报、版本发布、演示文稿"
echo -e "  ${CYAN}7)${NC} 周报模块风  — 工作周报、数据看板、团队进展"
echo -e "  ${CYAN}0)${NC} 自动判断   — 由 Claude 根据内容自动选择"
echo ""
read -rp "  请输入数字 [0-7]：" STYLE_NUM

case "${STYLE_NUM}" in
  1) STYLE_NAME="暗黑科技风" ;;
  2) STYLE_NAME="扁平现代风" ;;
  3) STYLE_NAME="杂志质感风" ;;
  4) STYLE_NAME="复古书卷风" ;;
  5) STYLE_NAME="蓝图波普风" ;;
  6) STYLE_NAME="纯白演示风" ;;
  7) STYLE_NAME="周报模块风" ;;
  0) STYLE_NAME="（自动判断）" ;;
  *)
    echo -e "\n  ${YELLOW}输入无效，已使用「自动判断」${NC}"
    STYLE_NAME="（自动判断）"
    ;;
esac

echo ""
echo -e "  ✅ 已选择：${GREEN}${STYLE_NAME}${NC}"

# ─── 步骤 2：主题内容 ────────────────────────────────────────────────────────
echo ""
echo -e "${BOLD}【第 2 步】输入信息图主题${NC}"
echo ""
echo -e "  示例："
echo -e "   · GPT-4o 的核心功能与技术规格"
echo -e "   · 《三体》第一部的内容解析"
echo -e "   · 2026年第一季度 Web 端版本更新"
echo -e "   · 2026年第9周工作周报"
echo ""
read -rp "  主题：" TOPIC

if [[ -z "${TOPIC}" ]]; then
  echo -e "\n  ${YELLOW}未输入主题，使用占位文本。${NC}"
  TOPIC="[请填写主题]"
fi

# ─── 步骤 3：附加参数 ────────────────────────────────────────────────────────
echo ""
echo -e "${BOLD}【第 3 步】附加视觉参数（可选，直接回车跳过）${NC}"
echo ""
echo -e "  示例：宽一点 / 信息密集 / 中文字体 / 无需注释"
echo ""
read -rp "  附加参数：" EXTRA_PARAMS

# ─── 步骤 4：输出内容来源 ────────────────────────────────────────────────────
echo ""
echo -e "${BOLD}【第 4 步】内容来源${NC}"
echo ""
echo -e "  ${CYAN}1)${NC} 让 Claude 自行检索和生成内容"
echo -e "  ${CYAN}2)${NC} 我会粘贴原始内容（手动复制到提示词中）"
echo ""
read -rp "  请选择 [1/2]：" SOURCE_NUM

case "${SOURCE_NUM}" in
  2) SOURCE_NOTE="（我附上了原始内容，请直接处理以下内容：）" ;;
  *) SOURCE_NOTE="" ;;
esac

# ─── 生成提示词 ──────────────────────────────────────────────────────────────
clear
echo ""
echo -e "${BOLD}╔══════════════════════════════════════════════════╗${NC}"
echo -e "${BOLD}║              ✨ 生成的提示词                    ║${NC}"
echo -e "${BOLD}╚══════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━ 复制以下内容 ━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# 构建提示词
PROMPT="请用 infographic-card 技能生成一张信息图。"

if [[ "${STYLE_NAME}" != "（自动判断）" ]]; then
  PROMPT+="
风格：${STYLE_NAME}"
fi

PROMPT+="
主题：${TOPIC}"

if [[ -n "${EXTRA_PARAMS}" ]]; then
  PROMPT+="
要求：${EXTRA_PARAMS}"
fi

if [[ -n "${SOURCE_NOTE}" ]]; then
  PROMPT+="

${SOURCE_NOTE}
[在此粘贴原始内容]"
fi

echo "${PROMPT}"
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "  💡 ${YELLOW}使用方式：${NC}"
echo -e "     将上面的提示词发送给 Claude（Claude code 或 claude.ai）"
echo -e "     Claude 将自动调用 infographic-card 技能生成 HTML 文件"
echo ""
echo -e "  🔍 生成后进行质量检查："
echo -e "     ${CYAN}bash scripts/quality-check.sh output.html${NC}"
echo ""
echo -e "  🖥️  快速预览："
echo -e "     ${CYAN}bash scripts/preview.sh output.html${NC}"
echo ""
