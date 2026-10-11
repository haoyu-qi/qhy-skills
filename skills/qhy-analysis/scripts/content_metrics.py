#!/usr/bin/env python3
"""Calculate descriptive video metrics from local JSON; no network or traffic labels.

Python 3.8+, standard library only. Missing fields stay missing; zero views
do not produce rates. Aggregate denominators include only observed fields.
"""
import argparse
import json
import statistics
import sys
from pathlib import Path

METRICS = ("like", "favorite", "coin", "share")


def nonnegative_integer(value):
    return type(value) is int and value >= 0


def analyse(data):
    rows = data.get("videos") if isinstance(data, dict) else data
    if not isinstance(rows, list):
        raise ValueError("输入必须为数组或含 videos 数组的对象")
    videos, errors, seen_ids = [], [], set()
    for index, row in enumerate(rows, 1):
        try:
            if not isinstance(row, dict):
                raise ValueError("视频记录必须是对象")
            if not nonnegative_integer(row.get("view")):
                raise ValueError("view 必须为非负整数")
            for key in METRICS:
                if key in row and not nonnegative_integer(row[key]):
                    raise ValueError("{} 必须为非负整数，缺失请省略字段".format(key))
            for key in ("title", "format"):
                if key in row and not isinstance(row[key], str):
                    raise ValueError("{} 必须为字符串".format(key))
            identity = row.get("id", "row-{}".format(index))
            if not isinstance(identity, str) or not identity.strip():
                raise ValueError("id 必须为非空字符串")
            if identity in seen_ids:
                raise ValueError("重复 id：{}".format(identity))
            seen_ids.add(identity)
            video = {"id": identity, "title": row.get("title", identity), "view": row["view"],
                     "format": row.get("format", "").strip() or "未分类"}
            video["counts"] = {key: row.get(key) for key in METRICS}
            video["rates_per_1000"] = {
                key: row[key] / row["view"] * 1000 if row["view"] and key in row else None
                for key in METRICS}
            video["like_coin_ratio"] = row["like"] / row["coin"] if (
                "like" in row and row.get("coin", 0) > 0) else None
            videos.append(video)
        except ValueError as exc:
            errors.append({"row": index, "error": str(exc)})

    groups = []
    for fmt in sorted({video["format"] for video in videos}):
        group = [video for video in videos if video["format"] == fmt]
        summary = {"format": fmt, "videos": len(group), "total_views": sum(v["view"] for v in group),
                   "zero_view_videos": sum(v["view"] == 0 for v in group), "metrics": {}}
        for key in METRICS:
            valid = [v for v in group if v["rates_per_1000"][key] is not None]
            denominator = sum(v["view"] for v in valid)
            numerator = sum(v["counts"][key] for v in valid)
            summary["metrics"][key] = {
                "observed_field_videos": sum(v["counts"][key] is not None for v in group),
                "rate_videos": len(valid), "missing_field_videos": sum(v["counts"][key] is None for v in group),
                "denominator_views": denominator, "numerator_interactions": numerator,
                "aggregate_per_1000": numerator / denominator * 1000 if denominator else None,
                "median_per_1000": statistics.median(v["rates_per_1000"][key] for v in valid) if valid else None,
            }
        groups.append(summary)
    return {"notice": "描述性统计，不判断投流、活动、自然流量或创作因果。缺失不填零。",
            "input_rows": len(rows), "videos": videos, "groups": groups, "errors": errors}


def display(value):
    return "缺失/不适用" if value is None else "{:.2f}".format(value)


def markdown(report):
    lines = ["# 内容表现统计", "", report["notice"], "",
             "有效记录：{}；错误：{}。".format(len(report["videos"]), len(report["errors"]))]
    for group in report["groups"]:
        lines.extend(["", "## {}".format(group["format"]), "",
                      "{} 条；总播放 {}；零播放 {}。".format(
                          group["videos"], group["total_views"], group["zero_view_videos"]), "",
                      "| 字段 | 有效比率样本 | 缺字段 | 比率分母播放 | 组合率‰ | 视频中位‰ |",
                      "| --- | --- | --- | --- | --- | --- |"])
        for key, item in group["metrics"].items():
            lines.append("| {} | {} | {} | {} | {} | {} |".format(
                key, item["rate_videos"], item["missing_field_videos"], item["denominator_views"],
                display(item["aggregate_per_1000"]), display(item["median_per_1000"])))
    for item in report["errors"]:
        lines.append("\n- 输入第 {} 条：{}".format(item["row"], item["error"]))
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", help="Local UTF-8 JSON file or - for stdin")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        raw = sys.stdin.read() if args.file == "-" else Path(args.file).read_text(encoding="utf-8")
        report = analyse(json.loads(raw))
    except (ValueError, OSError, UnicodeError) as exc:
        parser.exit(2, "输入失败：{}\n".format(exc))
    print(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False) if args.json else markdown(report))
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
