#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from xml.sax.saxutils import escape


STYLES = {
    1: {"bg": "#f8fafc", "panel": "#ffffff", "stroke": "#dbe3ef", "title": "#111827", "subtitle": "#6b7280"},
    2: {"bg": "#0f172a", "panel": "#111827", "stroke": "#334155", "title": "#f8fafc", "subtitle": "#94a3b8"},
    3: {"bg": "#0b1f3a", "panel": "#10294d", "stroke": "#4cc9f0", "title": "#e0f2fe", "subtitle": "#93c5fd"},
    4: {"bg": "#ffffff", "panel": "#ffffff", "stroke": "#d4d4d8", "title": "#18181b", "subtitle": "#71717a"},
    5: {"bg": "#0b1120", "panel": "#172033", "stroke": "#7dd3fc", "title": "#f8fafc", "subtitle": "#cbd5e1"},
    6: {"bg": "#f8f6f3", "panel": "#fffdf8", "stroke": "#d6cec3", "title": "#2f2823", "subtitle": "#7c6f64"},
    7: {"bg": "#ffffff", "panel": "#ffffff", "stroke": "#d1d5db", "title": "#111827", "subtitle": "#6b7280"},
}

FLOW_COLORS = {
    "data": "#2563eb",
    "control": "#ea580c",
    "write": "#059669",
    "read": "#16a34a",
    "async": "#6b7280",
    "loop": "#7c3aed",
}

NODE_FILLS = {
    "default": "#ffffff",
    "double_rect": "#eff6ff",
    "cylinder": "#f0fdf4",
    "document": "#fff7ed",
    "terminal": "#ede9fe",
    "circle_cluster": "#ecfeff",
}


def load_payload(arg: str) -> dict:
    path = Path(arg)
    if path.exists():
      return json.loads(path.read_text(encoding="utf-8"))
    return json.loads(arg)


def marker_defs() -> str:
    defs = []
    for flow, color in FLOW_COLORS.items():
        defs.append(
            f'<marker id="arrow-{flow}" viewBox="0 0 10 10" refX="9" refY="5" '
            f'markerWidth="8" markerHeight="8" orient="auto-start-reverse">'
            f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{color}" /></marker>'
        )
    return "".join(defs)


def render_container(c: dict, style: dict) -> str:
    x = c.get("x", 40)
    y = c.get("y", 90)
    width = c.get("width", 240)
    height = c.get("height", 160)
    label = escape(c.get("label", "Container"))
    side = escape(c.get("side_label", ""))
    prefix = escape(c.get("header_prefix", ""))
    header = escape(c.get("header_text", ""))
    header_text = f"{prefix} {header}".strip() or label
    parts = [
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="20" fill="{style["panel"]}" stroke="{style["stroke"]}" />',
        f'<text x="{x + 20}" y="{y + 30}" class="section">{header_text}</text>',
    ]
    if side:
        parts.append(f'<text x="{x - 10}" y="{y + 26}" class="meta-label" text-anchor="end">{side}</text>')
    return "".join(parts)


def render_node(n: dict, style: dict) -> str:
    x = n.get("x", 80)
    y = n.get("y", 140)
    width = n.get("width", 180)
    height = n.get("height", 64)
    label = escape(n.get("label", n.get("id", "Node")))
    sublabel = escape(n.get("sublabel", ""))
    kind = n.get("kind", "default")
    fill = n.get("fill", NODE_FILLS.get(kind, NODE_FILLS["default"]))
    stroke = n.get("stroke", style["stroke"])
    if kind == "cylinder":
        top = y + 12
        return (
            f'<ellipse cx="{x + width/2}" cy="{top}" rx="{width/2}" ry="12" fill="{fill}" stroke="{stroke}" />'
            f'<rect x="{x}" y="{top}" width="{width}" height="{height - 24}" fill="{fill}" stroke="{stroke}" />'
            f'<ellipse cx="{x + width/2}" cy="{y + height - 12}" rx="{width/2}" ry="12" fill="{fill}" stroke="{stroke}" />'
            f'<text x="{x + width/2}" y="{y + height/2}" class="node-label" text-anchor="middle">{label}</text>'
        )
    border = 2 if kind == "double_rect" else 1
    inner = ""
    if kind == "double_rect":
        inner = f'<rect x="{x + 6}" y="{y + 6}" width="{width - 12}" height="{height - 12}" rx="14" fill="none" stroke="{stroke}" />'
    return (
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="16" fill="{fill}" stroke="{stroke}" stroke-width="{border}" />'
        f'{inner}'
        f'<text x="{x + width/2}" y="{y + height/2 - (4 if sublabel else 0)}" class="node-label" text-anchor="middle">{label}</text>'
        + (f'<text x="{x + width/2}" y="{y + height/2 + 18}" class="meta-label" text-anchor="middle">{sublabel}</text>' if sublabel else "")
    )


