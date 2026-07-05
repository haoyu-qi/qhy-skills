#!/usr/bin/env python3
"""QHY animated diagram renderer adapted from cclank/lanshu-animated-architecture-diagram (MIT)."""

import argparse
import json
import math
import random
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont


DEFAULT_W = 1210
DEFAULT_H = 1138
DEFAULT_FRAMES = 41
DEFAULT_FPS = 20
SCALE = 2
UPDATED = 1782475200000
DEFAULT_STYLE = "lanshu-classic"

STYLE_THEMES = {
    "lanshu-classic": {
        "description": "Black hand-drawn canvas with green highlights and neon motion.",
        "bg": "#000000",
        "white": "#f4f0ee",
        "muted": "#cfc7c5",
        "frame": "#5c6265",
        "core_fill": "#04171e",
        "core_stroke": "#1d8be8",
        "green": "#22c86f",
        "green_fill": "#02160a",
        "purple": "#bd54d3",
        "purple_fill": "#120814",
        "cyan": "#7ee3d6",
        "blue_fill": "#081626",
        "highlight": "#124238",
        "amber": "#f4b64e",
        "pink": "#ff7ab6",
        "archive_fill": "#080711",
        "source_fill": "#02160a",
        "pack_fill": "#04180d",
        "decision_fill": "#052515",
        "mini_fill": "#04200f",
        "center_card_fill": "#17091d",
        "pack_row_fill": "#04200f",
    },
    "terminal-green": {
        "description": "Terminal-like black and green palette for agent and CLI workflows.",
        "bg": "#020403",
        "white": "#e8ffe8",
        "muted": "#8fbd98",
        "frame": "#2c6a43",
        "core_fill": "#031109",
        "core_stroke": "#39ff88",
        "green": "#39ff88",
        "green_fill": "#031b0c",
        "purple": "#58d68d",
        "purple_fill": "#06160c",
        "cyan": "#7fffd4",
        "blue_fill": "#06120a",
        "highlight": "#103b22",
        "amber": "#c6ff6b",
        "pink": "#9dffb0",
        "archive_fill": "#06110a",
        "source_fill": "#02180a",
        "pack_fill": "#031d0b",
        "decision_fill": "#052414",
        "mini_fill": "#042411",
        "center_card_fill": "#061c10",
        "pack_row_fill": "#042411",
    },
    "blueprint-cyan": {
        "description": "Deep blueprint canvas with cyan strokes for systems and topology.",
        "bg": "#06111f",
        "white": "#ecfbff",
        "muted": "#a8c9d8",
        "frame": "#3d6f8d",
        "core_fill": "#071b2e",
        "core_stroke": "#44c7ff",
        "green": "#65e4ff",
        "green_fill": "#052334",
        "purple": "#8aa7ff",
        "purple_fill": "#0b1430",
        "cyan": "#7eeaff",
        "blue_fill": "#08243d",
        "highlight": "#123f5a",
        "amber": "#ffd166",
        "pink": "#ff9fd6",
        "archive_fill": "#071427",
        "source_fill": "#061f2d",
        "pack_fill": "#062637",
        "decision_fill": "#073247",
        "mini_fill": "#082b3e",
        "center_card_fill": "#0b1d3c",
        "pack_row_fill": "#082b3e",
    },
    "warm-amber": {
        "description": "Warm black and amber visual language for business process stories.",
        "bg": "#0b0703",
        "white": "#fff4df",
        "muted": "#d8b98a",
        "frame": "#6d5331",
        "core_fill": "#1a1007",
        "core_stroke": "#f0a43a",
        "green": "#ffc857",
        "green_fill": "#271704",
        "purple": "#ff7a59",
        "purple_fill": "#24100a",
        "cyan": "#ffd58a",
        "blue_fill": "#201407",
        "highlight": "#5a3512",
        "amber": "#ffb000",
        "pink": "#ff8b7b",
        "archive_fill": "#160d06",
        "source_fill": "#1f1205",
        "pack_fill": "#241505",
        "decision_fill": "#2d1b06",
        "mini_fill": "#2b1a08",
        "center_card_fill": "#261108",
        "pack_row_fill": "#2b1a08",
    },
    "paper-ink": {
        "description": "Light paper and ink sketch for teaching, whiteboards, and simple flows.",
        "bg": "#f8f3e7",
        "white": "#202124",
        "muted": "#6b6256",
        "frame": "#9a8f80",
        "core_fill": "#fffaf0",
        "core_stroke": "#246b84",
        "green": "#2f7d55",
        "green_fill": "#e7f2e7",
        "purple": "#7b4f9f",
        "purple_fill": "#efe7f6",
        "cyan": "#2f7f95",
        "blue_fill": "#e8f1f5",
        "highlight": "#d9ead7",
        "amber": "#b36b00",
        "pink": "#b85b73",
        "archive_fill": "#f4edf8",
        "source_fill": "#edf7ef",
        "pack_fill": "#edf5ee",
        "decision_fill": "#e4f0df",
        "mini_fill": "#f5fff5",
        "center_card_fill": "#fbf5ff",
        "pack_row_fill": "#f5fff5",
    },
}

THEME = dict(STYLE_THEMES[DEFAULT_STYLE])


def available_styles():
    return {name: data["description"] for name, data in STYLE_THEMES.items()}


def apply_style(style_id):
    if style_id not in STYLE_THEMES:
        choices = ", ".join(sorted(STYLE_THEMES))
        raise ValueError(f"Unknown style '{style_id}'. Available styles: {choices}")
    THEME.clear()
    THEME.update(STYLE_THEMES[style_id])
    return style_id


def prepare_spec(spec, style_id=None):
    prepared = json.loads(json.dumps(spec))
    selected = style_id or prepared.get("style") or DEFAULT_STYLE
    apply_style(selected)
    prepared["style"] = selected
    return prepared


