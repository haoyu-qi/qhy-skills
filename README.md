# qhy-skills

面向 Claude Code 与 Codex 的中文技能集合，覆盖视觉内容、演示文稿、图示、正式文档、文本润色、邮件、表格整理和研发协作。

每个 skill 都是独立、可维护的工作单元：`SKILL.md` 定义触发条件与执行规则，`references/` 保存领域规范，`assets/` 提供模板素材，`scripts/` 承担可重复执行的本地工具。

## 技能总览

当前仓库包含 11 个技能。点击技能名可查看完整规则。

| 类别 | Skill | 适合处理 | 主要交付物 |
|---|---|---|---|
| 视觉内容 | [`qhy-card`](skills/qhy-card/SKILL.md) | 将复杂内容整理成信息图、海报页、结构白板或周报看板 | 单文件 HTML，可选 JSON 草稿 |
| 视觉内容 | [`qhy-ppt`](skills/qhy-ppt/SKILL.md) | 制作中文汇报、提案、培训、发布会和路演演示 | 可横向翻页的单文件 HTML deck |
| 视觉内容 | [`qhy-photo`](skills/qhy-photo/SKILL.md) | 将照片或场景编辑为纸刊海报、实景拼贴、抽象记忆面板或场景蒸馏插画 | 图片作品或可复用生图提示词 |
| 视觉内容 | [`qhy-picture`](skills/qhy-picture/SKILL.md) | 为公众号、博客、方法论和技术解读文章设计彩色手绘动画风格的正文配图 | 16:9 横版配图、shot list 或成组提示词 |
| 图示表达 | [`qhy-draw`](skills/qhy-draw/SKILL.md) | 绘制流程图、架构图、UML、ER 图、思维导图和网络拓扑 | `.drawio` 源文件及 PNG / SVG / PDF |
| 图示表达 | [`qhy-draw-gif`](skills/qhy-draw-gif/SKILL.md) | 制作动态架构图、流程动图和黑底手绘技术图解 | GIF、PNG 与可编辑 `.excalidraw` |
| 文本与文档 | [`qhy-word`](skills/qhy-word/SKILL.md) | 把想法、草稿或纪要整理成方案、报告、说明文和正式纪要 | 提纲、完整正文、章节草稿或修订建议 |
| 文本与文档 | [`qhy-humanizer-zh`](skills/qhy-humanizer-zh/SKILL.md) | 在保留作者立场和口吻的前提下，减少中文文本的 AI 写作痕迹 | 自然化改稿与必要的修改说明 |
| 沟通协作 | [`qhy-mail`](skills/qhy-mail/SKILL.md) | 起草、润色、回复或转发业务邮件，并生成 HTML 卡片正文 | HTML / 纯文本邮件草稿；确认后发送 |
| 研发协作 | [`qhy-bug-xlsx`](skills/qhy-bug-xlsx/SKILL.md) | 清洗禅道导出的 `.xlsx`、`.xls` 或 `.csv` Bug 列表 | 含总览、全部明细、T0 明细的整理表 |
| 研发协作 | [`qhy-avcon-zentao-iteration`](skills/qhy-avcon-zentao-iteration/SKILL.md) | 按 AVCON/QHY 五阶段模板创建或更新禅道迭代与任务 | 迭代执行、父阶段及需求关联子任务 |

## 怎么选择

- 内容需要“一眼看懂”，选 `qhy-card`；需要多页讲述，选 `qhy-ppt`。
- 以真实照片为起点做编辑创作，选 `qhy-photo`；为中文文章制作成组正文配图，选 `qhy-picture`。
- 需要标准可编辑图表，选 `qhy-draw`；需要动态讲解，选 `qhy-draw-gif`。
- 需要从零组织正式文档，选 `qhy-word`；已有文本只想去掉 AI 味，选 `qhy-humanizer-zh`。
- 需要处理实际邮件、Bug 表或禅道迭代，分别选 `qhy-mail`、`qhy-bug-xlsx`、`qhy-avcon-zentao-iteration`。

## 安装

### Claude Code

```bash
git clone https://github.com/haoyu-qi/qhy-skills.git ~/.claude/plugins/qhy-skills
```

克隆完成后重启 Claude Code。

### Codex

将需要的 `skills/qhy-*` 目录复制或链接到 `~/.codex/skills/`，然后重新启动 Codex。例如：

