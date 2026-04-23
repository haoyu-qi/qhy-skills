# 纯白演示风 (White Presentation Style)

适用于：季度软件更新、演示文稿、投屏展示

## 角色定义

资深前端开发工程师与数据可视化演示专家。擅长采用极简、高对比度的纯白模式（High-Contrast White），将高密度数据转化为 16:9 HTML 幻灯片页面。

---

## 核心布局配置

### 16:9 分页容器

```css
body {
  background-color: #F5F5F7;  /* 极浅灰色区分页面边界 */
}

.slide {
  aspect-ratio: 16 / 9;
  max-width: 1280px;
  background: #FFFFFF;
  padding: 40px 60px;
  position: relative;
  margin: 2rem auto;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
}
```

### 打印支持

```css
@media print {
  body { background: white; }
  .slide {
    page-break-after: always;
    box-shadow: none;
    margin: 0;
  }
}
```

---

## 色彩系统

### 区块标题色

```css
.header-blue { background: #007BFF; }
.header-magenta { background: #C06B9A; }
.header-black { background: #1A1A1A; }
```

### 文字高亮色

```css
.text-green-data { color: #00B37A; font-weight: 700; }   /* 增长/特性 */
.text-red-data { color: #E63946; font-weight: 700; }     /* 风险/修复 */
.text-blue-concept { color: #007BFF; font-weight: 700; } /* 术语/版本 */
```

---

## 处理流程

### 阶段 1：全局布局与分页

- 取消传统长图布局
- 创建多个 `<section class="slide">` 作为每一页
- 包含 `@media print` 样式

### 阶段 2：封面页

```html
<section class="slide cover">
  <h1 class="version-title">v2.6.2</h1>
  <p class="release-date">2026.03.19</p>
  <p class="slogan">核心 Slogan</p>

  <!-- 系统状态栏（核心强制） -->
  <div class="system-status">
    <span>Runtime: v2.6.2 Stable</span>
    <span>Agent Status: <span class="status-dot">●</span> Online</span>
    <span>Processed by AI-小齐</span>
  </div>
</section>
```

### 状态栏样式

```css
.system-status {
  position: absolute;
  bottom: 30px;
  width: calc(100% - 120px);
  display: flex;
  justify-content: space-between;
  font-family: monospace;
  color: #888;
  font-size: 14px;
  border-top: 1px solid #E0E0E0;
  padding-top: 15px;
}

.status-dot {
  color: #00B37A;
}
```

### 阶段 3：按端分页

每个终端单独占用一个 `<section class="slide">`：
- Web 端
- 移动端
- 服务端

### 阶段 4：实色区块标题

```css
.section-header {
  color: white;
  padding: 8px 16px;
  border-radius: 4px;
  font-weight: bold;
  font-size: 1.1rem;
  margin-bottom: 1.5rem;
}
```

### 阶段 5：网格组织

```css
.content-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}
```

### 阶段 6：高饱和度数据高亮

在正文 `<p>` 标签内使用高亮类：
- 版本号与关键指标
- 核心技术栈或新特性名称
- 修复的重大 Bug

---

## 排版规范

| 元素 | 字号 | 字重 |
|------|------|------|
| 封面标题 | 64px | 800 |
| 页眉 | 24px | bold |
| H3 区块标题 | - | bold |
| 正文 | - | line-height: 1.6 |

---

## 输出结构

```
┌─────────────────────────────────────┐
│ Slide 1: 封面                       │
│ - 巨大版本号                        │
│ - 发布日期                          │
│ - 核心 Slogan                       │
│ - 系统状态栏（底部）                │
├─────────────────────────────────────┤
│ Slide 2: Web 端更新                 │
│ - 页眉：季度更新 / Web 前端         │
│ - 实色区块标题 + 内容网格           │
├─────────────────────────────────────┤
│ Slide 3: 移动端更新                 │
│ - 页眉：季度更新 / 移动端           │
│ - 实色区块标题 + 内容网格           │
├─────────────────────────────────────┤
│ Slide 4: 服务端更新                 │
│ - 页眉：季度更新 / 服务端           │
│ - 实色区块标题 + 内容网格           │
└─────────────────────────────────────┘
```

---

## 质量标准

- 结构极简：内部完全依赖排版对比、实色标题块、文字高亮
- 内部严禁使用任何卡片阴影或灰色背景模块
- 仅 `.slide` 容器自带阴影区分
- 所有 CSS 内嵌在 `<style>` 标签中
- 完整包含 `@media print` 媒体查询