def hex_rgba(value, alpha=255):
    value = value.lstrip("#")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4)) + (alpha,)


def c(v):
    return int(round(v * SCALE))


def scaled_box(x, y, w, h):
    return (c(x), c(y), c(x + w), c(y + h))


def font_candidates(hand=False, cjk=False, bold=False):
    if hand:
        return [
            "/System/Library/Fonts/Supplemental/Chalkduster.ttf",
            "/System/Library/Fonts/MarkerFelt.ttc",
            "/System/Library/Fonts/Noteworthy.ttc",
            "/System/Library/Fonts/Supplemental/Bradley Hand Bold.ttf",
        ]
    if cjk:
        return [
            "C:/Windows/Fonts/msyhbd.ttc" if bold else "C:/Windows/Fonts/msyh.ttc",
            "C:/Windows/Fonts/simhei.ttf",
            "C:/Windows/Fonts/simsun.ttc",
            "/System/Library/Fonts/STHeiti Medium.ttc" if bold else "/System/Library/Fonts/STHeiti Light.ttc",
            "/System/Library/Fonts/Hiragino Sans GB.ttc",
            "/Library/Fonts/Arial Unicode.ttf",
            "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
        ]
    return [
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/msyhbd.ttc" if bold else "C:/Windows/Fonts/msyh.ttc",
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    ]


def load_font(size, hand=False, cjk=False, bold=False):
    for path in font_candidates(hand=hand, cjk=cjk, bold=bold):
        try:
            return ImageFont.truetype(path, c(size))
        except OSError:
            continue
    return ImageFont.load_default()


def has_cjk(text):
    return any("\u3400" <= ch <= "\u9fff" for ch in text)


def text_size(draw, text, font, spacing=3):
    if not text:
        return 0, 0
    box = draw.multiline_textbbox((0, 0), text, font=font, spacing=c(spacing))
    return box[2] - box[0], box[3] - box[1]


def wrap_token(draw, token, font, max_width):
    if not token:
        return [token]
    parts = []
    current = ""
    for char in token:
        candidate = current + char
        if current and text_size(draw, candidate, font)[0] > max_width:
            parts.append(current)
            current = char
        else:
            current = candidate
    if current:
        parts.append(current)
    return parts


def wrap_line(draw, line, font, max_width):
    if not line:
        return [line]
    tokens = list(line) if has_cjk(line) else line.split(" ")
    separator = "" if has_cjk(line) else " "
    lines = []
    current = ""
    for token in tokens:
        candidate = token if not current else current + separator + token
        if text_size(draw, candidate, font)[0] <= max_width:
            current = candidate
            continue
        if current:
            lines.append(current)
        if text_size(draw, token, font)[0] <= max_width:
            current = token
        else:
            split_parts = wrap_token(draw, token, font, max_width)
            lines.extend(split_parts[:-1])
            current = split_parts[-1] if split_parts else ""
    if current:
        lines.append(current)
    return lines


def wrap_text(draw, text, font, max_width):
    lines = []
    for raw_line in str(text).splitlines() or [""]:
        lines.extend(wrap_line(draw, raw_line, font, max_width))
    return "\n".join(lines)


EMERGENCY_MIN_TEXT_SIZE = 6


def text_variants(draw, text, font, max_width, wrap):
    raw = str(text)
    if not wrap:
        return [raw]
    wrapped = wrap_text(draw, raw, font, max_width)
    if wrapped == raw:
        return [wrapped]
    return [wrapped, raw]


def fit_text(draw, text, w, h, size, min_size=10, hand=False, bold=False, spacing=3, wrap=True):
    raw_text = str(text)
    has_cjk_text = has_cjk(raw_text)
    max_width = c(w)
    max_height = c(h)
    start_size = int(size)
    emergency_min = min(start_size, int(min_size), EMERGENCY_MIN_TEXT_SIZE)
    for candidate_size in range(start_size, emergency_min - 1, -1):
        candidate_font = load_font(candidate_size, hand=hand and not has_cjk_text, cjk=has_cjk_text, bold=bold)
        for candidate_text in text_variants(draw, raw_text, candidate_font, max_width, wrap):
            tw, th = text_size(draw, candidate_text, candidate_font, spacing=spacing)
            if tw <= max_width and th <= max_height:
                return candidate_text, candidate_size, candidate_font

    fallback_font = load_font(emergency_min, hand=hand and not has_cjk_text, cjk=has_cjk_text, bold=bold)
    fallback_text = wrap_text(draw, raw_text, fallback_font, max_width) if wrap else raw_text
    return fallback_text, emergency_min, fallback_font


