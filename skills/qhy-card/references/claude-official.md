# Claude 官网风格 (Claude Official Inspired Style)

适用于：AI 产品介绍、产品发布说明、研究摘要、能力说明、品牌感较强的内容页。

## 角色定义

克制的 AI 产品官网视觉设计师。用温暖、编辑感、理性留白来呈现技术内容，避免霓虹科技感和硬质仪表盘感。

## 视觉来源与边界

该风格借鉴 Claude / Anthropic 官网常见的暖色背景、编辑式排版、细线分隔、低饱和强调色和宽松留白。不要使用官方 Logo、官方字体文件、外链图片或可混淆的商标元素。

## 核心气质

- 温暖而理性：米白、陶土、深墨色搭配。
- 编辑感强：大标题像杂志头版，正文像产品故事。
- 结构克制：少用强阴影，多用细边框、分栏、留白。
- 科技内容不做冷蓝黑，优先“人文科技”的语气。

## 色彩系统

```css
:root {
  --bg: #f4efe7;
  --paper: #fbf7ef;
  --paper-soft: #eee6da;
  --ink: #2b2118;
  --muted: #6f6257;
  --line: rgba(43, 33, 24, 0.14);
  --accent: #b15f3b;
  --accent-soft: rgba(177, 95, 59, 0.12);
  --sage: #7d8b6f;
  --shadow: 0 28px 80px rgba(77, 54, 37, 0.12);
}
```

## 字体与排版

```css
body {
  background: var(--bg);
  color: var(--ink);
  font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", system-ui, sans-serif;
}

h1, .display {
  font-family: "Songti SC", "STSong", "Noto Serif SC", serif;
  font-size: clamp(46px, 7vw, 92px);
  line-height: 0.98;
  letter-spacing: 0;
  font-weight: 700;
}

.lead {
  font-size: 20px;
  line-height: 1.75;
  color: var(--muted);
}
```

## 布局组件

```css
.page {
  width: min(1220px, 100%);
  margin: 0 auto;
  padding: 48px 24px 64px;
}

.frame {
  border: 1px solid var(--line);
  border-radius: 28px;
  background: var(--paper);
  box-shadow: var(--shadow);
  overflow: hidden;
}

.hero {
  display: grid;
  grid-template-columns: 1.18fr 0.82fr;
  gap: 44px;
  padding: 54px 54px 36px;
}

.section {
  padding: 34px 54px;
  border-top: 1px solid var(--line);
}

.panel {
  border: 1px solid var(--line);
  border-radius: 18px;
  background: rgba(255, 252, 246, 0.72);
  padding: 24px;
}

.eyebrow {
  display: inline-flex;
  border: 1px solid var(--line);
  border-radius: 999px;
  padding: 7px 12px;
  color: var(--accent);
  background: var(--accent-soft);
  font-size: 13px;
}
```

## 适合的结构

- 单个产品主张 + 2 到 4 个论据模块。
- 发布说明中的“新增能力”可以做成温暖的主卡片。
- 研究/观点类内容适合左大标题、右摘要或引用。

## 避坑

- 不使用黑蓝霓虹背景。
- 不做密集仪表盘，也不做三列等宽功能卡。
- 不照搬官方文案、Logo 或具体页面布局。
- 不使用负字距，中文正文要保持舒展。
