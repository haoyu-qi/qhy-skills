# 单张生图提示词模板

每张图单独调用内置 `image_gen`。把花括号内容替换为当前文章信息。

```text
Use case: illustration-story
Asset type: 16:9 Chinese article illustration, image {序号} of a coherent series
Primary request: {核心观点}
Scene/backdrop: {一个明亮、干净、可叙事的场景}
Subject: {普通人物是谁，正在执行什么关键动作，动作如何表达观点}
Style/medium: full-color hand-drawn editorial animation frame, colored-pencil outlines, watercolor and gouache fills, lively handmade brush texture, mature and friendly, clear but not instructional
Composition/framing: wide 16:9 cinematic scene, one strong visual metaphor, organic layout, clear hierarchy, 25%-40% breathing room
Color palette: coral orange, cobalt blue, mustard yellow, teal, warm cream; keep the same palette across the series
Text (verbatim): “{标注1}”; “{标注2}”; “{标注3}”; “{可选标注4}”; “{可选标注5}”
Constraints: render only the quoted short labels, exactly and legibly; one image explains one relationship; the character must perform the core action; no headline unless requested; no logos; no black blob creature, no 小黑, no mascot
Avoid: monochrome black-and-white minimal line art, PPT infographic, formal flowchart, dense architecture chart, corporate flat vector art, 3D render, photorealism, childish cartoon, watermark
```

## 系列一致性补充

连续生成多张时，在每张提示词中重复：

```text
Keep the same editorial-animation visual language as the series: consistent colored-pencil line weight, watercolor/gouache texture, adult character proportions, palette, background brightness, and handwritten Chinese label style. Do not reuse the exact composition of another image.
```

## 中文修正

若中文错误较少，使用局部编辑：

```text
Edit only the incorrect label “{错误文字}” and replace it with the exact Chinese text “{正确文字}”. Preserve the entire scene, characters, colors, brushwork, composition, aspect ratio, and all other labels. Add nothing else.
```

若错误较多，重生成并把标注减少到 3 个。