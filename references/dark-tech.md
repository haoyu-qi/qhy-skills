# 暗黑科技风 (Dark Tech Style)

适用于：产品资料、功能列表、版本日志

## 角色定义

UI/UX 视觉架构师与高级前端开发工程师。擅长将复杂产品文档渲染为现代、冷峻、充满科技感的专业级暗黑模式单页信息图表。

---

## 核心视觉配置

### 色彩系统

```css
:root {
  --bg-page: #101116;
  --text-primary: #c0caf5;    /* 灰白 */
  --text-secondary: #7aa2f7;  /* 亮蓝 */
  --text-accent: #4ade80;     /* 科技绿 */
  --card-bg: #1F232B;
  --card-border: rgba(255, 255, 255, 0.08);
  --card-glow: 0 10px 40px rgba(122, 162, 247, 0.05);
}
```

### 悬浮辉光卡片

```css
.card {
  background: var(--card-bg);
  border-radius: 16px;
  border: 1px solid var(--card-border);
  box-shadow: var(--card-glow);
  position: relative;
  overflow: hidden;
  padding: 1.5rem;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 20px 60px rgba(122, 162, 247, 0.12);
}
```

### 背景水印编号

```css
.watermark {
  position: absolute;
  right: -10px;
  bottom: -20px;
  font-size: 8rem;
  font-weight: 900;
  color: #FFF;
  opacity: 0.04;
  z-index: 0;
  pointer-events: none;
  line-height: 1;
  user-select: none;
}

.card-content {
  position: relative;
  z-index: 1;
}
```

### 胶囊标签 (Pills)

```css
.pill {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 50px;
  background: rgba(122, 162, 247, 0.1);
  border: 1px solid rgba(122, 162, 247, 0.3);
  color: #7aa2f7;
  font-size: 0.8rem;
  font-weight: 500;
  margin-right: 6px;
  margin-bottom: 6px;
}

.pill-green {
  background: rgba(74, 222, 128, 0.1);
  border-color: rgba(74, 222, 128, 0.3);
  color: #4ade80;
}
```

### 顶部渐变光条

```css
.card::after {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(122, 162, 247, 0.4), transparent);
}
```

---

