# 实现衔接与结构检查

本技能负责图片分层与还原策略。PPTX API 和导出门禁使用当前宿主的演示文稿规范，不复制易过期的 API 手册。

## Codex 运行时

1. 从当前技能目录找到 `presentations:Presentations`，读取其 implementation、API quick start 和 finalization 指引。版本路径可能变化。
2. 调用 `load_workspace_dependencies` 获取 Node、Python 及依赖位置。按返回值运行 JavaScript ES modules，在工作目录连接相应 node_modules，不硬编码某用户的缓存路径。
3. 按宿主要求记录本次 artifact 操作并设置字体策略。参考图片不是 PPTX 字体证据，视觉匹配的字体属于设计选择。
4. `@oai/artifact-tool` 的位置和数字字号以 CSS 像素为单位；原比例 W×H 画布的 EMU 尺寸为 `W*9525,H*9525`。换画布时统一缩放形状、文本、线宽和图片。
5. 文字明确设置 typeface、fontSize、bold、color、alignment、verticalAlignment、insets、wrap 和 autoFit。不要用自动缩字掩盖布局问题。
6. 源码与逐字稿保存在当前任务工作目录。等待所有资产处理完成，再按固定顺序添加图层，避免图片晚于导出或意外覆盖文本。
7. 草稿和正式文件分开；正式修订使用新的文件名与回执路径，避免 finalizer 防覆盖错误。只整理本次临时版本，不删除其他业务的交付文件。
8. 按宿主规范执行结构校验和最终文件重新导入/渲染，逐页查看。联系图只辅助检查整本的顺序与风格。

## 辅助结构审查

```bash
python scripts/audit_pptx.py /path/deck.pptx --expected-slides 3 --require-native-text --report /path/work/editability-audit.json
```

明确不允许任何整页图片时加 `--forbid-full-slide-images`。默认图片宽高均达到画布 85% 时提示风险。`--source /path/source.png` 可检查完全同字节原图是否仍嵌入，允许多次指定；重新编码的同图不能靠哈希识别。

脚本列出每页原生文字、形状、图片、表格和图表计数及文字清单，提示整页图片、图片背景和组变换中的未知项。它不测字形，不判断视觉相似度，无法发现所有重影；有少量原生文字不等于所有信息都可编辑，不能把计数换算成“可编辑率”。

未经实际打开，不声称已在 Microsoft PowerPoint 验证。渲染工具与目标客户端可能在字体、渐变、圆角表现上有差异，仅在出现具体风险时追加针对性客户端检查。
