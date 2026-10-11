#!/usr/bin/env python3
"""Locate editorial candidates without modifying text or rating authorship.

Python 3.8+, standard library only. Candidates require contextual review.
"""
import argparse
import bisect
import json
import re
import sys
from pathlib import Path


PATTERNS = [
    ("空泛表达候选", r"赋能|抓手|全方位|深度融合|时代浪潮|日新月异|前所未有|保驾护航",
     "是否能指向具体对象、动作或依据？必要术语保留。"),
    ("引导套话候选", r"值得注意的是|不难看出|由此可见|综上所述|一句话总结",
     "是否提供范围、归因或实质导航？有作用则保留。"),
    ("开头结尾候选", r"在当今|让我们一起来看看|希望本文|希望对你有所帮助",
     "检查是否只是通用包装；引文或真实对话不改。"),
    ("强断言候选", r"一定|绝对|必然|毫无疑问|百分之百|永远",
     "检查语境和证据，不自动削弱作者观点或改变否定。"),
    ("反转句候选", r"不是[^。！？!?\n]{1,40}?而是|你以为[^。！？!?\n]{1,40}?其实",
     "真实排除/纠错保留，避免凭空假定读者误解。"),
]


def char_count(value):
    return len(re.findall(r"[\u3400-\u9fffA-Za-z0-9]", value))


def scan(value, mode="article"):
    line_starts = [0] + [m.end() for m in re.finditer("\n", value)]
    findings = []

    def add(kind, start, end, reason):
        line_index = bisect.bisect_right(line_starts, start) - 1
        findings.append({
            "category": kind, "line": line_index + 1,
            "column": start - line_starts[line_index] + 1,
            "offset": start, "end_offset": end,
            "text": value[start:end],
            "context": value[max(0, start - 18):min(len(value), end + 18)].replace("\n", " "),
            "review_question": reason,
        })

    for kind, pattern, reason in PATTERNS:
        for match in re.finditer(pattern, value):
            add(kind, match.start(), match.end(), reason)

    clauses = list(re.finditer(r"[^，,。！？!?；;：:\n]+", value))
    if mode == "speech":
        for match in clauses:
            if char_count(match.group()) > 25:
                add("口播气口候选", match.start(), match.end(),
                    "分句较长，需实际试读；不能仅凭字数拆坏条件和因果。")
    sentences = [char_count(m.group()) for m in re.finditer(r"[^。！？!?\n]+", value)
                 if char_count(m.group())]
    return {
        "mode": mode, "counted_characters": char_count(value),
        "nonempty_lines": sum(bool(line.strip()) for line in value.splitlines()),
        "sentence_count_approx": len(sentences),
        "notice": "仅定位编辑候选，不判作者身份、不评分、不自动改稿。引文、代码和正常术语也可能命中。",
        "findings": sorted(findings, key=lambda item: (item["offset"], item["category"])),
    }


def markdown(report):
    lines = ["# 文本编辑候选", "", report["notice"], "",
             "- 模式：{}；计数字符：{}；候选：{}".format(
                 report["mode"], report["counted_characters"], len(report["findings"])), ""]
    for item in report["findings"]:
        lines.extend(["- {}:{} {}：{}".format(item["line"], item["column"], item["category"],
                                             item["text"].strip().replace("\n", " ")),
                      "  {}".format(item["review_question"])])
    if not report["findings"]:
        lines.append("没有命中表层候选；仍需检查事实、逻辑与编辑范围。")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", help="UTF-8 text file or - for stdin")
    parser.add_argument("--mode", choices=("article", "speech"), default="article")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        value = sys.stdin.read() if args.file == "-" else Path(args.file).read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        parser.exit(2, "读取失败：{}\n".format(exc))
    report = scan(value, args.mode)
    print(json.dumps(report, ensure_ascii=False, indent=2) if args.json else markdown(report))


if __name__ == "__main__":
    main()