## 完整 HTML 骨架模板

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{标题}}</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }

    :root {
      --bg-page: #101116;
      --text-primary: #c0caf5;
      --text-secondary: #7aa2f7;
      --text-accent: #4ade80;
      --card-bg: #1F232B;
      --card-border: rgba(255,255,255,0.08);
    }

    body {
      background: var(--bg-page);
      color: var(--text-primary);
      font-family: -apple-system, 'PingFang SC', 'Microsoft YaHei', sans-serif;
      min-height: 100vh;
      padding: 2rem 1rem;
    }

    .page-container {
      max-width: 960px;
      margin: 0 auto;
    }

    /* 页眉 */
    .header {
      text-align: center;
      margin-bottom: 2.5rem;
    }
    .header .subtitle {
      font-size: 0.8rem;
      letter-spacing: 4px;
      color: #565f89;
      text-transform: uppercase;
      margin-bottom: 0.75rem;
    }
    .header .main-title {
      font-size: 2.8rem;
      font-weight: 800;
      color: var(--text-accent);
      line-height: 1.2;
    }
    .header .author-badge {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      margin-top: 1rem;
      padding: 6px 16px;
      background: rgba(255,255,255,0.04);
      border: 1px solid rgba(255,255,255,0.08);
      border-radius: 50px;
      font-size: 0.85rem;
      color: var(--text-secondary);
    }
    .header .notice-box {
      margin-top: 1rem;
      padding: 10px 16px;
      background: rgba(234, 179, 8, 0.08);
      border: 1px solid rgba(234, 179, 8, 0.2);
      border-radius: 8px;
      color: #eab308;
      font-size: 0.85rem;
      text-align: left;
    }

    /* 卡片网格 */
    .cards-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 1.25rem;
    }

    .card {
      background: var(--card-bg);
      border-radius: 16px;
      border: 1px solid var(--card-border);
      box-shadow: 0 10px 40px rgba(122,162,247,0.05);
      padding: 1.5rem;
      position: relative;
      overflow: hidden;
      transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .card:hover {
      transform: translateY(-4px);
      box-shadow: 0 20px 60px rgba(122,162,247,0.12);
    }
    .card::after {
      content: '';
      position: absolute;
      top: 0; left: 0; right: 0;
      height: 1px;
      background: linear-gradient(90deg, transparent, rgba(122,162,247,0.4), transparent);
    }

    .watermark {
      position: absolute;
      right: -10px; bottom: -20px;
      font-size: 8rem;
      font-weight: 900;
      color: #fff;
      opacity: 0.04;
      z-index: 0;
      line-height: 1;
      user-select: none;
      pointer-events: none;
    }
    .card-content { position: relative; z-index: 1; }

    .pills { margin-bottom: 0.75rem; }
    .pill {
      display: inline-block;
      padding: 3px 10px;
      border-radius: 50px;
      background: rgba(122,162,247,0.1);
      border: 1px solid rgba(122,162,247,0.3);
      color: var(--text-secondary);
      font-size: 0.78rem;
      margin-right: 5px;
    }

    .card-title {
      font-size: 1.1rem;
      font-weight: 700;
      color: var(--text-primary);
      margin-bottom: 0.75rem;
    }

    .card ul { padding-left: 0; list-style: none; }
    .card ul li {
      padding: 4px 0;
      font-size: 0.9rem;
      color: #9aa5ce;
      padding-left: 16px;
      position: relative;
    }
    .card ul li::before {
      content: '›';
      position: absolute;
      left: 0;
      color: var(--text-secondary);
    }

    /* 响应式 */
    @media (max-width: 768px) {
      .cards-grid { grid-template-columns: 1fr; }
      .header .main-title { font-size: 2rem; }
    }
  </style>
</head>
<body>
  <div class="page-container">

    <header class="header">
      <div class="subtitle">{{次标题}}</div>
      <h1 class="main-title">{{主标题}}</h1>
      <div class="author-badge">
        <span>👤</span>
        <span>{{作者名称}}</span>
        <span style="color:#565f89">@{{Handle}}</span>
      </div>
      <!-- 可选警告框 -->
      <div class="notice-box">⚠️ {{说明/警告内容}}</div>
    </header>

    <main class="cards-grid">

      <!-- 卡片 01 -->
      <div class="card">
        <div class="watermark">01</div>
        <div class="card-content">
          <div class="pills">
            <span class="pill">{{关键词1}}</span>
            <span class="pill">{{关键词2}}</span>
          </div>
          <h2 class="card-title">{{卡片标题}}</h2>
          <ul>
            <li>{{要点1}}</li>
            <li>{{要点2}}</li>
            <li>{{要点3}}</li>
          </ul>
        </div>
      </div>

      <!-- 后续卡片按此结构重复，编号递增 -->

    </main>
  </div>
</body>
</html>
```

---

## 处理流程

### 阶段 1：页眉信息提取

- **次标题**：所属分类，大写 + 宽字符间距 (`letter-spacing: 4px`)
- **主标题**：核心产品名，使用科技绿或亮蓝色
- **作者徽章**：头像占位符 + 名称 + Handle 的居中 Flex 胶囊
- **说明/警告框**：暗金色低透明度背景（可选）

### 阶段 2：内容模块拆解

- 梳理长文本，拆分为 **4-8 个核心模块**
- 每个模块对应一个卡片
- 提炼精准、犀利的卡片标题

### 阶段 3：特性胶囊与正文

- **胶囊标签**：2-3 个核心关键词，圆角半透明
- **列表内容**：3-5 条简炼无序列表，禁止大段文字

### 阶段 4：背景水印编号

- 每个卡片分配顺序编号 (01, 02, 03...)
- 巨型水印，绝对定位在卡片右下角底层

---

## 布局地图

```
┌───────────────────────────────────────────┐
│  [次标题 - 宽间距灰色]                      │
│  [主标题 - 科技绿/亮蓝大字]                 │
│  ( 头像 | 作者名称 | @Handle )              │
│  [ ⚠️ 说明/警告框 (暗金低透背景) ]          │
├───────────────────────────────────────────┤
│                                           │
│  ┌──────────────┐ ┌──────────────┐        │
│  │ [胶囊] [胶囊]│ │ [胶囊] [胶囊]│        │
│  │ 卡片标题     │ │ 卡片标题     │        │
│  │ › 列表项     │ │ › 列表项     │        │
│  │ › 列表项   01│ │ › 列表项   02│        │
│  └──────────────┘ └──────────────┘        │
│  ┌──────────────┐ ┌──────────────┐        │
│  │            03│ │            04│        │
│  └──────────────┘ └──────────────┘        │
└───────────────────────────────────────────┘
```

---

## 质量标准

- **层级分明**：`.watermark` (z-index: 0) 不遮挡 `.card-content` (z-index: 1)
- **响应式网格**：桌面端多列 Grid，移动端单列
- **零外部依赖**：HTML 与 CSS 完全内联
- **悬停效果**：卡片 hover 时轻微上移 + 加强辉光