class Excal:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.elements = []
        self.count = 0
        self.rng = random.Random(2069769416930414980)

    def base(self, prefix, kind, x, y, w, h, stroke, fill="transparent", stroke_width=2, stroke_style="solid", roundness=None):
        self.count += 1
        element = {
            "id": f"{prefix}-{self.count:04d}",
            "type": kind,
            "x": round(x, 2),
            "y": round(y, 2),
            "width": round(w, 2),
            "height": round(h, 2),
            "angle": 0,
            "strokeColor": stroke,
            "backgroundColor": fill or "transparent",
            "fillStyle": "solid",
            "strokeWidth": stroke_width,
            "strokeStyle": stroke_style,
            "roughness": 1,
            "opacity": 100,
            "groupIds": [],
            "frameId": None,
            "index": f"a{self.count:04d}",
            "roundness": roundness,
            "seed": self.rng.randint(1, 2147483646),
            "version": 1,
            "versionNonce": self.rng.randint(1, 2147483646),
            "isDeleted": False,
            "boundElements": None,
            "updated": UPDATED,
            "link": None,
            "locked": False,
        }
        self.elements.append(element)
        return element

    def rect(self, x, y, w, h, stroke, fill="transparent", width=2, style="solid"):
        return self.base("rect", "rectangle", x, y, w, h, stroke, fill, width, style, {"type": 3})

    def ellipse(self, x, y, w, h, stroke, fill="transparent", width=2, style="solid"):
        return self.base("ellipse", "ellipse", x, y, w, h, stroke, fill, width, style, None)

    def diamond(self, x, y, w, h, stroke, fill="transparent", width=2):
        return self.base("diamond", "diamond", x, y, w, h, stroke, fill, width, "solid", {"type": 2})

    def text(self, text, x, y, w, h, size, color, align="left"):
        element = self.base("text", "text", x, y, w, h, color, "transparent", 1, "solid", None)
        element.update(
            {
                "text": text,
                "fontSize": int(round(size)),
                "fontFamily": 5,
                "textAlign": align,
                "verticalAlign": "top",
                "baseline": int(round(size * 1.25)),
                "containerId": None,
                "originalText": text,
                "lineHeight": 1.25,
            }
        )
        return element

    def line(self, points, stroke, width=2, style="solid", arrow=False):
        kind = "arrow" if arrow else "line"
        min_x = min(x for x, _ in points)
        min_y = min(y for _, y in points)
        max_x = max(x for x, _ in points)
        max_y = max(y for _, y in points)
        element = self.base(
            kind,
            kind,
            min_x,
            min_y,
            max_x - min_x,
            max_y - min_y,
            stroke,
            "transparent",
            width,
            style,
            {"type": 2},
        )
        element["points"] = [[round(x - min_x, 2), round(y - min_y, 2)] for x, y in points]
        element["startBinding"] = None
        element["endBinding"] = None
        return element

    def write(self, path):
        data = {
            "type": "excalidraw",
            "version": 2,
            "source": "https://excalidraw.com",
            "elements": self.elements,
            "appState": {
                "viewBackgroundColor": THEME["bg"],
                "gridSize": 20,
                "currentItemFontFamily": 5,
            },
            "files": {},
        }
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def draw_text(ex, draw, text, x, y, w, h, size, color=None, align="center", hand=False, bold=False, spacing=3, fit=False, min_size=10, wrap=True):
    color = color or THEME["white"]
    if fit:
        text, size, font = fit_text(draw, text, w, h, size, min_size=min_size, hand=hand, bold=bold, spacing=spacing, wrap=wrap)
    else:
        font = load_font(size, hand=hand and not has_cjk(text), cjk=has_cjk(text), bold=bold)
    ex.text(text, x, y, w, h, size, color, align=align)
    tw, th = text_size(draw, text, font, spacing=spacing)
    tx = c(x)
    if align == "center":
        tx = c(x) + (c(w) - tw) / 2
    elif align == "right":
        tx = c(x + w) - tw
    ty = c(y) + (c(h) - th) / 2
    draw.multiline_text((tx, ty), text, font=font, fill=hex_rgba(color), spacing=c(spacing), align=align)


def draw_rect(ex, draw, x, y, w, h, stroke, fill=None, width=2, radius=10, style="solid"):
    ex.rect(x, y, w, h, stroke, fill or "transparent", width, style)
    draw.rounded_rectangle(scaled_box(x, y, w, h), radius=c(radius), outline=hex_rgba(stroke), fill=hex_rgba(fill) if fill else None, width=max(1, c(width)))


def draw_ellipse(ex, draw, x, y, w, h, stroke, fill=None, width=2):
    ex.ellipse(x, y, w, h, stroke, fill or "transparent", width)
    draw.ellipse(scaled_box(x, y, w, h), outline=hex_rgba(stroke), fill=hex_rgba(fill) if fill else None, width=max(1, c(width)))


def draw_line(ex, draw, points, stroke, width=2, style="solid", arrow=False):
    ex.line(points, stroke, width, style, arrow)
    scaled = [(c(x), c(y)) for x, y in points]
    if style == "solid":
        draw.line(scaled, fill=hex_rgba(stroke), width=max(1, c(width)), joint="curve")
    else:
        total = path_len(points)
        dist = 0
        dash = 8 if style == "dashed" else 2
        gap = 8 if style == "dashed" else 7
        while dist < total:
            start = point_at_distance(points, dist)
            end = point_at_distance(points, min(total, dist + dash))
            draw.line([(c(start[0]), c(start[1])), (c(end[0]), c(end[1]))], fill=hex_rgba(stroke), width=max(1, c(width)))
            dist += dash + gap
    if arrow and len(points) >= 2:
        arrow_head(draw, points[-2], points[-1], stroke, width)


def draw_diamond(ex, draw, x, y, w, h, stroke, fill=None, width=2):
    ex.diamond(x, y, w, h, stroke, fill or "transparent", width)
    pts = [(x + w / 2, y), (x + w, y + h / 2), (x + w / 2, y + h), (x, y + h / 2)]
    scaled = [(c(px), c(py)) for px, py in pts]
    draw.polygon(scaled, outline=hex_rgba(stroke), fill=hex_rgba(fill) if fill else None)
    draw.line(scaled + [scaled[0]], fill=hex_rgba(stroke), width=max(1, c(width)))


def path_len(points):
    return sum(math.dist(a, b) for a, b in zip(points, points[1:]))


def point_at_distance(points, distance):
    left = distance
    for a, b in zip(points, points[1:]):
        seg = math.dist(a, b)
        if seg == 0:
            continue
        if left <= seg:
            t = left / seg
            return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
        left -= seg
    return points[-1]


def point_at_fraction(points, t):
    total = path_len(points)
    return point_at_distance(points, (t % 1.0) * total)


