# 更新说明卡片风 (Release Note Card Style)

适用于：更新说明、版本发布、较上次发布、问题处理清单、缺陷修复公告、移动端 App 发布说明。

## 角色定义

产品发布说明编辑与信息图视觉架构师。擅长把冗长的问题单、缺陷列表和新增功能整理成可直接发公告的单页 HTML 卡片。

## 内容结构

默认采用“三段式发布说明”：

1. 顶部总览：产品名、主标题、较上次发布的摘要、关键统计。
2. 重点区：新增功能、问题优化，使用不等宽网格，新增功能作为视觉锚点。
3. 处理区：问题处理按影响路径归组，如会议稳定性、资源刷新、日程交互、兼容性。

当用户明确要求“不体现版本”时：

- 不显示具体版本号、构建号、发布日期和时间轴。
- 标题使用“更新说明（较上次发布）”或同义表达。
- 页脚只写整理口径和分类，不写版本范围。

## 视觉原则

- 主锚点是“本次更新内容数量”或“新增功能名称”，不要平均铺满。
- 用深色科技底、克制蓝绿强调和细线网格承载工程感。
- 避免大段原始问题清单堆叠，必须归并为模块。
- 问题单号可以放在末尾做追踪区，不要抢正文层级。

## 版式建议

```css
:root {
  --bg: #101116;
  --panel: #1f232b;
  --panel-deep: #171b22;
  --line: rgba(255, 255, 255, 0.09);
  --line-strong: rgba(122, 162, 247, 0.32);
  --text: #c0caf5;
  --muted: #8b95bf;
  --dim: #626d91;
  --blue: #7aa2f7;
  --green: #4ade80;
  --amber: #f6c177;
  --shadow: 0 24px 70px rgba(4, 10, 22, 0.42);
}

body {
  background:
    radial-gradient(circle at 12% 8%, rgba(122, 162, 247, 0.18), transparent 28%),
    radial-gradient(circle at 86% 16%, rgba(74, 222, 128, 0.10), transparent 30%),
    linear-gradient(135deg, #101116 0%, #151922 56%, #0f1218 100%);
  color: var(--text);
  font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", system-ui, sans-serif;
}

.page {
  width: min(1280px, 100%);
  margin: 0 auto;
  border: 1px solid var(--line);
  border-radius: 28px;
  background:
    linear-gradient(rgba(255, 255, 255, 0.035) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.035) 1px, transparent 1px),
    rgba(16, 17, 22, 0.84);
  background-size: 28px 28px, 28px 28px, auto;
  box-shadow: var(--shadow);
  overflow: hidden;
}

.hero {
  display: grid;
  grid-template-columns: 1.12fr 0.88fr;
  gap: 32px;
  padding: 42px 42px 26px;
}

.metric-board {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}

.metric.large {
  grid-column: 1 / -1;
  background: linear-gradient(135deg, rgba(122, 162, 247, 0.13), rgba(31, 35, 43, 0.78));
  border-color: var(--line-strong);
}

.update-grid {
  display: grid;
  grid-template-columns: 0.82fr 1.18fr;
  gap: 14px;
}

.problem-layout {
  display: grid;
  grid-template-columns: 1.08fr 0.92fr;
  gap: 14px;
}
```

## 文案整理规则

- `新增功能`：只放新能力，不混入修复项。
- `问题优化`：放体验、逻辑、显示状态、刷新准确性等改进项。
- `问题处理`：放明确缺陷、崩溃、异常跳转、兼容性问题。
- 如果原始材料包含多个历史版本，但用户要求“较上次发布”，优先抽取最新一次发布内容。
- 如果用户要求“给一个 md”，同步输出同结构 Markdown。

## 避坑

- 不要按版本做时间轴，除非用户明确要“历史版本汇总”。
- 不要把每个问题单都做成独立卡片。
- 不要在视觉上突出问题单号超过问题本身。
- 不要出现未替换的版本占位符。
