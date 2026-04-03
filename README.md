# qhy-skills

一个支持持续扩展的 Claude Code 技能仓库。它以 `qhy-card` 为起点，已经从单技能项目升级成多 skill 友好的仓库骨架，方便后续继续封装更多 `qhy-*` 技能。

## 设计目标

- 保留 `infographic-card` 擅长的中文信息图与 HTML 单文件输出
- 借鉴 `ljg-card` 的长处，把“单一风格生成器”升级成“有模具、有审美底线、有模板骨架”的技能
- 继续坚持零外部依赖 HTML，方便直接预览、分享、二次编辑

## 技能总览

| 技能 | 说明 |
|------|------|
| `qhy-card` | 将内容转为高质量 HTML 视觉卡片。支持信息图、海报、白板结构图、周报看板四类模具，并保留 7 种中文视觉风格。 |
| `qhy-<new-skill>` | 预留扩展位。后续新技能建议统一采用 `qhy-*` 命名，并按模板目录创建。 |

## 扩展方式

- 每个 skill 放在 `skills/<skill-name>/`
- 每个 skill 至少包含 `SKILL.md`
- 有额外知识时放 `references/`
- 有模板、素材或骨架时放 `assets/`
- 有 skill 专属脚本时放 `scripts/`
- 共用工具继续放仓库根目录 `scripts/`

建议优先使用模板目录 [skills/_template](/Users/qijingchun/Documents/qhy-card/qhy-skills/skills/_template) 作为新 skill 起点。

## qhy-card 能力概览

### 模具

| 参数 | 模具 | 说明 |
|------|------|------|
| `-i` | 信息图 | 自适应信息密度和非对称布局，适合“一图看懂”类内容 |
| `-p` | 海报页 | 更强调封面感和传播感，适合活动预告、发布说明、观点海报 |
| `-w` | 白板图 | 强调结构关系、箭头与标注，适合教程、流程、拆解 |
| `-r` | 周报板 | 面向团队周报、月报和进展看板 |

### 视觉风格

- 默认由模型根据内容自动选择
- 也支持先给用户 2 到 4 个候选方向，让用户交互式挑选
- 暗黑科技风
- 扁平现代风
- 杂志质感风
- 复古书卷风
- 蓝图波普风
- 纯白演示风
- 周报模块风

### 输出

- HTML 单文件
- 内联 CSS
- 默认零外部依赖
- 可选输出结构化 JSON 草稿

## 安装

```bash
git clone https://github.com/haoyu-qi/qhy-skills.git ~/.claude/plugins/qhy-skills
```

然后重启 Claude Code。

如果后续为截图或批量导出补充了本地渲染工具，可运行：

```bash
cd ~/.claude/plugins/qhy-skills && bash scripts/install.sh
```

当前仓库的脚本以 HTML 预览、校验和提示词脚手架为主，不强依赖 Node。

## 快速使用

直接向 Claude 发送：

```text
请用 qhy-card 生成一张信息图。
模具：信息图
主题：MCP、Skill、Plugin 三者的区别
要求：信息密集、中文字体、宽一点
```

如果你想让模型先给候选风格，也可以这样用：

```text
请用 qhy-card 做一张卡片。
先别直接生成，先根据内容给我 3 个合适的风格方向，我选一个再出图。
主题：AI 编码工具的工作流差异
```

或者运行脚手架：

```bash
bash scripts/new-card.sh
```

## 辅助脚本

```bash
bash scripts/new-card.sh
bash scripts/quality-check.sh output.html
bash scripts/preview.sh output.html
```

## 多 Skill 规范

- 命名统一用 `qhy-*`
- README 只做仓库级导航，不把单个 skill 的细节塞满首页
- 每个 skill 自己维护独立的 `SKILL.md`
- 可复用规范优先沉淀到模板和公共文档，而不是复制粘贴到每个 skill
- 新增 skill 时优先复用 [skills/_template/SKILL.md](/Users/qijingchun/Documents/qhy-card/qhy-skills/skills/_template/SKILL.md) 和 [skills/README.md](/Users/qijingchun/Documents/qhy-card/qhy-skills/skills/README.md)

## 仓库结构

```text
qhy-skills/
├── .claude-plugin/
│   ├── marketplace.json
│   └── plugin.json
├── docs/
│   └── architecture.md
├── README.md
├── scripts/
│   ├── install.sh
│   ├── new-card.sh
│   ├── preview.sh
│   ├── quality-check.sh
│   └── README.md
└── skills/
    ├── README.md
    ├── _template/
    │   ├── SKILL.md
    │   ├── assets/
    │   │   └── README.md
    │   ├── references/
    │   │   └── README.md
    │   └── scripts/
    │       └── README.md
    └── qhy-card/
        ├── SKILL.md
        ├── assets/
        │   ├── infograph_template.html
        │   ├── poster_template.html
        │   └── whiteboard_template.html
        └── references/
            ├── taste.md
            ├── mode-infograph.md
            ├── mode-poster.md
            ├── mode-whiteboard.md
            ├── dark-tech.md
            ├── flat-modern.md
            ├── magazine.md
            ├── vintage-book.md
            ├── blueprint-pop.md
            ├── white-presentation.md
            └── weekly-report.md
```

## 与原版 infographic-card 的区别

- 从单技能仓库升级为技能集合仓库命名和目录结构
- 从“只有风格”升级为“模具 + 风格 + 审美准则”的三层设计
- 增加模板骨架，减少每次从零生成时的漂移
- 增加更明确的工作流脚手架和更严格的输出质检
- 预留多 skill 扩展模板和架构文档，方便后续继续封装

## License

MIT
