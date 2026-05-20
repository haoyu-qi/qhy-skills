# Avcon 模板使用说明

`assets/avcon_template.html` 是 qhy-ppt 的企业汇报模板，参考 Avcon 年终总结类 PPT 的视觉格式：白底、Avcon 红、顶部红色分隔线、底部 Proprietary 页脚、右下 AVCOn 标识，以及封面红粉环形装饰。

## 何时使用

- 用户明确要求 `avcon` / `AVCON` / `Avcon 模板`
- 参考图包含 Avcon 标识、红色页眉线、`Avcon Proprietary - Restricted Distribution` 页脚
- 需要更像传统企业 PPT，而不是 qhy-ppt 默认的杂志风 / 电子墨水风

## 拷贝方式

```bash
mkdir -p "项目/XXX/ppt/images"
cp "<SKILL_ROOT>/assets/avcon_template.html" "项目/XXX/ppt/index.html"
```

avcon 模板是完整单文件 HTML，不需要复制 `motion.min.js` 或 `avatar.jpg`。

## 内置版式

### 1. 封面页

使用 `.slide.cover`：

- 大标题 `.cover-title`
- 副标题 `.cover-subtitle`
- 横向灰色进度线 `.cover-rule`
- 汇报人标签 `.presenter`
- 红粉环形装饰 `.ring-right` / `.ring-left`

适合年终总结、年度规划、部门汇报封面。

### 2. 正文页

使用普通 `.slide`：

- 顶部标题 `.content-title`
- 顶部红线 `.top-rule`
- 内容区 `.content-body`
- 底部页脚 `.footer`

页脚固定为三栏：页码、`Avcon Proprietary - Restricted Distribution`、右下 Avcon 原始 PNG logo。

### 3. 结束页

使用 `.slide.thanks`：

- 居中大字 `.thanks-title`
- 下方分隔线副标题 `.thanks-sub`
- 淡红点阵背景由 CSS 生成，不需要图片

## 生成约束

- 保持白底、红线、灰色大标题，不混入默认杂志模板的 WebGL 和作者头像
- 正文页标题使用深红色，加粗，左上对齐
- 底部页脚每页保留，页码按实际页数更新
- 右下 logo 使用 `.avcon-logo` 原始 PNG 位图；不要用文字或 SVG 近似替代
- 16:9 横屏优先，截图和图表放入 `.content-body` 内，避免覆盖顶部红线和底部页脚
