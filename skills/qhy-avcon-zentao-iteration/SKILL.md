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
   - `阶段一：需求明确阶段`
   - `阶段二：需求设计阶段`
   - `阶段三：功能开发阶段`
   - `阶段四：测试验证阶段`
   - `阶段五：版本发布阶段`
6. Before creating subtasks, ask whether subtasks should be created.
7. If subtasks are requested, prefer requirement-document-based decomposition over generic subtasks for stages one through four.
8. For `阶段五：版本发布阶段`, do not decompose from requirement documents. Always create exactly these two fixed subtasks:
   - `版本发布评审`
   - `产品资料准备`
9. After writing to ZenTao, verify by listing the execution tasks and summarize task IDs, names, owners, and deadlines.

## Subtask Decision

Ask this before creating subtasks:

```text
是否需要在 5 个阶段任务下继续创建子任务？
```

If the user provides requirement documents, requirement links, requirement IDs, or a feature list, read that material and decompose subtasks from it for stages one through four.

`阶段五：版本发布阶段` is fixed and must not be decomposed from requirement documents. It contains only:

```text
版本发布评审
产品资料准备
```

If the user does not provide a requirement source, ask for one if the task has high specificity. For low-risk or generic setup, create only the five first-level stage tasks and note that subtasks were not created.

## Reference

Read `references/iteration-template.md` when:

- Creating a new software iteration task list.
- Updating the stage naming or fixed lifecycle rules.
- Creating subtasks from requirement documents.
- Explaining the AVCON/QHY ZenTao iteration standard.