def arrow_head(draw, a, b, stroke, width=2):
    angle = math.atan2(b[1] - a[1], b[0] - a[0])
    length = 14 + width
    spread = 0.52
    p1 = (b[0] - length * math.cos(angle - spread), b[1] - length * math.sin(angle - spread))
    p2 = (b[0] - length * math.cos(angle + spread), b[1] - length * math.sin(angle + spread))
    draw.line([(c(p1[0]), c(p1[1])), (c(b[0]), c(b[1])), (c(p2[0]), c(p2[1]))], fill=hex_rgba(stroke), width=max(1, c(width)))


def icon(ex, draw, kind, x, y, color=None, scale=1.0):
    color = color or THEME["cyan"]
    if kind == "folder":
        draw_line(ex, draw, [(x, y + 9 * scale), (x, y + 35 * scale), (x + 48 * scale, y + 35 * scale), (x + 48 * scale, y + 7 * scale), (x + 26 * scale, y + 7 * scale), (x + 21 * scale, y), (x + 2 * scale, y), (x + 2 * scale, y + 9 * scale)], THEME["white"], 2)
        draw_rect(ex, draw, x + 5 * scale, y + 15 * scale, 38 * scale, 15 * scale, color, color, 1, 3)
    elif kind == "file":
        draw_rect(ex, draw, x + 7 * scale, y, 33 * scale, 36 * scale, THEME["white"], color, 2, 4)
        draw_line(ex, draw, [(x + 15 * scale, y + 14 * scale), (x + 31 * scale, y + 14 * scale)], THEME["bg"], 2)
        draw_line(ex, draw, [(x + 15 * scale, y + 24 * scale), (x + 31 * scale, y + 24 * scale)], THEME["bg"], 2)
    elif kind == "scan":
        draw_ellipse(ex, draw, x + 14 * scale, y + 11 * scale, 38 * scale, 38 * scale, THEME["white"], None, 4 * scale)
        draw_line(ex, draw, [(x + 47 * scale, y + 45 * scale), (x + 64 * scale, y + 62 * scale)], THEME["white"], 5 * scale)
    elif kind == "shield":
        pts = [(x + 38 * scale, y + 7 * scale), (x + 63 * scale, y + 17 * scale), (x + 58 * scale, y + 47 * scale), (x + 38 * scale, y + 65 * scale), (x + 18 * scale, y + 47 * scale), (x + 13 * scale, y + 17 * scale)]
        draw.polygon([(c(px), c(py)) for px, py in pts], fill=hex_rgba(THEME["green"], 180), outline=hex_rgba(THEME["white"]))
        draw_line(ex, draw, pts + [pts[0]], THEME["white"], 3 * scale)
        draw_line(ex, draw, [(x + 27 * scale, y + 37 * scale), (x + 36 * scale, y + 48 * scale), (x + 51 * scale, y + 27 * scale)], THEME["white"], 4 * scale)
    elif kind == "db":
        draw_ellipse(ex, draw, x + 15 * scale, y + 9 * scale, 50 * scale, 17 * scale, THEME["white"], color, 2 * scale)
        draw_rect(ex, draw, x + 15 * scale, y + 17 * scale, 50 * scale, 37 * scale, THEME["white"], color, 2 * scale, 0)
        draw_ellipse(ex, draw, x + 15 * scale, y + 45 * scale, 50 * scale, 17 * scale, THEME["white"], color, 2 * scale)
    elif kind == "hash":
        draw_line(ex, draw, [(x + 27 * scale, y + 14 * scale), (x + 22 * scale, y + 58 * scale)], THEME["amber"], 4 * scale)
        draw_line(ex, draw, [(x + 50 * scale, y + 14 * scale), (x + 45 * scale, y + 58 * scale)], THEME["amber"], 4 * scale)
        draw_line(ex, draw, [(x + 15 * scale, y + 29 * scale), (x + 62 * scale, y + 29 * scale)], THEME["white"], 4 * scale)
        draw_line(ex, draw, [(x + 13 * scale, y + 45 * scale), (x + 60 * scale, y + 45 * scale)], THEME["white"], 4 * scale)
    elif kind == "package":
        draw_line(ex, draw, [(x + 38 * scale, y + 8 * scale), (x + 66 * scale, y + 23 * scale), (x + 66 * scale, y + 52 * scale), (x + 38 * scale, y + 68 * scale), (x + 10 * scale, y + 52 * scale), (x + 10 * scale, y + 23 * scale), (x + 38 * scale, y + 8 * scale)], THEME["white"], 3 * scale)
        draw_line(ex, draw, [(x + 10 * scale, y + 23 * scale), (x + 38 * scale, y + 38 * scale), (x + 66 * scale, y + 23 * scale)], THEME["amber"], 3 * scale)
        draw_line(ex, draw, [(x + 38 * scale, y + 38 * scale), (x + 38 * scale, y + 68 * scale)], THEME["amber"], 3 * scale)
    else:
        draw_ellipse(ex, draw, x + 18 * scale, y + 18 * scale, 36 * scale, 36 * scale, color, color, 2 * scale)


def draw_signature(ex, draw, text, x, y):
    ex.text(text, x, y, 120, 36, 23, THEME["white"], align="left")
    font = load_font(24, cjk=True, bold=True)
    sx, sy = c(x), c(y)
    for dx, dy, color, alpha in [(-1, 1, THEME["purple"], 165), (1, -1, THEME["cyan"], 135), (0, 0, THEME["white"], 245)]:
        draw.text((sx + c(dx), sy + c(dy)), text, font=font, fill=hex_rgba(color, alpha))
    draw.line([(sx + 6, sy + 56), (sx + 28, sy + 61), (sx + 62, sy + 58), (sx + 86, sy + 63)], fill=hex_rgba(THEME["purple"], 170), width=3)
    draw.line([(sx + 8, sy + 54), (sx + 84, sy + 60)], fill=hex_rgba(THEME["white"], 125), width=1)