```bash
git clone https://github.com/haoyu-qi/qhy-skills.git ~/.codex/qhy-skills
cp -R ~/.codex/qhy-skills/skills/qhy-* ~/.codex/skills/
```

更新仓库后，如果使用的是复制安装，需要再次同步对应技能目录；使用目录链接则会随仓库更新生效。

## 快速开始

在对话中直接点名技能并说明目标、材料、受众和输出要求即可。

```text
请用 qhy-card 把下面的版本更新整理成一张中文信息图，输出单文件 HTML。
```

```text
请用 qhy-photo 保留这张照片的真实人物和环境，把它编辑成留白克制的纸刊海报。
```

```text
请用 qhy-picture 分析这篇中文文章，生成一组风格一致的 16:9 彩色手绘正文配图。
```

```text
请用 qhy-draw 画一个电商下单流程图，保留 .drawio 源文件并导出 PNG。
```

```text
请用 qhy-word 把这些会议记录整理成正式纪要，单独列出结论、待办、负责人和时间点。
```

```text
请用 qhy-bug-xlsx 整理这份禅道 bug-list，输出总览、全部明细和 T0 明细。
```

多个技能也可以串联使用，例如先用 `qhy-word` 整理内容，再用 `qhy-ppt` 生成汇报 deck，或先用 `qhy-draw` 固化架构，再用 `qhy-draw-gif` 制作动态讲解版。

## 运行条件

大部分技能以规则、模板和本地文件为主，不要求统一安装运行时。以下能力有额外条件：

| Skill | 条件 |
|---|---|
| `qhy-draw` | 导出 PNG / SVG / PDF 时需要 draw.io Desktop CLI；仅生成 `.drawio` 不受影响 |
| `qhy-draw-gif` | 内置渲染器需要 Python 3.9+ 与 `Pillow>=10.0.0` |
| `qhy-bug-xlsx` | 整理脚本需要 Node.js 与仓库指定的表格依赖 |
| `qhy-mail` | 实际发送依赖已配置的 `mail-skill` 与邮箱账号；任何发送、回复、转发都必须先人工确认 |
| `qhy-avcon-zentao-iteration` | 写入禅道依赖已配置的 ZenTao CLI；认证信息由 CLI 管理 |

## 仓库结构

```text
qhy-skills/
├── .claude-plugin/             # Claude 插件元数据
├── .github/                    # Issue 与 PR 模板
├── docs/                       # 仓库架构说明
├── examples/                   # 代表性输出示例
├── scripts/                    # 跨技能复用的工具
├── tests/                      # 仓库级验证
└── skills/
    ├── _template/              # 新技能模板
    ├── qhy-card/
    ├── qhy-ppt/
    ├── qhy-photo/
    ├── qhy-picture/
    ├── qhy-draw/
    ├── qhy-draw-gif/
    ├── qhy-word/
    ├── qhy-humanizer-zh/
    ├── qhy-mail/
    ├── qhy-bug-xlsx/
    └── qhy-avcon-zentao-iteration/
```

单个技能通常采用以下结构：

```text
skills/qhy-<name>/
├── SKILL.md                    # 必需：用途、触发条件、工作流与边界
├── references/                # 可选：规则、模式与知识参考
├── assets/                    # 可选：模板与静态素材
└── scripts/                   # 可选：技能专属脚本
```

## 辅助脚本

根目录脚本当前主要服务 HTML 卡片的创建、检查和预览：

```bash
bash scripts/new-card.sh
bash scripts/quality-check.sh output.html
bash scripts/preview.sh output.html
```

详细说明见 [`scripts/README.md`](scripts/README.md)，代表性产出见 [`examples/README.md`](examples/README.md)。

## 扩展与贡献

新增技能时：

1. 复制 `skills/_template/`，重命名为 `skills/qhy-<name>/`。
2. 先完善 `SKILL.md`，明确用途、触发场景、输入输出、执行顺序和边界。
3. 按需补充 `references/`、`assets/`、`scripts/` 与代表性示例。
4. 更新本 README 的技能总览、运行条件和仓库结构。
5. 按 [`CONTRIBUTING.md`](CONTRIBUTING.md) 完成检查并提交变更。

技能行为以各目录内的 `SKILL.md` 为准，README 只维护导航和简要定位。

## License

MIT

