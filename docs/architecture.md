# qhy-skills 架构说明

这个仓库现在按“仓库层 + skill 层 + 模板层”组织，目标是让后续新增 skill 时不需要重想一遍结构，并且能稳定承接 `qhy-card`、`qhy-ppt`、`qhy-draw`、`qhy-word` 这类并列能力。

## 1. 仓库层

位于根目录，负责整个仓库被识别、安装和导航：

- `.claude-plugin/`：插件元数据
- `README.md`：仓库总入口
- `scripts/`：跨 skill 复用的公共脚本
- `docs/`：仓库级规范和架构说明

## 2. Skill 层

每个 skill 都位于 `skills/<skill-name>/`，相互独立，互不污染。

推荐结构：

```text
skills/<skill-name>/
├── SKILL.md
├── assets/
├── references/
└── scripts/
```

说明：

- `SKILL.md`：唯一必需文件，定义触发条件、工作流和输出要求
- `assets/`：模板、静态骨架、图标、示例片段
- `references/`：规则、模式、知识参考、风格库
- `scripts/`：仅当前 skill 使用的专属脚本

当前建议把 skill 按“输出形态”而不是“行业场景”拆分：

- `qhy-card`：单页视觉卡片
- `qhy-ppt`：多页演示文稿
- `qhy-draw`：图示与白板结构
- `qhy-word`：正式文档正文

## 3. 模板层

`skills/_template/` 是新增 skill 的标准起点。

当准备新增 skill 时，建议直接复制这套结构，再替换：

- skill 名称
- 触发场景
- 引用资料
- 资产模板
- 专属脚本

## 4. 命名约定

- 仓库内技能统一使用 `qhy-*`
- 目录名、skill 名、README 展示名尽量一致
- 不建议混入风格完全不同的命名前缀

## 5. 公共与私有边界

放到根目录 `scripts/` 的，应当是多个 skill 都可能用到的工具。

只服务单一 skill 的工具，放到对应 skill 的 `scripts/`。

判断标准：

- 如果它只理解某一个 skill 的领域概念，就放 skill 内部
- 如果它只是预览、校验、初始化这类通用工作，就放根目录

## 6. 扩展建议

当前仓库已经具备四类基础表达能力，后续更适合补“跨 skill 编排层”：

1. `qhy-flow`：把多个 skill 串成工作流
2. `qhy-plain`：复杂内容白话化改写
3. `qhy-paper`：论文 / 报告理解与结构化输出

建议路径是：

- 先让单项能力边界清晰
- 再补多 skill 协同
- 最后再加更细分的垂类 skill
