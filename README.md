# qhy-skills

一个面向 Claude Code / Codex 的可扩展技能仓库，围绕中文内容生产与表达，逐步补齐“卡片、演示、图示、文档、文本润色”几类核心能力。

它不是单一的提示词集合，而是一套适合持续扩展的 skill repo：

- 有技能层：每个 skill 独立维护
- 有模板层：新 skill 可以按模板快速复制
- 有工具层：预览、校验、脚手架等公共脚本集中管理

## Why This Repo

- 保留 `qhy-card` 在中文可视化表达上的优势
- 让仓库从单一 HTML 卡片能力，扩展到多种内容交付形态
- 为后续新增 `qhy-*` 技能保留统一结构和命名规范

## Skills

| Skill | Description |
|------|------|
| `qhy-card` | 将内容转为高质量 HTML 视觉卡片，适合信息图、海报页、白板图、周报板。 |
| `qhy-ppt` | 将想法、报告、方案和纪要重组为适合汇报和演示的 PPT / Slide Deck 结构。 |
| `qhy-draw` | 直接生成 draw.io XML，并导出流程图、架构图、UML、ER 图、思维导图和网络拓扑图。 |
| `qhy-word` | 将零散材料整理成可提交、可审阅、可流转的正式文档。 |
| `qhy-humanizer-zh` | 识别并去除中文文本中的 AI 写作痕迹，让表达更自然、更像真人写作。 |
| `qhy-avcon-zentao-iteration` | 为 AVCON/QHY 禅道项目创建或更新五阶段迭代执行与任务清单。 |

## Capability Map

### `qhy-card`

- 面向“看一眼就明白”的视觉表达
- 输出以单文件 HTML 为主
- 更适合封面、信息图、结构白板、周报看板

### `qhy-ppt`

- 面向“讲给别人听”的演示表达
- 输出以多页 HTML deck、逐页文案、讲稿备注结构为主
- 更适合汇报、提案、培训、路演

### `qhy-draw`

- 面向“把关系画清楚”的 draw.io 图示表达
- 输出以 `.drawio` 源文件为主，可通过 draw.io Desktop CLI 导出 PNG / SVG / PDF
- 更适合流程图、架构图、UML 时序/类图、ER 图、思维导图、网络拓扑图

### `qhy-word`

- 面向“形成正式文档”的书面表达
- 输出以提纲、正文、章节草稿、修订建议为主
- 更适合方案、报告、纪要、说明文

### `qhy-humanizer-zh`

- 面向“去掉 AI 味”的文本润色
- 识别宣传腔、空泛归因、三段式排比、过度连接词等常见 AI 写作痕迹
- 更适合文章、文案、报告段落、对外说明的自然化改写

### `qhy-avcon-zentao-iteration`

- 面向“把软件迭代落到禅道任务”的项目执行表达
- 固定创建概念、计划、开发、验证、发布五个父阶段
- 开发阶段子任务优先对齐需求文档中的模块、功能点、页面、接口和交付物
- 更适合 AVCON/QHY 月度迭代、版本执行、需求落地和任务模板复用

## qhy-card Highlights

### 模式

| 参数 | 模式 | 适合场景 |
|------|------|------|
| `-i` | 信息图 | 一图看懂、概念拆解、项目总览 |
| `-p` | 海报页 | 汇报封面、观点表达、活动预告 |
| `-w` | 白板图 | 流程、关系、框架、结构解释 |
| `-r` | 周报板 | 周报、月报、项目推进看板 |

### 输出

- HTML 单文件
- 内联 CSS
- 默认零外部依赖
- 可选 JSON 结构草稿

## Example Outputs

仓库中已包含若干 `qhy-card` 示例：

- [项目推进看板示例](examples/qhy-card-priority-board.html)
- [汇报 Deck 示例](examples/qhy-card-priority-deck.html)
- [AI 路线图示例](examples/qhy-card-ai-roadmap-board.html)

也可以直接查看 [examples/README.md](examples/README.md) 获取示例导航与使用建议。

## Install

```bash
git clone https://github.com/haoyu-qi/qhy-skills.git ~/.claude/plugins/qhy-skills
```

然后重启 Claude Code / Codex。

当前技能以文本工作流为主，不强依赖 Node。现有公共脚本重点服务 `qhy-card` 的 HTML 预览、检查和脚手架。

## Quick Start

可以直接这样使用：

```text
请用 qhy-card 生成一张信息图
主题：MCP、Skill、Plugin 三者的区别
要求：中文、信息密集、宽一点
```

```text
请用 qhy-ppt 把下面这份项目周报整理成 8 页以内的汇报 deck
受众：老板
目标：同步进展并争取资源
```

```text
请用 qhy-draw 画一个电商下单流程图，并导出 PNG
```

```text
请用 qhy-word 把这些会议纪要整理成正式纪要，并补一个待办清单
```

```text
请用 qhy-humanizer-zh 把下面这段话改得更自然，去掉 AI 味
```

```text
请用 qhy-avcon-zentao-iteration 为 X86 客户端创建 6 月禅道迭代，并按需求文档生成开发阶段子任务
```

## Scripts

```bash
bash scripts/new-card.sh
bash scripts/quality-check.sh output.html
bash scripts/preview.sh output.html
```

## Collaboration

仓库已经补充基础协作模板：

- Bug 报告：`.github/ISSUE_TEMPLATE/bug-report.md`
- 能力提案：`.github/ISSUE_TEMPLATE/feature-request.md`
- PR 模板：`.github/pull_request_template.md`

如果你准备继续扩展 skill、模板或脚本，建议先看 [CONTRIBUTING.md](CONTRIBUTING.md)。

## Repo Layout

```text
qhy-skills/
├── .claude-plugin/          # 插件元数据
├── docs/                    # 架构与仓库级说明
├── examples/                # 示例输出
├── scripts/                 # 多 skill 共用脚本
└── skills/
    ├── README.md            # skills 目录说明
    ├── _template/           # 新 skill 模板
    ├── qhy-avcon-zentao-iteration/ # 禅道软件迭代任务模板
    ├── qhy-card/            # HTML 卡片能力
    ├── qhy-ppt/             # 演示文稿能力
    ├── qhy-draw/            # draw.io 图表生成能力
    ├── qhy-word/            # 正式文档能力
    ├── qhy-humanizer-zh/    # 中文文本去 AI 味
    └── qhy-avcon-zentao-iteration/ # AVCON/QHY 禅道迭代任务模板
```

## Multi-Skill Expansion

后续新增 skill 时，推荐遵循这套结构：

- 每个 skill 放在 `skills/<skill-name>/`
- 每个 skill 至少包含 `SKILL.md`
- 知识规则放 `references/`
- 模板与静态资产放 `assets/`
- skill 专属脚本放 `scripts/`
- 公共工具继续放根目录 `scripts/`

建议直接从 [skills/_template](skills/_template) 开始。

## Compared To The Original infographic-card

- 从单技能项目升级为多 skill 仓库
- 从“只有风格”升级为“模块 + 风格 + 审美准则 + 多表达形态”
- 增加模板骨架，减少输出漂移
- 增加脚手架、质检和示例输出
- 补齐 `qhy-ppt`、`qhy-draw`、`qhy-word`、`qhy-humanizer-zh`、`qhy-avcon-zentao-iteration` 等方向的基础能力

## License

MIT
