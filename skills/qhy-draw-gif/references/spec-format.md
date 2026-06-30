# qhy-draw-gif Spec Format

Use this reference when creating or editing a spec for `scripts/render_animated_diagram.py`.

## Layout Model

The renderer uses a fixed art-directed architecture/process layout:

1. Top title: `title.prefix` plus highlighted `title.highlight`
2. Top input box: four compact input sources
3. Middle core: three major process cards, a decision diamond, and an output card
4. Bottom left panel: source/context cards
5. Bottom center panel: internal storage or processing layers
6. Bottom right panel: final package/output cards
7. Top-right brand slot: dotted mark plus `signature`

Keep copy short. The renderer wraps CJK and English text and reduces font size as a safety net, but concise copy produces the strongest result.

## Fields

- `canvas.width`, `canvas.height`: output dimensions; default is `1210 x 1138`.
- `canvas.fps`, `canvas.frames`: GIF timing; default is `20 fps` and `41 frames`.
- `style`: one of `lanshu-classic`, `terminal-green`, `blueprint-cyan`, `warm-amber`, `paper-ink`.
- `signature`: short handle shown in the top-right brand slot.
- `title.prefix`, `title.highlight`, `title.subtitle`: main title treatment.
- `input_title`: label above the input row.
- `inputs`: up to four input items, each with `label`, `icon`, and optional `color`.
- `core.title`, `core.subtitle`, `core.cards`: main process group and three primary stages.
- `decision.title`, `decision.body`: central quality gate or branch.
- `output.label`, `output.icon`: result card after the decision.
- `loop_label`, `retry_label`, `yes_label`, `read_label`, `context_label`: explanatory labels for feedback/retry and lower-panel flows.
- `left_panel`, `center_panel`, `right_panel`: lower supporting panels.

## Recommended Copy Length

- `title.prefix`: 2 to 4 words
- `title.highlight`: 1 to 3 words
- Input labels: 1 word
- Core card title: 1 to 2 words
- Core card body: 2 lines, each under 22 characters
- Panel card title: 1 to 3 words
- Panel card body: 1 to 2 short lines
- Signature: short handle, such as `@QHY`

Manual line breaks in the spec are preserved. English text wraps on spaces, while CJK text can wrap between characters when needed.

## Supported Icons

- `folder`
- `file`
- `scan`
- `shield`
- `db`
- `hash`
- `package`

Use built-in icons unless the user explicitly provides audited local assets. Avoid remote icon libraries.

## Styles

- `lanshu-classic`: black hand-drawn canvas, green title highlight, neon motion.
- `terminal-green`: black/green terminal feel for agents and automation.
- `blueprint-cyan`: deep blue technical blueprint feel.
- `warm-amber`: black/amber business-process feel.
- `paper-ink`: light paper sketch feel.

The CLI `--style` option overrides the `style` field in the spec. Use this to render the same diagram in multiple visual directions.

## Quality Bar

Every finished diagram should include:

- `.png` static preview
- `.gif` animated version
- `.excalidraw` editable source

Verify:

- GIF dimensions match the canvas.
- GIF frame count and FPS match the spec.
- Frame-diff shows real motion.
- Excalidraw JSON has unique IDs.
- All text elements use `fontFamily: 5`.
- `files` is empty unless embedded assets were explicitly requested.
- Text does not overlap or feel cramped in the PNG preview.

## Common Commands

Render default:

```bash
python skills/qhy-draw-gif/scripts/render_animated_diagram.py \
  --spec skills/qhy-draw-gif/assets/default-spec.json \
  --outdir /tmp/qhy-draw-gif-output \
  --basename diagram \
  --verify \
  --check
```

Render another style:

```bash
python skills/qhy-draw-gif/scripts/render_animated_diagram.py \
  --spec skills/qhy-draw-gif/assets/default-spec.json \
  --outdir /tmp/qhy-draw-gif-output \
  --basename diagram-blueprint \
  --style blueprint-cyan \
  --verify \
  --check
```
