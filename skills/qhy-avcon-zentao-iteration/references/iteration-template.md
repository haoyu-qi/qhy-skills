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
| 1 | 一、概念阶段 | 确认需求说明书、版本目标和范围边界 |
| 2 | 二、计划阶段 | 完成项目计划规划、资源安排和计划评审 |
| 3 | 三、开发阶段 | 完成模块设计、开发实现和模块测试 |
| 4 | 四、验证阶段 | 完成集成测试和验证闭环 |
| 5 | 五、发布阶段 | 完成版本发布评审和产品资料准备 |

Do not create these as default stages:

- 问题修复阶段
- 生命周期维护阶段
- 停产阶段

If concentrated bug fixing is needed, track it under `四、验证阶段` or create specific bug-fix tasks, not a fixed lifecycle stage.

## Owner Suggestions

| Stage | Suggested Owner |
| --- | --- |
| 一、概念阶段 | 项目/产品负责人 |
| 二、计划阶段 | 项目经理/研发负责人 |
| 三、开发阶段 | 研发负责人 |
| 四、验证阶段 | 测试/研发负责人 |
| 五、发布阶段 | 发布/测试负责人 |

## Schedule Suggestions

For a four-week monthly iteration:

| Stage | Suggested Window |
| --- | --- |
| 一、概念阶段 | 第 1 周前半 |
| 二、计划阶段 | 第 1 周后半 |
| 三、开发阶段 | 第 2 周到第 3 周 |
| 四、验证阶段 | 第 4 周前半 |
| 五、发布阶段 | 第 4 周后半 |

## Default Subtasks

When the user confirms that subtasks should be created, use these defaults for stages one, two, four, and five. For `三、开发阶段`, generate subtasks from the requirement document when one is available.

| Parent Task | Order | Fixed Subtask | Goal |
| --- | --- | --- | --- |
| 一、概念阶段 | 1 | 需求说明书确认 | 确认需求说明书内容、范围、边界和版本目标 |
| 二、计划阶段 | 1 | 项目计划规划与评审 | 完成项目计划、排期、资源和风险评审 |
| 三、开发阶段 | 1..n | 按需求文档生成 | 从需求文档中的模块、功能点、页面、接口和交付物抽取开发任务 |
| 四、验证阶段 | 1 | 集成测试 | 完成系统集成测试、缺陷跟踪和验证 |
| 五、发布阶段 | 1 | 版本发布评审 | 确认版本范围、测试结论、遗留问题、发布风险和准出条件 |
| 五、发布阶段 | 2 | 产品资料准备 | 准备发布说明、版本范围、使用说明、验收材料和归档资料 |

Fallback development subtasks when no requirement document or feature list is available:

```text
模块一的测试
模块一的开发
模块一的设计页面设计
```

## Requirement-Based Development Subtasks

When a requirement document, requirement link, requirement ID, or feature list is available, use it to generate `三、开发阶段` subtasks. Keep the five parent stages unchanged.

| Source Information | Use |
| --- | --- |
| 功能模块/功能点 | 生成开发阶段子任务 |
| 用户场景/业务流程 | 补充 `需求说明书确认` 的确认要点 |
| 交互说明/页面规则 | 生成页面设计、前端实现或交互确认类开发子任务 |
| 接口/数据/权限规则 | 生成后端、接口、数据、权限或联调类开发子任务 |
| 验收标准 | 补充开发阶段子任务和 `集成测试` 的完成条件 |
| 依赖项/风险点 | 补充 `项目计划规划与评审` 和 `版本发布评审` 的风险项 |
| 发布影响范围 | 作为 `版本发布评审` 和 `产品资料准备` 的输入 |

Development subtask naming should follow the requirement document. Prefer concrete names from the document over generic placeholders.

Recommended naming patterns:

```text
{模块名}的开发
{模块名}的设计页面设计
{模块名}的接口开发
{模块名}的联调
{模块名}的自测
```

Examples:

```text
会议调度的开发
会议调度的设计页面设计
会议调度的接口开发
会议调度的联调
```

Only create `模块一的测试`, `模块一的开发`, and `模块一的设计页面设计` when no requirement document, feature list, or module name is available.

Stage mapping:

| Stage | Subtask Sources |
| --- | --- |
| 一、概念阶段 | 固定创建 `需求说明书确认` |
| 二、计划阶段 | 固定创建 `项目计划规划与评审` |
| 三、开发阶段 | 优先按需求文档生成；无需求文档时兜底创建 `模块一的测试`、`模块一的开发`、`模块一的设计页面设计` |
| 四、验证阶段 | 固定创建 `集成测试` |
| 五、发布阶段 | 固定创建 `版本发布评审`、`产品资料准备` |

Quality rules:

- Each subtask must have a clear owner.
- Each subtask must have a verifiable completion condition.
- A subtask should not span multiple stages.
- If requirements are unclear, capture clarification work under `需求说明书确认`.
- If technical risk is high, capture validation or review work under `项目计划规划与评审` or the relevant development/verification subtask.
- Development-stage subtasks must trace back to requirement document modules, features, pages, interfaces, or deliverables when that source exists.
- `五、发布阶段` must contain exactly `版本发布评审` and `产品资料准备` unless the user explicitly asks for additional release subtasks.

## ZenTao Parent/Child Task Creation

ZenTao CLI 0.1.8 does not expose `parent` as a standalone `task create` or `task update` option. To create real child tasks, pass `parent` in the full JSON request body:

```bash
zentao task create --data='{"executionID":306,"parent":970,"name":"系统界面网络连接、WiFi和IP配置的开发","type":"devel","assignedTo":"qihaoyu","deadline":"2026-06-16"}'
```

After creating subtasks, verify with:

```bash
zentao task --executionID=306 --status=all --recPerPage=1000 --pick=id,name,parent,type,assignedTo,status,deadline --format=json
```

If the resulting task has `parent: 0`, it is not a real child task. Recreate it with the JSON body pattern above.

## ZenTao Creation Rules

1. Create or update the execution with the selected product, project, branch, date range, and concise name.
2. Create the five fixed first-level stage tasks using `一、概念阶段` through `五、发布阶段`.
3. Ask whether to create subtasks before creating them.
4. If the user confirms subtasks, create the fixed default subtasks for stages one, two, four, and five.
5. For `三、开发阶段`, generate subtasks from requirement documents or feature lists when available.
6. If there is no requirement document or feature list, use the fallback development subtasks as-is.
7. Verify by listing tasks from the execution.
8. Summarize what was created, including execution ID, task IDs, parent IDs, owners, and deadlines.

## Known X86 Client Example

- Execution ID: `295`
- Execution name: `X86客户端6月迭代`
- Product: `U8融合通信平台客户端`
- Product ID: `1`
- Project: `U8-X86-版本更新（闪电）-凌云版本`
- Project ID: `7`
- Stage tasks:
  - `882` `一、概念阶段`
  - `884` `二、计划阶段`
  - `885` `三、开发阶段`
  - `886` `四、验证阶段`
  - `887` `五、发布阶段`