def center(node: dict) -> tuple[float, float]:
    x = float(node.get("x", 0))
    y = float(node.get("y", 0))
    width = float(node.get("width", 180))
    height = float(node.get("height", 64))
    return x + width / 2, y + height / 2


def render_arrow(a: dict, nodes_by_id: dict[str, dict]) -> str:
    source = nodes_by_id[a["source"]]
    target = nodes_by_id[a["target"]]
    sx, sy = center(source)
    tx, ty = center(target)
    flow = a.get("flow", "data")
    color = FLOW_COLORS.get(flow, FLOW_COLORS["data"])
    dashed = a.get("dashed", False) or flow in {"write", "async"}
    stroke_dash = ' stroke-dasharray="6 4"' if dashed else ""
    label = escape(a.get("label", ""))
    line = (
        f'<line x1="{sx}" y1="{sy}" x2="{tx}" y2="{ty}" stroke="{color}" stroke-width="2.5"'
        f'{stroke_dash} marker-end="url(#arrow-{flow})" />'
    )
    if not label:
        return line
    mx = (sx + tx) / 2
    my = (sy + ty) / 2 - 8
    return (
        line
        + f'<rect x="{mx - 24}" y="{my - 14}" width="48" height="18" rx="9" fill="#ffffff" stroke="#dbe3ef" />'
        + f'<text x="{mx}" y="{my - 1}" class="legend-label" text-anchor="middle">{label}</text>'
    )


def render_legend(legend: list[dict], x: int, y: int, style: dict) -> str:
    if not legend:
        return ""
    height = 36 + 20 * len(legend)
    parts = [f'<rect x="{x}" y="{y}" width="220" height="{height}" rx="16" fill="{style["panel"]}" stroke="{style["stroke"]}" />']
    parts.append(f'<text x="{x + 18}" y="{y + 24}" class="section">LEGEND</text>')
    yy = y + 42
    for item in legend:
        flow = item.get("flow", "data")
        color = FLOW_COLORS.get(flow, FLOW_COLORS["data"])
        dash = ' stroke-dasharray="6 4"' if flow in {"write", "async"} else ""
        label = escape(item.get("label", flow))
        parts.append(f'<line x1="{x + 18}" y1="{yy}" x2="{x + 54}" y2="{yy}" stroke="{color}" stroke-width="2.5"{dash} />')
        parts.append(f'<text x="{x + 64}" y="{yy + 4}" class="legend-label">{label}</text>')
        yy += 20
    return "".join(parts)


def main() -> int:
    if len(sys.argv) != 4:
        print("Usage: generate-from-template.py <type> <output.svg> <json-or-path>", file=sys.stderr)
        return 1

    _diagram_type = sys.argv[1]
    output_path = Path(sys.argv[2])
    payload = load_payload(sys.argv[3])
    style_id = int(payload.get("style", 1))
    style = STYLES.get(style_id, STYLES[1])
    title = escape(payload.get("title", "Untitled Diagram"))
    subtitle = escape(payload.get("subtitle", "Generated by qhy-draw"))
    width = int(payload.get("width", 960))
    height = int(payload.get("height", 600))

    containers = payload.get("containers", [])
    nodes = payload.get("nodes", [])
    arrows = payload.get("arrows", [])
    legend = payload.get("legend", [])
    nodes_by_id = {n["id"]: n for n in nodes if "id" in n}

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img">',
        "<defs>",
        marker_defs(),
        (
            "<style>"
            f'.title {{ font: 700 24px "Segoe UI","PingFang SC","Microsoft YaHei",sans-serif; fill: {style["title"]}; }}'
            f'.subtitle {{ font: 400 13px "Segoe UI","PingFang SC","Microsoft YaHei",sans-serif; fill: {style["subtitle"]}; }}'
            f'.section {{ font: 700 13px "Segoe UI","PingFang SC","Microsoft YaHei",sans-serif; fill: {style["title"]}; }}'
            f'.node-label {{ font: 600 14px "Segoe UI","PingFang SC","Microsoft YaHei",sans-serif; fill: {style["title"]}; }}'
            f'.meta-label {{ font: 400 12px "Segoe UI","PingFang SC","Microsoft YaHei",sans-serif; fill: {style["subtitle"]}; }}'
            f'.legend-label {{ font: 400 12px "Segoe UI","PingFang SC","Microsoft YaHei",sans-serif; fill: {style["title"]}; }}'
            "</style>"
        ),
        "</defs>",
        f'<rect width="{width}" height="{height}" fill="{style["bg"]}" />',
        f'<text x="48" y="48" class="title">{title}</text>',
        f'<text x="48" y="72" class="subtitle">{subtitle}</text>',
    ]

    svg.extend(render_container(c, style) for c in containers)
    svg.extend(render_node(n, style) for n in nodes)
    svg.extend(render_arrow(a, nodes_by_id) for a in arrows if a.get("source") in nodes_by_id and a.get("target") in nodes_by_id)
    svg.append(render_legend(legend, width - 252, height - 110, style))
    svg.append("</svg>")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("".join(svg), encoding="utf-8")
    print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