def brand(ex, draw, signature):
    dots = [
        (0, 0, THEME["cyan"]),
        (10, 8, THEME["white"]),
        (0, 16, THEME["purple"]),
        (10, 24, THEME["white"]),
        (20, 0, THEME["white"]),
        (30, 8, THEME["pink"]),
        (20, 16, THEME["white"]),
        (30, 24, THEME["green"]),
    ]
    for dx, dy, color in dots:
        draw_ellipse(ex, draw, 955 + dx, 143 + dy, 5, 5, color, color, 1)
    draw_signature(ex, draw, signature, 998, 135)


def small_input(ex, draw, x, y, item):
    kind = item.get("icon", "file")
    color = item.get("color", THEME["cyan"])
    icon(ex, draw, kind, x + 25, y + 2, color, 0.54)
    draw_text(ex, draw, item.get("label", ""), x - 7, y + 36, 82, 22, 13, THEME["white"], "center", fit=True, min_size=10)


def core_card(ex, draw, x, y, card):
    draw_rect(ex, draw, x, y, 260, 90, THEME["core_stroke"], THEME["blue_fill"], 2, 9)
    icon(ex, draw, card.get("icon", "file"), x + 16, y + 16, card.get("color", THEME["cyan"]), 0.86)
    draw_text(ex, draw, card.get("title", ""), x + 110, y + 11, 100, 28, 20, THEME["white"], "center", hand=True, bold=True, fit=True, min_size=15)
    draw_text(ex, draw, card.get("body", ""), x + 92, y + 42, 150, 38, 15, THEME["white"], "center", spacing=3, fit=True, min_size=11)


def mini_card(ex, draw, x, y, w, h, card, stroke, fill):
    draw_rect(ex, draw, x, y, w, h, stroke, fill, 2, 8)
    icon(ex, draw, card.get("icon", "file"), x + 12, y + 13, card.get("color", THEME["cyan"]), 0.76)
    draw_text(ex, draw, card.get("title", ""), x + 72, y + 11, 130, 25, 18, THEME["white"], "left", bold=True, fit=True, min_size=13)
    draw_text(ex, draw, card.get("body", ""), x + 72, y + 39, w - 86, h - 42, 13, THEME["white"], "left", spacing=3, fit=True, min_size=10)


def pack_row(ex, draw, x, y, card):
    draw_rect(ex, draw, x, y, 228, 84, THEME["green"], THEME["pack_row_fill"], 2, 8)
    icon(ex, draw, card.get("icon", "file"), x + 14, y + 14, card.get("color", THEME["cyan"]), 0.76)
    draw_text(ex, draw, card.get("title", ""), x + 78, y + 12, 135, 25, 18, THEME["white"], "center", bold=True, fit=True, min_size=12)
    draw_text(ex, draw, card.get("body", ""), x + 76, y + 42, 140, 30, 13, THEME["white"], "center", spacing=3, fit=True, min_size=10)


