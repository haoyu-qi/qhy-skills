# Animated Diagram Layout Strategy

Choose the motion layout before authoring. The goal is to preserve the source diagram's structure while adding motion, not to make every diagram look like the same three-card explainer.

## Decision Rule

Use the bundled fixed renderer only when the content is a narrative/process explainer with:

- one main input row,
- three major stages,
- a decision or readiness point,
- lower supporting panels.

For everything else, use a custom layout and renderer.

## Layout Families

### Tree / Org / Plan List

Use for product line trees, plan lists, org charts, capability breakdowns, and mindmap-like source images.

- Preserve the root, branches, and leaf hierarchy.
- Animate by revealing branches from root to leaves, pulsing priority leaves, and sweeping along connector lines.
- Avoid converting wide trees into a generic process flow unless the user explicitly asks for a summary.
- Good editable sources: `.svg`, `.drawio`.

### Layered Architecture

Use for diagrams with clients, service layers, platform services, infrastructure, or cross-cutting concerns.

- Preserve horizontal or vertical layers.
- Animate top-down or left-right calls, then pulse the layer or service being highlighted.
- Keep layer labels fixed and readable.
- Good editable sources: `.svg`, `.drawio`, `.excalidraw`.

### Topology / Network

Use for nodes connected by routes, gateways, protocols, or deployment topology.

- Preserve node positions and connection semantics.
- Animate packets/dots along edges and pulse active nodes.
- Avoid rearranging into sequential cards.
- Good editable sources: `.svg`, `.drawio`.

### Roadmap / Timeline

Use for plans across weeks, milestones, releases, or phases.

- Preserve time direction.
- Animate a progress sweep, milestone pulses, and current/next phase emphasis.
- Good editable sources: `.svg`, `.html`.

### Matrix / Dashboard / List

Use for status boards, comparison matrices, module inventories, or grouped lists.

- Preserve rows/columns or card groups.
- Animate scan lines, status chips, priority highlights, or group-by-group reveals.
- Good editable sources: `.svg`, `.html`.

### Narrative Explainer

Use the bundled fixed renderer for compact explanations where the source does not already have a strong layout.

- Inputs -> three core cards -> decision/output -> lower panels.
- Keep text short and use `references/spec-format.md`.

## Custom Rendering Guidance

- Create a source artifact first (`.svg`, `.html`, `.drawio`, or `.excalidraw`) with stable coordinates.
- Generate a PNG preview from frame 0 or a static complete frame.
- Generate the GIF from deterministic frames using browser screenshots, Pillow, or imageio/Pillow.
- Verify at least 3 sampled frame diffs have nonzero changed pixels.
- Visually inspect that labels do not overlap and no highlighted text falls outside its container.

## Anti-Repetition Checklist

Before delivering, ask:

- Does the diagram still look like the input's diagram family?
- Are the primary groupings from the source preserved?
- Did I choose motion that explains the source instead of replacing the source?
- Would two unrelated user diagrams produced by this skill look meaningfully different?
