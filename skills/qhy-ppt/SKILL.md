---
name: qhy-ppt
description: |
  将大纲、长文、会议纪要、方案说明、课程内容或汇报材料转成多页 HTML 演示文稿。适用于需要“PPT / slides / deck / keynote / 幻灯片 / 演讲稿 / 分享稿 / 路演 / 周报 deck / 小红书图文 / 培训课件”等多页输出的场景，尤其适合中文内容、单文件 HTML、可离线预览、可继续人工修改的交付方式。

  当用户要做技术分享、产品发布、投资人 pitch、周报回顾、课程模块、小红书图文，或明确提到“演讲者备注 / speaker notes / 逐字稿 / 提词器”时，优先使用这个 skill，而不是单页的 qhy-card。
---

# qhy-ppt

面向多页 HTML 演示文稿的 skill。目标不是“做一个像 PPT 的网页”，而是把内容组织成真正可讲、可翻页、可分享、可后续修改的 deck。

## 核心原则

1. 先定叙事，再定样式，再写页面。
2. 优先输出单文件 HTML，默认内联 CSS 和必要 JS，保证离线打开可用。
3. 每一页只讲一个动作：开场、解释、对比、证明、计划、收尾。
4. 演讲者备注只能放进 `.notes`，不要把提示词写进观众可见区域。
5. 优先复用 `assets/deck-starter.html` 的结构，不要从空白页硬写。

## 执行顺序

生成前按顺序读取：

1. `references/quality-bar.md`
2. `references/workflow.md`
3. 先用 `references/structure.md` 确定推进逻辑
4. 再读 `references/presentation-style.md` 对齐中文汇报语气
5. 按任务类型读取 `references/deck-patterns.md`
6. 按页面需要读取 `references/page-patterns.md` 与 `references/slide-patterns.md`
7. 需要推荐视觉方向时读取 `references/theme-guide.md`
8. 涉及演讲、分享、讲稿、speaker notes 时读取 `references/presenter-notes.md`
9. 使用 `assets/deck-starter.html` 作为骨架起步

## 什么时候直接开始，什么时候先确认

如果用户已经给了完整材料，可以直接做，并在开始前用一句话说明你的默认判断：

- 受众是谁
- 预计页数
- 视觉方向
- 是否需要备注

只有这四项里有明显风险时，才先询问。默认优先给出 2 到 3 个主题或模板建议，而不是把所有选项都摊给用户。

## 场景映射

| 用户意图 | 优先 deck 类型 | 必读参考 |
|---|---|---|
| 技术分享 / 内部分享 / 架构讲解 | `tech-sharing` | `deck-patterns.md` `slide-patterns.md` `presenter-notes.md` |
| 产品发布 / 功能发布 / 发布会 | `product-launch` | `deck-patterns.md` `theme-guide.md` |
| 投资人路演 / 商业 pitch | `pitch-deck` | `deck-patterns.md` `theme-guide.md` |
| 周报 / 月报 / 复盘 | `weekly-report` | `deck-patterns.md` `slide-patterns.md` |
| 课程 / 培训 / 工作坊 | `course-module` | `deck-patterns.md` `presenter-notes.md` |
| 小红书图文 / 轮播图文 | `xhs-post` | `deck-patterns.md` `theme-guide.md` |

## 输出规范

### 必须做

- 输出完整 HTML，而不是只给提纲
- 使用 `.slide` 作为每页容器
- 包含 `<meta charset="UTF-8">` 和 viewport
- 包含基本翻页逻辑，至少支持左右键
- 每页有清晰标题层级，不靠堆字形成“信息页”
- 移动端至少保证可滚动阅读，不出现严重溢出
- 如果用户要演讲稿，在每页底部补 `.notes`

### 禁止做

- 不要默认做成单页长图
- 不要把所有页都做成“标题 + 三栏卡片”
- 不要依赖远程图片、远程字体或在线构建
- 不要把演讲提示语直接写在可见正文里
- 不要为炫技加入大量无意义动效

## 辅助脚本

优先使用：

- `scripts/new-deck.ps1` 或 `scripts/new-deck.sh`：从基础 deck 模板脚手架新演示
- `scripts/render.ps1` 或 `scripts/render.sh`：将 deck 渲染成单张或逐页 PNG 预览

## 默认结构约定

- 外层：`.deck`
- 页面：`.slide`
- 页眉信息：`.eyebrow` / `.meta`
- 主标题：`h1` 或 `h2`
- 主体内容区：`.grid` / `.panel` / `.stats` / `.timeline` 等语义容器
- 演讲备注：`.notes`

## 自检清单

- [ ] 页数和叙事节奏匹配，没有明显水页或挤页
- [ ] 封面、正文、收尾风格一致
- [ ] 数据页和概念页区分清楚
- [ ] 每页只保留一个主锚点
- [ ] 没有把备注写进观众视图
- [ ] HTML 离线可打开，键盘翻页可用
