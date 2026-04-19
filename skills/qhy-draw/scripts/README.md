# qhy-draw Scripts

这些脚本参考了 `fireworks-tech-graph` 的工作流，用于让 `qhy-draw` 在本地也具备更接近的 SVG 生成、验证和回归测试能力。

## 脚本列表

### 1. `validate-svg.sh`

检查 SVG 基础合法性：

- 文件是否存在
- XML 是否可解析
- 是否包含 `<svg>` 根节点
- 是否存在闭合标签
- 是否存在 marker 引用缺失
- 如果本机安装了 `rsvg-convert`，则额外做一次渲染验证

### 2. `generate-from-template.py`

根据 JSON 数据生成基础 SVG，支持：

- `style`
- `title`
- `subtitle`
- `containers`
- `nodes`
- `arrows`
- `legend`

### 3. `generate-diagram.sh`

对已有 SVG 做：

- 验证
- 可选 PNG 导出

### 4. `test-all-styles.sh`

批量读取 JSON 数据，调用 `generate-from-template.py` 生成 SVG，并对输出做验证。

## 推荐流程

1. 先让模型确定图型、风格和结构
2. 生成 JSON 或直接生成 SVG
3. 用 `generate-from-template.py` 产出基础 SVG
4. 用 `validate-svg.sh` 校验
5. 如本机有 `rsvg-convert`，再用 `generate-diagram.sh` 导出 PNG
