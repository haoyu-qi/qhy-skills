# qhy-draw 领域图谱

这个文件用于补齐 `qhy-draw` 在 AI / Agent / 技术系统场景中的默认认知。遇到这些主题时，不要只画通用方框图，要优先识别领域里的常见层次和关系。

## 1. RAG 系统

常见模块：

- 用户 / 问题
- Query Rewrite / 检索策略
- Retriever
- Vector Store / 文档库
- Reranker
- Context Builder
- LLM
- Answer / 引用来源

画法建议：

- 主线是“问题进入后如何检索、拼上下文、生成回答”
- 检索和生成分层
- 如果涉及更新知识库，单独画 ingest 支路

## 2. Agent 系统

常见层次：

- 输入层：用户、触发器、任务
- Agent 核心：Planner、Reasoner、LLM、Orchestrator
- 工具层：Search、Browser、Code、API、DB
- Memory 层：短期记忆、长期记忆、任务状态
- 输出层：回复、执行结果、副作用

画法建议：

- Agent 核心必须是中心层，不要和工具并排成“平铺功能卡片”
- 有循环时明确画出反馈回路
- 工具调用用另一类箭头，与主数据流区分

## 3. Memory 系统

常见模块：

- Working Memory
- Short-term Memory
- Episodic Memory
- Semantic Memory
- Procedural Memory
- Vector Store / Graph DB / KV Store
- Memory Manager / Consolidation

画法建议：

- 读路径和写路径分开
- 存储层要有层次，不要都叫“数据库”
- 如果是 Mem0 / MemGPT 风格，强调 manager 和 retrieval

## 4. Multi-Agent 协作

常见模块：

- User / Mission
- Coordinator / Supervisor
- Specialist Agents
- Shared Memory / Shared Context
- Synthesizer / Reviewer
- Final Output

画法建议：

- 先画控制链，再画协作链
- Specialist Agents 可以并排，但必须看出谁调度谁
- 有共享上下文时单独做中间层

## 5. 微服务 / 云基础设施

常见层次：

- Client / Edge
- Gateway / Auth / Policy
- Services
- Queue / Event Bus
- Storage
- Observability

画法建议：

- 优先按层画，不要按“服务名称清单”平铺
- 数据存储与计算服务区分形状
- 异步链路和同步调用用不同箭头

## 6. API / Tool Call 流程

常见模块：

- User / Application
- SDK / Gateway
- Model Runtime
- Tool Selector
- Tool Execution
- Result Parser
- Final Response

画法建议：

- 时序明确时画时序图
- 逻辑闭环更重要时画流程图
- Tool Call 返回链必须可见

## 领域图通用提醒

- 不要把“AI”“Agent”“Memory”“Tool”都画成一样的盒子
- 同一个图里，至少要让用户一眼看出核心控制层、存储层、外部接口层
- 领域名词再多，也不能牺牲主路径可读性
