---
name: qhy-bug-xlsx
description: QHY bug Excel organizer for importing ZenTao/禅道 bug-list exports and producing a cleaned bug整理表 workbook with 总览, 全部明细, and T0明细 sheets. Use when the user asks to 导入禅道 bug-list, 整理禅道 Bug, 输出 bug 整理表, process ZenTao .xlsx/.xls/.csv bug exports, or clean bug lists with fields such as Bug编号, Bug标题, 严重程度, 解决方案, 解决日期.
---

# QHY Bug XLSX

## Purpose

Use this skill to turn a ZenTao/禅道 bug-list export into a readable QHY bug整理表. Keep the source workbook unchanged and write a new `.xlsx` artifact under `outputs/<task-name>/`.

## Default Output

Generate these sheets:

- `总览`: summary worksheet with total counts, T0 count, open/deferred count, P1 count, resolved count, status distribution, module distribution, and a focused issue snapshot.
- `全部明细`: normalized full bug list from all source sheets.
- `T0明细`: normalized rows from the `T0` source sheet when present.

Use a unified neutral table style. Keep title rows, header rows, and data rows consistently spaced across all output sheets.

## Normalization

Preserve the original bug title and solution text in the detail sheets. Normalize only helper fields:

- trim bug IDs and text cells
- extract numeric severity from values such as `2(#2)`
- classify `状态归类` from `解决方案`
- classify `模块` from `Bug标题`
- split Excel serial dates from free-text notes in `解决日期`
- produce `处理建议` and `计划/提示` from the status text

For detailed field/module rules, read `references/classification.md` when adjusting classification behavior.

## Script

Use `scripts/organize_buglist.mjs` for repeatable processing.

```bash
ARTIFACT_TOOL_NODE_MODULES=<bundled-node_modules> node scripts/organize_buglist.mjs <zentao-bug-list.xlsx> <output-dir> [output-name.xlsx]
```

In Codex Desktop, call `load_workspace_dependencies`, set `ARTIFACT_TOOL_NODE_MODULES` to the returned Node.js packages path, and run the bundled Node executable.

## Validation

After export:

1. Reopen the workbook and confirm sheets include `总览`, `全部明细`, `T0明细`.
2. Scan for formula/display errors such as `#REF!`, `#VALUE!`, `#NAME?`, `#N/A`.
3. Render representative sheets to verify row spacing, wrapping, and table readability.

Final response should include a short summary and a direct link to the final workbook.
