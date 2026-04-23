# Contributing

欢迎继续扩展 `qhy-skills`。

这个仓库当前的目标不是一次性塞满所有能力，而是把每个 skill 做成清晰、独立、可维护的模块。

## 基本原则

- 一个 skill 只解决一类明确问题
- 尽量复用仓库已有模板和公共脚本
- 优先写清楚规则和边界，再增加素材和脚本
- 示例输出应尽量真实，不要只放占位内容

## 新增 Skill 的推荐流程

1. 从 `skills/_template/` 复制一个新目录
2. 重命名为 `skills/qhy-<name>/`
3. 完成 `SKILL.md`
4. 按需补充 `references/`、`assets/`、`scripts/`
5. 更新根目录 `README.md` 中的技能列表
6. 如有代表性产出，可在 `examples/` 增加示例

## 目录约定

- `skills/<skill-name>/SKILL.md`
  说明 skill 的用途、触发场景、输入输出、执行顺序和规则
- `skills/<skill-name>/references/`
  放风格、知识、规则、模式文档
- `skills/<skill-name>/assets/`
  放模板、静态资源、示例骨架
- `skills/<skill-name>/scripts/`
  仅放这个 skill 自己专用的脚本
- `scripts/`
  放多个 skills 共用的工具

## 命名规范

- 新技能统一使用 `qhy-*`
- skill 名尽量表达能力，不要只表达技术实现
- 示例文件名尽量能看出内容类型，例如 `qhy-card-priority-board.html`

## 提交建议

- 一个 commit 尽量只完成一类改动
- 文档、模板、脚本混改时，commit message 要能说明变化意图
- 若新增 skill，建议在 commit message 里直接写出 skill 名
- 提交 PR 时，优先按 `.github/pull_request_template.md` 补齐变更背景、验证方式和注意事项

## Issue / PR 模板

- 提 bug 时优先使用 `.github/ISSUE_TEMPLATE/bug-report.md`
- 提新能力时优先使用 `.github/ISSUE_TEMPLATE/feature-request.md`
- 提 PR 时使用 `.github/pull_request_template.md`

## 质量检查

如果改动涉及 `qhy-card` 输出结果，建议至少执行：

```bash
bash scripts/quality-check.sh <file.html>
```

如需本地预览：

```bash
bash scripts/preview.sh <file.html>
```

## 文档同步

以下文件建议一起维护：

- `README.md`
- `docs/architecture.md`
- `skills/README.md`
- 对应 skill 的 `SKILL.md`

如果仓库方向变了，但这些文件没有跟上，后续扩展会很快失焦。
