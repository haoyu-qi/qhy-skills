---
name: qhy-avcon-zentao-iteration
description: Create or update ZenTao software iteration executions and task lists for AVCON/QHY workflows. Use when the user asks to build, solidify, apply, or reuse a software iteration task template in ZenTao, including monthly iterations, lifecycle stage tasks, and subtasks generated from requirement documents.
---

# QHY AVCON ZenTao Iteration

Use this skill to create or maintain ZenTao software iteration task structures.

## Core Workflow

1. Use the existing `zentao-cli` skill for all ZenTao reads and writes.
2. Never read or display ZenTao credentials; let the CLI handle authentication.
3. Identify the target product, project, execution, iteration month, date range, and owner assumptions.
4. Create or update the execution with a concise name such as `{project/product short name}{month}月迭代`.
5. Before creating any task, apply [Task Numbering](#task-numbering) to its title. Create exactly five first-level stage tasks unless the user explicitly requests a different structure:
   - `概念阶段`
   - `计划阶段`
   - `开发阶段`
   - `验证阶段`
   - `发布阶段`
6. Before creating subtasks, ask whether subtasks should be created.
7. If subtasks are requested, use the fixed default subtasks below for stages one, two, four, and five. For `开发阶段`, align subtasks with the requirement document when one is provided:
   - `概念阶段`
     - `需求说明书确认`
   - `计划阶段`
     - `项目计划规划与评审`
   - `开发阶段`
     - Extract modules, features, pages, interfaces, or deliverables from the requirement document.
     - Create development-stage subtasks using those extracted items.
     - If no requirement document or feature list is available, fall back to `模块一的测试`, `模块一的开发`, and `模块一的设计页面设计`.
   - `验证阶段`
     - `集成测试`
   - `发布阶段`
     - `版本发布评审`
     - `产品资料准备`
8. If requirement documents are provided, use them to generate `开发阶段` subtasks and to refine owners, deadlines, descriptions, and completion criteria. Do not replace the five-stage structure unless the user explicitly asks.
9. When creating real ZenTao subtasks, pass `parent` in the full `--data` JSON payload instead of as a standalone CLI flag, for example `zentao task create --data='{"executionID":306,"parent":970,"name":"【任务01-01】 需求说明书确认"}'`. Verify that the created task has the expected nonzero `parent`.
10. After writing to ZenTao, list the execution tasks to verify the new title prefixes against the parent IDs and summarize task IDs, names, parent IDs, owners, and deadlines.

## Task Numbering

- Prefix each new title with `【任务编号】` and one space, using the actual parent hierarchy. Format first-level tasks as `【任务01】 任务名称`, their children as `【任务01-01】 子任务名称`, and deeper tasks as `【任务01-01-1】 下级任务名称`. Use two digits for the first two segments and unpadded numbers from the third segment onward.
- Before each creation batch, list the target execution's tasks across all statuses and pages, including subtasks. For first-level tasks, increment the highest first-level number in the execution. For subtasks, append the next number among the parent's direct children. Start an empty sequence at `01` for the first two levels or `1` from the third level onward. For example, with first-level tasks through `【任务14】` and children of `【任务11】` through `【任务11-08】`, use `【任务15】` for a new first-level task and `【任务11-09】` for the next child of task 11.
- For legacy titles, use numeric prefixes such as `05、` and stage prefixes such as `五、` when finding the highest sibling number or building a parent's prefix. Use the stage name after its prefix to identify the parent and preserve existing titles. For an unnumbered parent, reuse its path if its numbered children establish one. Otherwise reserve the next available number at the parent's level for its path and use that path when numbering its children. Include such reserved paths from existing child titles when counting used numbers.

## Subtask Decision

Ask this before creating subtasks:

```text
是否需要在 5 个阶段任务下继续创建子任务？
```

If the user provides requirement documents, requirement links, requirement IDs, or a feature list, read that material to generate development-stage subtasks and refine task descriptions, owners, deadlines, module names, and acceptance criteria.

The default subtask structure below lists base titles. Add the assigned sequence prefix when creating each task.

```text
概念阶段
- 需求说明书确认

计划阶段
- 项目计划规划与评审

开发阶段
- 按需求文档中的模块/功能点/页面/接口/交付物生成
- 无需求文档时兜底使用：模块一的测试、模块一的开发、模块一的设计页面设计

验证阶段
- 集成测试

发布阶段
- 版本发布评审
- 产品资料准备
```

If the user does not provide a requirement source, use the fallback development subtasks only after the user confirms subtasks should be created.

## Reference

Read `references/iteration-template.md` when:

- Creating a new software iteration task list.
- Updating the stage naming or fixed lifecycle rules.
- Creating subtasks from requirement documents.
- Explaining the AVCON/QHY ZenTao iteration standard.
