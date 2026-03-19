# 信息图 (Infographic Card)

将复杂信息转化为专业级 HTML 信息卡片的 Claude 技能。

## 支持的视觉风格

| 风格 | 适用场景 | 关键特征 |
|------|----------|----------|
| **暗黑科技风** | 产品资料、功能列表、版本日志 | 深色背景、辉光卡片、水印编号 |
| **扁平现代风** | AI 产品宣传、技术指标展示 | 浅色背景、多彩卡片、大背景数字 |
| **杂志质感风** | 社论风格、深度报道 | 大字号正文、噪点纹理、分割线 |
| **复古书卷风** | 书籍解析、文学内容 | 传统配色、装饰纹样、书法字体 |
| **蓝图波普风** | 高密度干货、技术教程 | 实验室感、坐标系、荧光高亮 |
| **纯白演示风** | 季度更新、演示文稿 | 16:9 分页、高对比高亮 |
| **周报模块风** | 工作周报、数据看板 | 彩色分区、模块化布局 |

## 快速上手

**方式一：直接发提示词**

```
请用 infographic-card 技能生成一张信息图。
风格：暗黑科技风
主题：GPT-4o 的核心功能与技术规格
```

**方式二：使用脚手架脚本**

```bash
bash scripts/new-card.sh
```

## 使用示例

```
生成一张信息图展示 XXX
一图看懂 XXX
帮我生成周报 HTML
把《三体》的内容做成信息卡片
```

## 输出格式

- **HTML 单文件**（内联 CSS，零外部依赖）
- **JSON 结构化数据**（可选）

## 技能结构

```
infographic-card/
├── SKILL.md                  # 主文件（风格识别、行为规范）
├── README.md
├── references/
│   ├── dark-tech.md          # 暗黑科技风（含 HTML 骨架）
│   ├── flat-modern.md        # 扁平现代风
│   ├── magazine.md           # 杂志质感风（含噪点 SVG）
│   ├── vintage-book.md       # 复古书卷风（含传统纹样）
│   ├── blueprint-pop.md      # 蓝图波普风（含网格背景）
│   ├── white-presentation.md # 纯白演示风
│   └── weekly-report.md      # 周报模块风
└── scripts/
    ├── README.md             # 脚本使用文档
    ├── preview.sh            # 浏览器快速预览
    ├── quality-check.sh      # HTML 质量检查（9 项）
    └── new-card.sh           # 交互式提示词生成
```

## 辅助脚本

```bash
bash scripts/preview.sh output.html        # 预览
bash scripts/quality-check.sh output.html  # 质量检查
bash scripts/new-card.sh                   # 生成提示词
```

## License

MIT
