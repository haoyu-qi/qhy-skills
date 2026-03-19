# 扁平现代风 (Flat Modern Style)

适用于：AI 产品宣传、技术指标展示

## 角色定义

信息图可视化设计师与信息架构师。擅长以扁平化、现代的设计语言，从技术宣传图中提炼核心信息结构。

---

## 核心视觉配置

### 色彩系统

```css
:root {
  --primary-blue-bg: #ECF3FD;
  --card-grey-bg: #F7F7F9;
  --theme-green-bg: #19C171;
  --accent-red: #DC3545;
  --accent-green: #28A745;
  --accent-purple: #6F42C1;
  --text-dark: #333;
  --text-muted: #666;
}
```

### 卡片配置

```css
.card {
  background-color: var(--card-grey-bg);
  border-radius: 12px;
  padding: 1.5rem;
  position: relative;
  overflow: hidden;
}

.card-blue { background-color: var(--primary-blue-bg); }
.card-green { background-color: var(--theme-green-bg); color: white; }
```

### 大背景数字/百分比

```css
.bg-text {
  position: absolute;
  opacity: 0.1;
  font-weight: 800;
  z-content: -1;
}
.bg-score { font-size: 15rem; top: -2rem; right: -2rem; }
.bg-label { font-size: 12rem; bottom: -3rem; right: -1rem; }
.bg-index { font-size: 10rem; top: -2rem; right: -1.5rem; }
```

### 网格布局

```css
.row-3-1 { display: flex; gap: 1rem; }
.row-3-1 .card { flex: 1; }
.grid-2x1 { display: grid; grid-template-columns: repeat(2, 1fr); gap: 1.5rem; }
```

---

## 处理流程

### 阶段 1：页眉信息提取

- **公司/日期**：小字，灰调
- **主标题**：非常粗，大字
- **副标题**：全大写，小字

### 阶段 2：模型描述卡片

- 深蓝色卡片背景
- 标题 + 描述（强调关键术语）

### 阶段 3：功能卡片（3 个）

每个卡片包含：
- 共同灰色背景
- 大背景数字 (01, 02, 03)
- 标题
- 全大写副标题
- 描述

### 阶段 4：成绩卡片（2 行 4 个）

每个卡片包含：
- 大背景百分比
- 英文标题
- 中文副标题
- 彩色标签 (红色 SOTA / 紫色当前最高分 / 绿色超越)
- 描述

### 阶段 5：技术规范（2 个）

- 大背景标签 (如 1T / 256K)
- 标题 + 副标题
- 项目符号列表

### 阶段 6：应用场景（3 个）

- 大背景图标
- 标题 + 描述

### 阶段 7：页脚 (CTA)

- 绿色背景
- 粗体白色标题
- 步骤列表

---

## 布局地图

```
┌─────────────────────────────────────┐
│  [Header: Company | Title | Subtitle]│
├─────────────────────────────────────┤
│  [Model Description Card - Blue]    │
├─────────────────────────────────────┤
│  [Feature Cards Row (3 x 1)]        │
├─────────────────────────────────────┤
│  [Score Cards Row 1 (2 x 1)]        │
├─────────────────────────────────────┤
│  [Score Cards Row 2 (2 x 1)]        │
├─────────────────────────────────────┤
│  [Technical Specs Row (2 x 1)]      │
├─────────────────────────────────────┤
│  [Use Case Cards Row (3 x 1)]       │
├─────────────────────────────────────┤
│  [Footer CTA Card - Green]          │
└─────────────────────────────────────┘
```

---

## 标签色彩映射

| 含义 | 颜色 | CSS 类 |
|------|------|--------|
| SOTA/最优 | 红色 | `.tag-red` |
| 当前最高分 | 紫色 | `.tag-purple` |
| 超越竞品 | 绿色 | `.tag-green` |