def render_static(spec):
    width = spec.get("canvas", {}).get("width", DEFAULT_W)
    height = spec.get("canvas", {}).get("height", DEFAULT_H)
    ex = Excal(width, height)
    img = Image.new("RGBA", (width * SCALE, height * SCALE), hex_rgba(THEME["bg"]))
    draw = ImageDraw.Draw(img)

    title = spec.get("title", {})
    draw_line(ex, draw, [(29, 31), (29, 78)], THEME["purple"], 11)
    draw_text(ex, draw, title.get("prefix", "The internals of"), 45, 14, 535, 66, 47, THEME["white"], "left", hand=True, bold=True)
    draw_rect(ex, draw, 600, 27, 392, 72, THEME["highlight"], THEME["highlight"], 2, 16)
    draw_text(ex, draw, title.get("highlight", "Memory Pack"), 622, 19, 350, 76, 44, THEME["green"], "center", hand=True, bold=True)
    draw_text(ex, draw, title.get("subtitle", ""), 104, 90, 420, 25, 15, THEME["muted"], "left")

    draw_rect(ex, draw, 18, 117, 1174, 994, THEME["frame"], None, 2, 29)
    if spec.get("signature", "@岚叔"):
        brand(ex, draw, spec.get("signature", "@岚叔"))

    inputs = spec.get("inputs", [])
    while len(inputs) < 4:
        inputs.append({"label": "", "icon": "file"})
    draw_rect(ex, draw, 389, 138, 430, 101, THEME["green"], None, 2, 8)
    draw_text(ex, draw, spec.get("input_title", "Source / Input"), 498, 144, 210, 31, 22, THEME["white"], "center", hand=True, bold=True)
    for x, item in zip([423, 532, 640, 748], inputs[:4]):
        small_input(ex, draw, x, 180, item)
    draw_line(ex, draw, [(605, 239), (605, 316)], THEME["white"], 2, "solid", True)

    core = spec.get("core", {})
    cards = core.get("cards", [])
    while len(cards) < 3:
        cards.append({"title": "", "body": "", "icon": "file"})
    draw_rect(ex, draw, 53, 317, 1104, 320, THEME["core_stroke"], THEME["core_fill"], 2, 20)
    draw_text(ex, draw, core.get("title", "Archive Core"), 462, 327, 210, 31, 22, THEME["white"], "center", hand=True, bold=True)
    draw_text(ex, draw, core.get("subtitle", "(local read-only pipeline)"), 635, 336, 220, 23, 13, THEME["white"], "center")
    core_card(ex, draw, 95, 366, cards[0])
    core_card(ex, draw, 472, 366, cards[1])
    core_card(ex, draw, 850, 366, cards[2])
    draw_line(ex, draw, [(355, 411), (472, 411)], THEME["white"], 2, "solid", True)
    draw_line(ex, draw, [(732, 411), (850, 411)], THEME["white"], 2, "solid", True)
    draw_line(ex, draw, [(982, 456), (982, 481), (768, 481), (768, 508)], THEME["white"], 2, "solid", True)

    decision = spec.get("decision", {"title": "Ready?", "body": "safe, traced\nusable"})
    draw_diamond(ex, draw, 706, 508, 120, 120, THEME["green"], THEME["decision_fill"], 2)
    draw_text(ex, draw, decision.get("title", "Ready?"), 728, 541, 78, 26, 20, THEME["white"], "center", fit=True, min_size=14)
    draw_text(ex, draw, decision.get("body", ""), 728, 569, 78, 34, 14, THEME["white"], "center", fit=True, min_size=10)
    draw_rect(ex, draw, 1022, 527, 112, 94, THEME["core_stroke"], THEME["blue_fill"], 2, 9)
    icon(ex, draw, spec.get("output", {}).get("icon", "file"), 1050, 535, THEME["cyan"], 0.62)
    draw_text(ex, draw, spec.get("output", {}).get("label", "Report"), 1041, 588, 75, 25, 18, THEME["white"], "center", bold=True, fit=True, min_size=12)
    draw_line(ex, draw, [(826, 568), (1022, 568)], THEME["white"], 2, "solid", True)
    draw_text(ex, draw, spec.get("yes_label", "是"), 900, 543, 45, 25, 15, THEME["white"], "center")
    draw_line(ex, draw, [(707, 568), (510, 568), (222, 568), (222, 456)], THEME["muted"], 2, "dashed", True)
    draw_text(ex, draw, spec.get("loop_label", "Loop until checked and updated"), 330, 504, 540, 25, 14, THEME["white"], "center")
    draw_text(ex, draw, spec.get("retry_label", "No / missing source or conflict"), 475, 580, 250, 24, 14, THEME["white"], "center")

    draw_line(ex, draw, [(156, 637), (156, 736)], THEME["white"], 2, "solid", True)
    draw_line(ex, draw, [(205, 736), (205, 637)], THEME["white"], 2, "solid", True)
    draw_text(ex, draw, spec.get("read_label", "读取"), 109, 677, 45, 22, 16, THEME["white"], "center")
    draw_text(ex, draw, spec.get("context_label", "上下文"), 211, 676, 70, 22, 16, THEME["white"], "center")

    left = spec.get("left_panel", {})
    draw_rect(ex, draw, 39, 735, 281, 344, THEME["green"], THEME["source_fill"], 2, 14)
    draw_text(ex, draw, left.get("title", "Memory Sources"), 58, 752, 180, 30, 22, THEME["white"], "left", hand=True, bold=True)
    draw_text(ex, draw, left.get("badge", "read only"), 244, 779, 62, 18, 11, THEME["green"], "center")
    for (y, h), card in zip([(797, 78), (892, 78), (987, 62)], left.get("cards", [])[:3]):
        mini_card(ex, draw, 51, y, 258, h, card, THEME["green"], THEME["mini_fill"])

    center = spec.get("center_panel", {})
    draw_rect(ex, draw, 333, 734, 522, 346, THEME["purple"], THEME["archive_fill"], 2, 14)
    draw_text(ex, draw, center.get("title", "Archive Layers"), 512, 756, 180, 34, 23, THEME["white"], "center", hand=True, bold=True)
    draw_text(ex, draw, center.get("subtitle", "(local, readable, traceable storage)"), 444, 790, 300, 24, 14, THEME["white"], "center")
    layer_cards = center.get("cards", [])[:4]
    while len(layer_cards) < 4:
        layer_cards.append({"title": "", "body": "", "icon": "file"})
    for x, card in zip([346, 474, 602, 730], layer_cards):
        draw_rect(ex, draw, x, 827, 112, 142, THEME["purple"], THEME["center_card_fill"], 2, 8)
        icon(ex, draw, card.get("icon", "file"), x + 24, 846, card.get("color", THEME["cyan"],), 0.78)
        draw_text(ex, draw, card.get("title", ""), x + 10, 910, 92, 25, 18, THEME["white"], "center", bold=True, fit=True, min_size=12)
        draw_text(ex, draw, card.get("body", ""), x + 8, 936, 96, 30, 12, THEME["white"], "center", spacing=2, fit=True, min_size=9)
    draw_line(ex, draw, [(458, 890), (474, 890)], THEME["white"], 2, "solid", True)
    draw_line(ex, draw, [(586, 890), (602, 890)], THEME["white"], 2, "solid", True)
    draw_line(ex, draw, [(714, 890), (730, 890)], THEME["white"], 2, "solid", True)
    draw_rect(ex, draw, 491, 1010, 220, 50, THEME["purple"], THEME["archive_fill"], 2, 8)
    draw_text(ex, draw, center.get("footer", "Redact + Dedup"), 528, 1017, 165, 33, 20, THEME["white"], "center", hand=True, bold=True, fit=True, min_size=14)
    draw_line(ex, draw, [(603, 969), (603, 1010)], THEME["muted"], 2, "dashed", True)

    right = spec.get("right_panel", {})
    draw_line(ex, draw, [(855, 890), (904, 890)], THEME["white"], 2, "solid", True)
    draw_text(ex, draw, right.get("incoming_label", "Compile"), 850, 868, 65, 20, 12, THEME["white"], "center")
    draw_rect(ex, draw, 904, 735, 258, 344, THEME["green"], THEME["pack_fill"], 2, 14)
    draw_text(ex, draw, right.get("title", "Memory Pack"), 948, 750, 170, 34, 22, THEME["white"], "center", hand=True, bold=True)
    for y, card in zip([786, 884, 982], right.get("cards", [])[:3]):
        pack_row(ex, draw, 918, y, card)
    draw_line(ex, draw, [(1036, 735), (1036, 691), (766, 691), (766, 628)], THEME["white"], 2, "solid", True)
    draw_text(ex, draw, right.get("return_label", "Reusable"), 867, 669, 75, 23, 16, THEME["white"], "center")

    if spec.get("show_decorations", True):
        for x, y, color in [(375, 292, THEME["cyan"]), (704, 293, THEME["green"]), (1048, 292, THEME["purple"]), (315, 707, THEME["green"]), (868, 707, THEME["purple"])]:
            draw_line(ex, draw, [(x - 8, y), (x + 8, y)], color, 2)
            draw_line(ex, draw, [(x, y - 8), (x, y + 8)], color, 2)

    return ex, img.resize((width, height), Image.Resampling.LANCZOS).convert("RGB")


