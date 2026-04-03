# qhy-skills

一个面向 Claude Code 的可扩展技能仓库，当前以 `qhy-card` 为核心，主打中文内容可视化、HTML 卡片生成和多 skill 结构化扩展。

它不是单一的“信息图提示词集合”，而是一套适合继续长大的 skill repo：

- 有技能层：每个 skill 独立维护
- 有模板层：新 skill 可以按模板快速复制
- 有工具层：预览、校验、脚手架等公共脚本集中管理

## Why This Repo

- 从 `infographic-card` 演进而来，保留中文信息图和 HTML 单文件输出能力
- 吸收了更成熟的技能仓库组织方式，把项目升级成多 skill 友好结构
- 默认零外部依赖，生成结果便于预览、分享和二次修改

## Skills

| Skill | Description |
|------|------|
| `qhy-card` | 将内容转为高质量 HTML 视觉卡片，支持信息图、海报页、白板图、周报板四类模具。 |
| `qhy-<new-skill>` | 预留扩展位。后续新技能建议统一使用 `qhy-*` 命名。 |

## qhy-card Highlights

### 模具

| 参数 | 模具 | 适合场景 |
|------|------|------|
| `-i` | 信息图 | 一图看懂、概念拆解、项目总览 |
| `-p` | 海报页 | 汇报封面、观点表达、活动预告 |
| `-w` | 白板图 | 流程、关系、框架、结构解释 |
| `-r` | 周报板 | 周报、月报、项目推进看板 |

### 风格

- 暗黑科技风
- 扁平现代风
- 杂志质感风
- 复古书卷风
- 蓝图波普风
- 纯白演示风
- 周报模块风

默认由模型根据内容自动选择风格，也支持先给用户 2 到 4 个候选方向再交互选择。

### 输出

- HTML 单文件
- 内联 CSS
- 默认零外部依赖
- 可选 JSON 结构草稿

## Example Outputs

仓库里已经包含两个示例：

- [项目推进看板示例](examples/qhy-card-priority-board.html)
- [汇报 Deck 示例](examples/qhy-card-priority-deck.html)

## Install

```bash
git clone https://github.com/haoyu-qi/qhy-skills.git ~/.claude/plugins/qhy-skills
```

然后重启 Claude Code。

当前仓库的运行重点是 HTML 预览、检查和脚手架，不强依赖 Node。

## Quick Start

直接给 Claude：

```text
请用 qhy-card 生成一张信息图。
模具：信息图
主题：MCP、Skill、Plugin 三者的区别
要求：信息密集、中文字体、宽一点
```

如果你想先挑风格：

```text
请用 qhy-card 做一张卡片。
先别直接生成，先根据内容给我 3 个合适的风格方向，我选一个再出图。
主题：AI 编码工具的工作流差异
```

或者使用脚手架：

```bash
bash scripts/new-card.sh
```

## Scripts

```bash
bash scripts/new-card.sh
bash scripts/quality-check.sh output.html
bash scripts/preview.sh output.html
```

## Repo Layout

```text
qhy-skills/
├── .claude-plugin/          # 插件元数据
├── docs/                    # 架构与仓库级说明
├── examples/                # 示例 HTML 输出
├── scripts/                 # 多 skill 共用脚本
└── skills/
    ├── README.md            # skills 目录说明
    ├── _template/           # 新 skill 模板
    └── qhy-card/            # 当前主技能
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

更完整的仓库分层说明见：

- [架构文档](docs/architecture.md)
- [skills 目录说明](skills/README.md)

## Compared To The Original infographic-card

- 从单技能项目升级为多 skill 仓库
- 从“只有风格”升级为“模具 + 风格 + 审美准则”
- 增加模板骨架，减少输出漂移
- 增加脚手架、质检和示例输出
- 预留了可持续扩展的新 skill 模板

## License

MIT
