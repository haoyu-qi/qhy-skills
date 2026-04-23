# 蓝图波普风 (Blueprint Pop Style)

适用于：高密度干货、技术教程、产品选购指南

## 角色定义

顶级信息设计师。擅长将复杂知识转化为实验室精密手册感 + 波普实验风格的高密度干货。

## 视觉哲学

拒绝平庸的手账，追求"数据可视化"的极致美感。参考《字体结构拆解》的精密感与《HBL 30周年》的色彩冲击力。

---

## 工作流程

1. 启动询问 → 深度搜索 → 提炼价值 → 建立坐标体系 → 生成内容 → 精准视觉确认

### 阶段 1：启动询问

向用户询问：
1. **主题**：信息图的核心内容是什么？
2. **描述**：1-2 句话说明核心要点或目标受众
3. **图片数量**：需要制作多少张？（3-10 张）

### 阶段 2：深度搜索

检索高权威信源及专业数据库，提取：
- 价格区间、技术参数、使用寿命
- 占比数据、一线品牌推荐

### 阶段 3：提炼价值

依据以下标准筛选：
- **实用性**：用户可直接落地执行
- **稀缺性**：非泛泛而谈的深度洞察
- **清晰性**：能解决具体痛点

### 阶段 4：视觉坐标拆分

将价值点拆分为 6-7 个核心模块，并分配"视觉坐标"：

```
图片1 → 核心主题：[主题名称]
├─ 坐标 A-01：[4字名称]（品牌阵列/对比区）
├─ 坐标 B-05：[4字名称]（核心参数/刻度区）
├─ 坐标 C-12：[4字名称]（结构拆解/细节图）
```

### 阶段 5：生成高密度内容

每个模块包含：
- 具体品牌名、数值、百分比
- 视觉符号建议（如：180°C、X轴、45度切角）
- 右下角小字 "模板 by WaytoAGI"

---

## 色彩配置

### 蓝图波普调色板

```css
:root {
  /* 背景基底 */
  --bg-blueprint: #F2F2F2;           /* 专业灰白 */
  --bg-blueprint-dark: #E8F4F8;      /* 淡蓝图纸感 */

  /* 系统基色 */
  --systemic-teal: #B8D8BE;          /* 主要功能块、稳定数据区 */
  --systemic-sage: #A8D5BA;          /* 次要功能区 */

  /* 高警报强调 */
  --alert-pink: #E91E63;             /* "陷阱"、"警告"或最重要的"赢家" */
  --alert-coral: #FF6B6B;            /* 次级警告 */

  /* 标记高亮 */
  --marker-yellow: #FFF200;          /* 半透明荧光笔效果 */
  --marker-lime: #CCFF00;            /* 关键词高亮 */

  /* 功能辅助色 */
  --function-blue: #4FC3F7;          /* 结构/流程 */
  --function-orange: #FF9800;        /* 步骤/操作 */
  --function-purple: #9C27B0;        /* 数据/统计 */
}
```

---

## 蓝图网格背景

```css
/* 方法1：CSS 渐变网格（推荐，零依赖） */
.blueprint-bg {
  background-color: #F2F6FA;
  background-image:
    linear-gradient(rgba(74, 144, 226, 0.12) 1px, transparent 1px),
    linear-gradient(90deg, rgba(74, 144, 226, 0.12) 1px, transparent 1px),
    linear-gradient(rgba(74, 144, 226, 0.05) 1px, transparent 1px),
    linear-gradient(90deg, rgba(74, 144, 226, 0.05) 1px, transparent 1px);
  background-size: 40px 40px, 40px 40px, 8px 8px, 8px 8px;
  background-position: -1px -1px, -1px -1px, -1px -1px, -1px -1px;
}

/* 方法2：精细点阵网格 */
.dot-grid-bg {
  background-color: #F8FAFB;
  background-image: radial-gradient(circle, rgba(74,144,226,0.25) 1px, transparent 1px);
  background-size: 20px 20px;
}
```

---

## 剪贴板样式

```css
.clipboard {
  background: white;
  border-radius: 4px;
  box-shadow:
    0 1px 3px rgba(0,0,0,0.12),
    0 4px 6px rgba(0,0,0,0.05),
    inset 0 1px 0 rgba(255,255,255,0.8);
  border: 1px solid #E0E0E0;
  position: relative;
  overflow: hidden;
  padding: 1.5rem;
  margin-bottom: 1rem;
}

/* 回形针效果 */
.clipboard::before {
  content: '';
  position: absolute;
  top: -5px;
  left: 20px;
  width: 30px;
  height: 15px;
  border: 3px solid #888;
  border-bottom: none;
  border-radius: 15px 15px 0 0;
  z-index: 1;
}
```

---

## 坐标系标注规范

```css
/* 坐标标签 */
.coord-label {
  display: inline-block;
  font-family: 'Courier New', monospace;
  font-size: 11px;
  font-weight: bold;
  color: #4A90E2;
  background: rgba(74, 144, 226, 0.1);
  border: 1px solid rgba(74, 144, 226, 0.3);
  padding: 2px 8px;
  border-radius: 3px;
  letter-spacing: 1px;
  margin-bottom: 8px;
}

/* 侧边标签 */
.side-label {
  position: absolute;
  left: -8px;
  top: 50px;
  transform: rotate(-90deg);
  transform-origin: left center;
  background: var(--systemic-teal);
  color: white;
  font-size: 10px;
  font-weight: bold;
  letter-spacing: 2px;
  padding: 4px 12px;
  text-transform: uppercase;
  white-space: nowrap;
}

/* 荧光高亮 */
.highlight-yellow {
  background: var(--marker-yellow);
  padding: 0 4px;
  border-radius: 2px;
}
.highlight-pink {
  background: rgba(233, 30, 99, 0.15);
  color: var(--alert-pink);
  font-weight: bold;
  padding: 0 4px;
}
```

---

## 信息密度布局

```
┌─────────────────────────────────────────────┐
│ [∙∙∙ 点阵背景 ∙∙∙]                           │
│ [侧边标签: COMPARISON]                       │
├─────────────────────────────────────────────┤
│ ┌──────────┐ ┌──────────┐ ┌──────────┐      │
│ │ A-01     │ │ B-02     │ │ C-03     │      │
│ │ 品牌对比 │ │ 核心参数 │ │ 结构拆解 │      │
│ │          │ │          │ │          │      │
│ │ [数据]   │ │ [刻度]   │ │ [图解]   │      │
│ └──────────┘ └──────────┘ └──────────┘      │
├─────────────────────────────────────────────┤
│ ┌───────────────────────────────────────┐   │
│ │ D-04 详细参数对比表                    │   │
│ │ ┌─────┬─────┬─────┬─────┐            │   │
│ │ │参数 │品牌A│品牌B│品牌C│            │   │
│ │ ├─────┼─────┼─────┼─────┤            │   │
│ │ │...  │...  │...  │...  │            │   │
│ │ └─────┴─────┴─────┴─────┘            │   │
│ └───────────────────────────────────────┘   │
├─────────────────────────────────────────────┤
│ ⚠️ 避坑指南 (粉色高亮区域)                   │
├─────────────────────────────────────────────┤
│ ✅ 最终推荐                                  │
└─────────────────────────────────────────────┘
                                模板 by WaytoAGI
```

---

## 质量标准

- 具体数值：必须有具体数字，禁止模糊描述
- 品牌命名：必须使用真实品牌名
- 视觉坐标：每个模块有明确坐标标识
- 风格一致：多图保持剪贴板样式一致
- 网格背景：使用 CSS 渐变生成，不依赖外部资源
