# 来源、能力映射与适配

## 来源与署名

改编自 **chrislitality-svg** 的 [wangziru-analysis-skill](https://github.com/chrislitality-svg/wangziru-analysis-skill)，读取提交 `e696d7d564e3c9db1d55285e4b7bcba173008ba6`，获取日期 2026-10-11。

上游为 **CC BY-NC 4.0**，完整 [LICENSE](../LICENSE) 随技能保留，许可说明见 [CC 官方页面](https://creativecommons.org/licenses/by-nc/4.0/)。上游材料及本技能改编保留署名和非商业条款，无担保；仓库 MIT 总标识不覆盖它们。不声称上游作者或王自如本人参与、认可或代言。

本次修改：重写入口和手册，把强制修辞、词频和分数阈值改成按用途判断；合入 QHY 风格、保真和编辑范围；加入文章与业务分析；重新实现候选扫描与本地描述性指标工具。不含视频全文语料、声线、肖像或照搬金句。

## 能力映射

| 上游材料/能力 | 本技能位置 | 适配 |
| --- | --- | --- |
| SKILL 四模式 A/B/C/D | SKILL A/B/C/D | 拆解、成稿、诊断、保真清理，完成当前请求 |
| 定义、换尺、排除、框架、比喻、收口 | analysis-blueprint.md | 准确定义、可验证尺度、公平比较、有边界结论 |
| logic-表达逻辑 | analysis-blueprint.md | 四骨架、关键依据、案例位置、逻辑链和首尾 |
| blueprint-template | analysis-blueprint.md / writing-and-delivery.md | 可裁剪蓝图、形态路由、真实开头 |
| syntax-长句逻辑 | writing-and-delivery.md | 因果、条件、让步与回指，长句和气口分查 |
| playbook-句法手册 | writing-and-delivery.md / examples-and-practice.md | 功能块、标注、录制剪辑、纠错和训练 |
| quotes-金句库 | writing-and-delivery.md | 句子功能和节奏，不携带原句供照搬 |
| samples-标杆拆解 | analysis-blueprint.md / examples-and-practice.md | 个人决策链、同尺比较和自创演示 |
| de-ai-去AI味 | qhy-style.md / review-and-rewrite.md | 定位式编辑、范围控制和保真复检 |
| ai_flavor_check.py | scripts/text_review.py | 重写为候选位置和统计，无人味分数 |
| strategy-内容战略与局限 | strategy-and-benchmarking.md | 目标、系列、双轨、修正、利益关系和局限 |
| data-量化复盘 | strategy-and-benchmarking.md | 分开描述、线索与因果，不推广单账号经验 |
| bili_fingerprint.py | strategy-and-benchmarking.md / scripts/content_metrics.py | 保留复盘与复核能力；现有工具采集，本地计算，去掉买量断言及跨账号兜底基准 |

## QHY 依据

本次读取的已有技能：

- `qhy-humanizer-zh/SKILL.md` 与 `references/chinese-editing-rules.md`：最小编辑、保真和中文规则的保留条件。
- `qhy-word/SKILL.md` 与 `references/writing-standards.md`：直接清楚、结论靠前、内容可流转、行动明确。
- `qhy-card/references/editorial-thesis.md`：主命题、路线、优先级和取舍、原话与提炼分清；未导入视觉布局约束。
- `arming-thought/SKILL.md`：事实先于判断，验证后才声称完成。

上述规则已合入，运行无需另装这些技能。未取得可用记忆结果，不把未确认的习惯归给用户。用户提供样文后以真实文本调整，不搜索无关私人文件。

## 适配边界

不强制争议立场、四字定义、多个排除对象、绝对化重锤、固定框架数、重复比喻、12 字金句、自嘲笑场、词频配额、禁标点、AI 味分低于 20，或等待蓝图批准才写稿。这些规则与任务或用户风格不一致时不强加，保留其分析功能。

上游称基于 71 个视频和约 50 小时机器转写。本次读取了公开技能、参考手册和两个脚本，未获得原始语料，不宣称独立验证统计或效果。其量化文件说明部分相关线索未过多重校正，异常指纹不证明投流；不能作为用户达标标准。

本地脚本测试证明计算和定位行为，不证明模型对所有选题都会作出正确判断。