def premium_finish(base):
    width, height = base.size
    img = base.convert("RGBA")
    glow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    g = ImageDraw.Draw(glow)
    for rect, color, line_width in [
        ((18, 117, 1192, 1111), THEME["frame"], 3),
        ((53, 317, 1157, 637), THEME["core_stroke"], 3),
        ((333, 734, 855, 1080), THEME["purple"], 3),
        ((39, 735, 320, 1079), THEME["green"], 3),
        ((904, 735, 1162, 1079), THEME["green"], 3),
        ((600, 27, 992, 99), THEME["green"], 2),
    ]:
        g.rounded_rectangle(rect, radius=18, outline=hex_rgba(color, 70), width=line_width)
    img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(4)))

    grain = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grain)
    rng = random.Random(2069769416930414980)
    for _ in range(2600):
        x = rng.randrange(width)
        y = rng.randrange(height)
        tone = rng.randrange(120, 220)
        gd.point((x, y), fill=(tone, tone, tone, rng.randrange(4, 14)))
    img.alpha_composite(grain)

    mask_small = Image.new("L", (180, 170), 0)
    pixels = []
    cx, cy = 90, 78
    max_dist = math.dist((0, 0), (cx, cy))
    for y in range(170):
        for x in range(180):
            dist = math.dist((x, y), (cx, cy)) / max_dist
            pixels.append(int(max(0, min(115, (dist - 0.38) * 150))))
    mask_small.putdata(pixels)
    mask = mask_small.resize((width, height), Image.Resampling.BICUBIC)
    vignette = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    vignette.putalpha(mask)
    img.alpha_composite(vignette)
    return img.convert("RGB")


def draw_glow_dot(draw, x, y, color, strength=1.0):
    for radius, alpha in [(15, 42), (10, 70), (5, 210)]:
        a = int(alpha * strength)
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=hex_rgba(color, a))
    draw.ellipse((x - 2, y - 2, x + 2, y + 2), fill=hex_rgba(THEME["white"], 245))


def pulse_rect(draw, rect, color, phase, radius=10):
    x1, y1, x2, y2 = rect
    alpha = int(70 + 70 * (0.5 + 0.5 * math.sin(phase)))
    for grow, width in [(0, 2), (4, 2), (8, 1)]:
        draw.rounded_rectangle((x1 - grow, y1 - grow, x2 + grow, y2 + grow), radius=radius + grow, outline=hex_rgba(color, max(25, alpha - grow * 8)), width=width)


