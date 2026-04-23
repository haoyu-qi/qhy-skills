# qhy-ppt Scripts

`qhy-ppt` 目前补齐了和 `html-ppt-skill` 同类的两项基础脚本能力：

- `new-deck`：从基础 deck 模板脚手架一个新演示
- `render`：用本地浏览器无头渲染 PNG 预览

## Windows

```powershell
powershell -ExecutionPolicy Bypass -File skills/qhy-ppt/scripts/new-deck.ps1 my-talk
powershell -ExecutionPolicy Bypass -File skills/qhy-ppt/scripts/render.ps1 skills/qhy-ppt/examples/my-talk/index.html all
```

## macOS / Linux

```bash
bash skills/qhy-ppt/scripts/new-deck.sh my-talk
bash skills/qhy-ppt/scripts/render.sh skills/qhy-ppt/examples/my-talk/index.html all
```

## 说明

- `new-deck` 默认从 `assets/deck-starter.html` 复制到 `examples/<name>/index.html`
- `render` 默认输出 1920x1080 PNG
- `render all` 会自动统计 `.slide` 数量并逐页截图
