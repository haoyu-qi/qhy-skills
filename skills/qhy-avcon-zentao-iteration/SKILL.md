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
5. Create exactly five first-level stage tasks unless the user explicitly requests a different structure:
   - `一、概念阶段`
   - `二、计划阶段`
   - `三、开发阶段`
   - `四、验证阶段`
   - `五、发布阶段`
6. Before creating subtasks, ask whether subtasks should be created.
7. If subtasks are requested, use the fixed default subtasks below for stages one, two, four, and five. For `三、开发阶段`, align subtasks with the requirement document when one is provided:
   - `一、概念阶段`
     - `需求说明书确认`
   - `二、计划阶段`
     - `项目计划规划与评审`
   - `三、开发阶段`
     - Extract modules, features, pages, interfaces, or deliverables from the requirement document.
     - Create development-stage subtasks using those extracted items.
     - If no requirement document or feature list is available, fall back to `模块一的测试`, `模块一的开发`, and `模块一的设计页面设计`.
   - `四、验证阶段`
     - `集成测试`
   - `五、发布阶段`
     - `版本发布评审`
     - `产品资料准备`
8. If requirement documents are provided, use them to generate `三、开发阶段` subtasks and to refine owners, deadlines, descriptions, and completion criteria. Do not replace the five-stage structure unless the user explicitly asks.
9. When creating real ZenTao subtasks, pass `parent` in the full `--data` JSON payload instead of as a standalone CLI flag, for example `zentao task create --data='{"executionID":306,"parent":970,"name":"..."}'`. Verify that the created task has the expected nonzero `parent`.
10. After writing to ZenTao, verify by listing the execution tasks and summarize task IDs, names, parent IDs, owners, and deadlines.

## Subtask Decision

Ask this before creating subtasks:

```text
是否需要在 5 个阶段任务下继续创建子任务？
```

If the user provides requirement documents, requirement links, requirement IDs, or a feature list, read that material to generate development-stage subtasks and refine task descriptions, owners, deadlines, module names, and acceptance criteria.

The default subtask structure is:

```text
一、概念阶段
- 需求说明书确认

二、计划阶段
- 项目计划规划与评审

三、开发阶段
- 按需求文档中的模块/功能点/页面/接口/交付物生成
- 无需求文档时兜底使用：模块一的测试、模块一的开发、模块一的设计页面设计

四、验证阶段
- 集成测试

五、发布阶段
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
