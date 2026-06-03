# Software Iteration Task Template

## Scope

- Applies to software version iterations for client, mobile, server, and platform products.
- Use for creating monthly ZenTao executions and task lists.
- Use the concrete project/product names from the user or from ZenTao context.

## Execution Naming

Recommended pattern:

```text
{项目/产品简称}{月份}月迭代
```

Examples:

```text
X86客户端6月迭代
移动端7月迭代
服务端8月迭代
```

## Fixed First-Level Stage Tasks

Create these five first-level tasks in order:

| Order | Task Name | Goal |
| --- | --- | --- |
| 1 | 阶段一：需求明确阶段 | 明确版本范围、需求边界、优先级和交付目标 |
| 2 | 阶段二：需求设计阶段 | 完成产品方案、交互说明、技术评审和风险识别 |
| 3 | 阶段三：功能开发阶段 | 完成功能开发、自测和代码合入 |
| 4 | 阶段四：测试验证阶段 | 完成集成测试、回归测试、缺陷验证和准出确认 |
| 5 | 阶段五：版本发布阶段 | 完成版本包整理、发布说明、上线发布和发布确认 |

Do not create these as default stages:

- 问题修复阶段
- 生命周期维护阶段
- 停产阶段

If concentrated bug fixing is needed, track it under `阶段四：测试验证阶段` or create specific bug-fix tasks, not a fixed lifecycle stage.

## Owner Suggestions

| Stage | Suggested Owner |
| --- | --- |
| 阶段一：需求明确阶段 | 项目/产品负责人 |
| 阶段二：需求设计阶段 | 产品/研发负责人 |
| 阶段三：功能开发阶段 | 研发负责人 |
| 阶段四：测试验证阶段 | 测试/研发负责人 |
| 阶段五：版本发布阶段 | 发布/测试负责人 |

## Schedule Suggestions

For a four-week monthly iteration:

| Stage | Suggested Window |
| --- | --- |
| 阶段一：需求明确阶段 | 第 1 周前半 |
| 阶段二：需求设计阶段 | 第 1 周后半到第 2 周初 |
| 阶段三：功能开发阶段 | 第 2 周到第 3 周 |
| 阶段四：测试验证阶段 | 第 4 周前半 |
| 阶段五：版本发布阶段 | 第 4 周后半 |

## Requirement-Based Subtask Decomposition

When a requirement document, requirement link, requirement ID, or feature list is available, extract:

| Source Information | Use |
| --- | --- |
| 功能模块/功能点 | 拆分功能开发子任务 |
| 用户场景/业务流程 | 补充需求明确和需求设计子任务 |
| 交互说明/页面规则 | 拆分产品设计、交互确认、前端实现任务 |
| 接口/数据/权限规则 | 拆分后端、联调、兼容性任务 |
| 验收标准 | 拆分测试验证子任务 |
| 依赖项/风险点 | 拆分评审、联调、风险验证任务 |
| 发布影响范围 | 拆分版本发布、发布说明、上线检查任务 |

Subtask naming pattern:

```text
{功能/模块} - {动作}
```

Examples:

```text
会议调度 - 梳理业务流程
会议调度 - 完成交互设计
会议调度 - 实现窗口保留逻辑
会议调度 - 补充回归测试用例
会议调度 - 更新版本发布说明
```

Stage mapping:

| Stage | Subtask Sources |
| --- | --- |
| 阶段一：需求明确阶段 | 需求范围、业务目标、边界条件、优先级确认 |
| 阶段二：需求设计阶段 | 产品方案、交互设计、技术方案、接口设计、风险评审 |
| 阶段三：功能开发阶段 | 前端实现、后端实现、客户端实现、接口联调、自测 |
| 阶段四：测试验证阶段 | 测试用例、集成测试、回归测试、缺陷验证、准出检查 |
| 阶段五：版本发布阶段 | 发版清单、发布说明、安装包/构建物、上线验证、归档 |

Quality rules:

- Each subtask must have a clear owner.
- Each subtask must have a verifiable completion condition.
- A subtask should not span multiple stages.
- If requirements are unclear, create clarification subtasks under `阶段一：需求明确阶段`.
- If technical risk is high, create validation or review subtasks under `阶段二：需求设计阶段`.

## ZenTao Creation Rules

1. Create or update the execution with the selected product, project, branch, date range, and concise name.
2. Create the five fixed first-level stage tasks.
3. Ask whether to create subtasks before creating them.
4. If the user confirms subtasks, prioritize requirement-document-based decomposition.
5. If there is no requirement document, use standard or custom decomposition only after clarifying with the user.
6. Verify by listing tasks from the execution.
7. Summarize what was created, including execution ID and task IDs.

## Known X86 Client Example

- Execution ID: `295`
- Execution name: `X86客户端6月迭代`
- Product: `U8融合通信平台客户端`
- Product ID: `1`
- Project: `U8-X86-版本更新（闪电）-凌云版本`
- Project ID: `7`
- Stage tasks:
  - `882` `阶段一：需求明确阶段`
  - `884` `阶段二：需求设计阶段`
  - `885` `阶段三：功能开发阶段`
  - `886` `阶段四：测试验证阶段`
  - `887` `阶段五：版本发布阶段`
