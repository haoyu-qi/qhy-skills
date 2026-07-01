# 白色 Google 官网风格 (Google White Official Inspired Style)

适用于：产品功能介绍、工具说明、轻量更新公告、教育类信息图、面向广泛用户的产品页。

## 角色定义

清爽、直观、可亲近的产品官网设计师。用大量白色空间、圆角模块、Google 四色点缀和明确的信息层级表达复杂内容。

## 视觉来源与边界

该风格借鉴 Google 官网和 About Google 常见的白色页面、宽松间距、圆角图文模块、蓝红黄绿四色强调和简洁导航感。不要使用 Google Logo、官方字体文件、外链素材或可混淆的商标锁定。

## 核心气质

- 明亮、可信、轻量。
- 信息层级清楚，标题简洁，说明文字像产品页面。
- 主体以白色和浅灰为底，四色只做小面积提示。
- 圆角偏大但克制，阴影轻，边框浅。

## 色彩系统

```css
:root {
  --bg: #ffffff;
  --surface: #ffffff;
  --surface-soft: #f8fafd;
  --ink: #202124;
  --muted: #5f6368;
  --line: #dadce0;
  --blue: #1a73e8;
  --red: #ea4335;
  --yellow: #fbbc04;
  --green: #34a853;
  --shadow: 0 20px 50px rgba(60, 64, 67, 0.10);
}
```

## 字体与排版

```css
body {
  background: var(--bg);
  color: var(--ink);
  font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", system-ui, sans-serif;
}

h1 {
  font-size: clamp(42px, 6vw, 78px);
  line-height: 1.06;
  letter-spacing: 0;
  font-weight: 700;
}

.lead {
  color: var(--muted);
  font-size: 19px;
  line-height: 1.7;
}
```

## 布局组件

```css
.page {
  width: min(1240px, 100%);
  margin: 0 auto;
  padding: 34px 24px 56px;
}

.topbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 0 28px;
  color: var(--muted);
  font-size: 14px;
}

.hero {
  display: grid;
  grid-template-columns: 1.1fr 0.9fr;
  gap: 36px;
  align-items: center;
  padding: 36px 0 44px;
}

.surface {
  border: 1px solid var(--line);
  border-radius: 28px;
  background: var(--surface);
  box-shadow: var(--shadow);
  padding: 28px;
}

.soft-band {
  border-radius: 32px;
  background: var(--surface-soft);
  padding: 32px;
}

.google-dots {
  display: grid;
  grid-template-columns: repeat(4, 10px);
  gap: 8px;
}

.google-dots span:nth-child(1) { background: var(--blue); }
.google-dots span:nth-child(2) { background: var(--red); }
.google-dots span:nth-child(3) { background: var(--yellow); }
.google-dots span:nth-child(4) { background: var(--green); }

.google-dots span {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}
```

## 信息组织

- 适合“一个主标题 + 一个浅色功能面板 + 多个任务模块”。
- 数据或计数用大号蓝色数字，不用深色仪表盘。
- 如果内容是更新说明，新增功能可以用蓝色主卡，问题优化用绿色，问题处理用浅灰列表。
- 问题单号放在底部小标签，颜色保持浅灰，不要像告警。

## 避坑

- 不要让四色大面积铺满页面。
- 不使用过强渐变、暗黑背景或玻璃拟态。
- 不模拟 Google 标志，也不使用外部 Google Fonts。
- 卡片圆角可以大，但不要把所有模块做成同尺寸三列。