def animate_frame(base, idx, total):
    frame = base.convert("RGBA")
    overlay = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    progress = idx / total
    paths = [
        ([(605, 239), (605, 316)], THEME["green"], 0.00),
        ([(355, 411), (472, 411)], THEME["cyan"], 0.10),
        ([(732, 411), (850, 411)], THEME["cyan"], 0.24),
        ([(982, 456), (982, 481), (768, 481), (768, 508)], THEME["core_stroke"], 0.38),
        ([(826, 568), (1022, 568)], THEME["green"], 0.54),
        ([(707, 568), (510, 568), (222, 568), (222, 456)], THEME["purple"], 0.66),
        ([(156, 637), (156, 736)], THEME["green"], 0.18),
        ([(205, 736), (205, 637)], THEME["green"], 0.58),
        ([(458, 890), (486, 890), (598, 890), (626, 890), (738, 890), (766, 890)], THEME["purple"], 0.32),
        ([(855, 890), (904, 890)], THEME["white"], 0.46),
        ([(1036, 735), (1036, 691), (766, 691), (766, 628)], THEME["amber"], 0.72),
    ]
    for points, color, offset in paths:
        for trail, strength in [(0, 1.0), (-0.035, 0.72), (-0.07, 0.44)]:
            x, y = point_at_fraction(points, progress + offset + trail)
            draw_glow_dot(draw, x, y, color, strength)
    pulse_targets = [
        ((389, 138, 819, 239), THEME["green"]),
        ((95, 366, 355, 456), THEME["core_stroke"]),
        ((472, 366, 732, 456), THEME["green"]),
        ((850, 366, 1110, 456), THEME["core_stroke"]),
        ((706, 508, 826, 628), THEME["green"]),
        ((333, 734, 855, 1080), THEME["purple"]),
        ((904, 735, 1162, 1079), THEME["green"]),
    ]
    active = (idx // 6) % len(pulse_targets)
    for pos, (rect, color) in enumerate(pulse_targets):
        if pos == active:
            pulse_rect(draw, rect, color, progress * math.tau * 2, 12)
    frame.alpha_composite(overlay)
    return frame.convert("RGB")


def write_outputs(spec, outdir, basename, style_id=None):
    spec = prepare_spec(spec, style_id)
    outdir.mkdir(parents=True, exist_ok=True)
    ex, static = render_static(spec)
    final = premium_finish(static)
    png_path = outdir / f"{basename}.png"
    gif_path = outdir / f"{basename}.gif"
    excalidraw_path = outdir / f"{basename}.excalidraw"
    final.save(png_path, "PNG")
    frames = [animate_frame(final, i, spec.get("canvas", {}).get("frames", DEFAULT_FRAMES)) for i in range(spec.get("canvas", {}).get("frames", DEFAULT_FRAMES))]
    duration = int(1000 / spec.get("canvas", {}).get("fps", DEFAULT_FPS))
    frames[0].save(gif_path, save_all=True, append_images=frames[1:], duration=duration, loop=0, optimize=False)
    ex.write(excalidraw_path)
    return {"png": str(png_path), "gif": str(gif_path), "excalidraw": str(excalidraw_path), "elements": len(ex.elements), "style": spec["style"]}


def frame_diff_report(gif_path):
    with Image.open(gif_path) as im:
        picks = [0, max(1, im.n_frames // 4), max(2, im.n_frames // 2), max(3, 3 * im.n_frames // 4), im.n_frames - 1]
        frames = []
        for idx in picks:
            im.seek(idx)
            frames.append(im.convert("RGB"))
        frame_count = im.n_frames
    diffs = []
    for left, right, a, b in zip(frames, frames[1:], picks, picks[1:]):
        diff = ImageChops.difference(left, right)
        bbox = diff.getbbox()
        changed = 0
        if bbox:
            cropped = diff.crop(bbox)
            data = cropped.get_flattened_data() if hasattr(cropped, "get_flattened_data") else cropped.getdata()
            changed = sum(1 for px in data if px != (0, 0, 0))
        diffs.append({"from": a, "to": b, "changed_pixels": changed})
    return {"frames": frame_count, "diffs": diffs}


def check_outputs(result, spec):
    canvas = spec.get("canvas", {})
    expected_width = canvas.get("width", DEFAULT_W)
    expected_height = canvas.get("height", DEFAULT_H)
    expected_frames = canvas.get("frames", DEFAULT_FRAMES)
    expected_fps = canvas.get("fps", DEFAULT_FPS)

    checks = []

    gif_path = Path(result["gif"])
    with Image.open(gif_path) as gif:
        gif_width = gif.width
        gif_height = gif.height
        gif_frames = gif.n_frames
        duration_ms = gif.info.get("duration")
    actual_fps = round(1000 / duration_ms, 3) if duration_ms else None
    checks.extend(
        [
            {"name": "gif_exists", "ok": gif_path.is_file()},
            {"name": "gif_width", "ok": gif_width == expected_width, "expected": expected_width, "actual": gif_width},
            {"name": "gif_height", "ok": gif_height == expected_height, "expected": expected_height, "actual": gif_height},
            {"name": "gif_frames", "ok": gif_frames == expected_frames, "expected": expected_frames, "actual": gif_frames},
            {"name": "gif_fps", "ok": duration_ms == int(1000 / expected_fps), "expected": expected_fps, "actual": actual_fps},
        ]
    )

    diff_report = frame_diff_report(gif_path)
    checks.append(
        {
            "name": "gif_has_motion",
            "ok": any(item["changed_pixels"] > 0 for item in diff_report["diffs"]),
            "diffs": diff_report["diffs"],
        }
    )

    excalidraw_path = Path(result["excalidraw"])
    excalidraw = json.loads(excalidraw_path.read_text(encoding="utf-8"))
    elements = excalidraw.get("elements", [])
    ids = [element.get("id") for element in elements]
    text_elements = [element for element in elements if element.get("type") == "text"]
    checks.extend(
        [
            {"name": "excalidraw_exists", "ok": excalidraw_path.is_file()},
            {"name": "excalidraw_unique_ids", "ok": len(ids) == len(set(ids))},
            {"name": "excalidraw_text_font_family", "ok": all(element.get("fontFamily") == 5 for element in text_elements)},
            {"name": "excalidraw_files_empty", "ok": excalidraw.get("files") == {}},
        ]
    )

    png_path = Path(result["png"])
    with Image.open(png_path) as png:
        png_width = png.width
        png_height = png.height
    checks.extend(
        [
            {"name": "png_exists", "ok": png_path.is_file()},
            {"name": "png_width", "ok": png_width == expected_width, "expected": expected_width, "actual": png_width},
            {"name": "png_height", "ok": png_height == expected_height, "expected": expected_height, "actual": png_height},
        ]
    )

    return {"ok": all(check["ok"] for check in checks), "checks": checks}


def main():
    parser = argparse.ArgumentParser(description="Render a premium hand-drawn animated diagram from a JSON spec.")
    parser.add_argument("--spec", help="Path to spec JSON.")
    parser.add_argument("--outdir", help="Output directory.")
    parser.add_argument("--basename", default="animated-diagram", help="Output basename.")
    parser.add_argument("--style", choices=sorted(STYLE_THEMES), help="Override the style declared in the spec.")
    parser.add_argument("--list-styles", action="store_true", help="Print available style IDs and exit.")
    parser.add_argument("--verify", action="store_true", help="Print frame-diff verification after rendering.")
    parser.add_argument("--check", action="store_true", help="Validate PNG, GIF, and Excalidraw output contracts; exits nonzero on failure.")
    args = parser.parse_args()

    if args.list_styles:
        print(json.dumps(available_styles(), ensure_ascii=False, indent=2))
        return
    if not args.spec:
        parser.error("--spec is required unless --list-styles is used")
    if not args.outdir:
        parser.error("--outdir is required unless --list-styles is used")

    spec = json.loads(Path(args.spec).read_text(encoding="utf-8"))
    result = write_outputs(spec, Path(args.outdir), args.basename, style_id=args.style)
    if args.verify:
        result["verification"] = frame_diff_report(result["gif"])
    if args.check:
        result["checks"] = check_outputs(result, spec)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if args.check and not result["checks"]["ok"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
