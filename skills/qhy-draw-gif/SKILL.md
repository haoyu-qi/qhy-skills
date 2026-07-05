---
name: qhy-draw-gif
description: |
  Use this skill when the user wants an animated architecture diagram, animated process diagram, Excalidraw-like technical sketch, black-background hand-drawn GIF, 岚叔动态架构图, or a visual explanation that should be delivered as GIF + PNG + editable Excalidraw.

  触发词：动态图、动态架构图、动画架构图、GIF 架构图、GIF 流程图、岚叔动态架构图、Excalidraw 动图、黑底手绘图、动态技术图解、animated diagram。

  Workflow: identify diagram family -> choose a motion layout -> render .gif + .png + editable source -> verify motion and readability.
---

# qhy-draw-gif: Animated Diagram Generator

`qhy-draw-gif` turns architecture, process, and technical explanation content into a polished animated diagram bundle. Do not force every diagram into the same fixed three-card template; preserve the source diagram's structural grammar whenever the source has one.

- Editable source (`.excalidraw`, `.svg`, `.drawio`, or `.html`)
- Static `.png` preview
- Animated `.gif` with moving flow highlights and pulsing modules

Use `qhy-draw-gif` for motion-first storytelling. Keep using `qhy-draw` when the user needs a draw.io / diagrams.net source file, UML, ER, network topology, or a static diagram export.

This skill is adapted from `cclank/lanshu-animated-architecture-diagram` and preserves the local deterministic Python/Pillow rendering model. The bundled renderer is one option, not the default for every task.

## Workflow

1. Understand the content.
   - Identify the source diagram family before authoring: tree/org chart, layered architecture, process/flow, topology, timeline/roadmap, matrix/list, or narrative explainer.
   - Identify the core actors, hierarchy, stages, data flow, quality gate, and output.
   - For an article or long text, compress the story into three core cards plus lower panels only if there is no stronger visual structure.
   - Keep labels short; rewrite crowded labels instead of shrinking text until unreadable.

2. Choose the motion layout.
   - Read `references/layout-strategy.md` when the source is an existing architecture diagram, org/tree chart, plan list, product map, topology, roadmap, or any non-linear diagram.
   - Use the bundled fixed renderer only for narrative explainers and simple left-to-right process stories.
   - For tree, layered, matrix, topology, or roadmap diagrams, create a custom SVG/HTML/Pillow frame renderer that preserves the original structure, then export GIF + PNG.
   - Default to Chinese labels. Use another language only when the user asks for it or the reference visual clearly calls for it.

3. Author the render source.
   - For fixed narrative layouts: create a spec JSON starting from `assets/default-spec.json`; read `references/spec-format.md` when editing fields, choosing styles, or checking copy length.
   - For custom layouts: create a compact JSON/SVG/HTML source with explicit coordinates, grouping, and animation phases. Prefer deterministic local rendering with Pillow, browser screenshots, or imageio/Pillow frame assembly.

4. Render outputs.

```bash
python skills/qhy-draw-gif/scripts/render_animated_diagram.py \
  --spec skills/qhy-draw-gif/assets/default-spec.json \
  --outdir outputs/qhy-draw-gif \
  --basename sample \
  --verify \
  --check
```

5. Validate before delivery.
   - Confirm `--check` returns `"ok": true`.
   - Confirm `--verify` includes nonzero changed pixels between sampled GIF frames.
   - Visually inspect the PNG/GIF for overlap, cramped text, weak hierarchy, or unclear motion.
   - Compare the output's structure to the source: a tree should still read as a tree, a layered architecture should still read as layers, and a roadmap should still read as a roadmap.

6. Deliver the files.
   - Show or link the GIF preview when supported.
   - Mention the `.png` preview and editable source (`.excalidraw`, `.drawio`, `.svg`, or `.html`, depending on the chosen renderer).

## Styles

Use `style` in the spec or pass `--style <style-id>` from the CLI. CLI `--style` overrides the spec.

Available styles:

- `lanshu-classic` - default black hand-drawn canvas with green highlights and neon motion.
- `terminal-green` - terminal-like black and green palette for agents, CLI, and automation workflows.
- `blueprint-cyan` - deep blueprint canvas with cyan strokes for systems and topology.
- `warm-amber` - warm black and amber visual language for business process stories.
- `paper-ink` - light paper and ink sketch for teaching, whiteboards, and simple flows.

List styles:

```bash
python skills/qhy-draw-gif/scripts/render_animated_diagram.py --list-styles
```

## Spec Authoring Hints

Use this section only when the chosen layout is the bundled fixed narrative renderer. Map content to the fixed layout:

- `inputs`: source systems, triggers, documents, tools, or user actions
- `core.cards`: the three main stages of the process
- `decision`: the quality gate, readiness check, or branching point
- `left_panel`: memory, context, source material, or upstream inputs
- `center_panel`: internal layers, safeguards, stores, or pipeline internals
- `right_panel`: packaged outputs, generated reports, reusable assets, or final deliverables

If the subject has more than three stages, group adjacent steps into three core cards and move details into the lower panels. If that grouping would erase the source structure, stop and use a custom layout instead.

## Output Contract

Each render should produce:

```text
<basename>.png
<basename>.gif
<basename>.<editable-source>
```

For the bundled renderer, `<editable-source>` is `.excalidraw`. For custom layouts, use the most appropriate editable source: `.svg` for hand-authored vector diagrams, `.drawio` for diagrams.net editing, `.html` for browser/CSS animations, or `.excalidraw` for sketch-style diagrams.

Default media settings:

```text
1210 x 1138
20 fps
41 frames
2.05 seconds
```

## Verification Commands

Render and validate:

```bash
python skills/qhy-draw-gif/scripts/render_animated_diagram.py \
  --spec skills/qhy-draw-gif/assets/default-spec.json \
  --outdir /tmp/qhy-draw-gif-output \
  --basename diagram \
  --verify \
  --check
```

Optional media inspection:

```bash
ffprobe -v error -select_streams v:0 -count_frames \
  -show_entries stream=width,height,r_frame_rate,avg_frame_rate,nb_read_frames \
  -show_entries format=duration \
  -of default=noprint_wrappers=1 /tmp/qhy-draw-gif-output/diagram.gif
```

The `--check` report validates dimensions, frame count, frame duration, sampled motion, Excalidraw unique IDs, text font family, empty `files`, and PNG dimensions.
