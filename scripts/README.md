# Scripts — 工具脚本说明

`scripts/` 目录提供三个辅助工具，提升信息图生成效率。

---

## 🖥️ preview.sh — 快速预览

在系统默认浏览器中打开生成的 HTML 文件。

```bash
bash scripts/preview.sh output.html
```

**支持：** macOS / Linux / Windows (Git Bash)

---

## 🔍 quality-check.sh — 质量检查

对输出 HTML 进行 9 项自动化检查：

| 检查项 | 说明 |
|--------|------|
| 外部 CSS/JS | 检测 CDN 链接（违反零依赖规则） |
| 外部图片 | 检测 `src="http..."` 图片 |
| 内联样式 | 确认 `<style>` 标签存在 |
| 响应式断点 | 检测 768px 媒体查询 |
| UTF-8 声明 | 确认 `<meta charset>` |
| Viewport | 确认移动端 meta 标签 |
| 拼写错误 | 检测 `z-content`（应为 `z-index`） |
| 空 `<ul>` | 检测空列表标签 |
| 文件大小 | 评估文件体积 |

```bash
bash scripts/quality-check.sh output.html
```

**退出码：** `0` = 无失败项；`1` = 有失败项（CI/CD 友好）

---

## 🎨 new-card.sh — 交互式提示词生成

通过问答引导，生成可直接发给 Claude 的信息图提示词。

```bash
bash scripts/new-card.sh
```

**流程：**

1. 选择风格（7 种 + 自动判断）
2. 输入主题
3. 附加视觉参数（可选）
4. 选择内容来源
5. 输出格式化提示词 → 复制发给 Claude

---

## 推荐工作流

```bash
# 1. 生成提示词
bash scripts/new-card.sh

# 2. 将提示词发给 Claude，Claude 生成 HTML
# 3. 将 HTML 保存为 output.html

# 4. 质量检查
bash scripts/quality-check.sh output.html

# 5. 浏览器预览
bash scripts/preview.sh output.html
```
