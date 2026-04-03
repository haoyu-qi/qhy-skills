# Scripts

`qhy-skills` 当前提供 4 个辅助脚本，帮助我们更稳定地生成和检查 HTML 卡片。

## `new-card.sh`

交互式脚手架。引导选择模具、风格、主题和额外要求，最后输出一段可直接发送给 Claude 的提示词。

```bash
bash scripts/new-card.sh
```

## `quality-check.sh`

对生成结果做静态检查，重点排查：

- 外部 CSS / JS 依赖
- 外部图片和远程字体
- 缺失 `charset` / `viewport`
- 缺失移动端断点
- `z-content` 这类常见拼写错误
- 空列表标签
- 未替换模板变量，如 `{{TITLE}}`
- 文件体积是否异常

```bash
bash scripts/quality-check.sh output.html
```

## `preview.sh`

在默认浏览器中打开本地 HTML 文件。

```bash
bash scripts/preview.sh output.html
```

## `install.sh`

预留安装脚本。目前主要用于后续可能加入的本地渲染依赖检查，不强制安装。

```bash
bash scripts/install.sh
```
