---
name: qhy-mail
description: |
  qhy 系列邮件助理。用于起草、润色、回复、转发和发送邮件，默认将邮件正文生成 qhy-card 风格的 HTML 卡片，并通过本地 mail-skill CLI 处理邮箱发送。

  强制规则：
  - 所有发送、回复、转发前必须先给用户人工确认。
  - 新邮件正文默认使用 qhy-card HTML 卡片。
  - 复用既有 mail-skill 配置与账号，不复制邮箱密钥或邮件数据。

  触发场景：
  - 发邮件、写邮件、起草邮件、回复邮件、转发邮件
  - 会议通知、评审通知、周报/月报邮件、发布通知、对外沟通邮件
  - 用户明确提到 qhy-mail、邮件卡片、HTML 邮件
---

# qhy-mail

qhy-mail 是面向中文业务沟通的邮件技能。它优先把邮件做成清晰、可扫读、审美稳定的 HTML 卡片，而不是普通大段文本；但实际发送必须经过用户手动确认。

## 固定原则

1. 永远不要自动发送邮件。
2. 任何 `send`、`reply`、`forward`、AI 自动回复发送动作前，必须先展示发送确认清单并等待用户明确回复“发送 / 确认发送 / 同意发送”。
3. 新建外发邮件默认使用 qhy-card 生成 HTML 正文，并用邮件 CLI 的 `--html-body` 发送。
4. 始终保留一份纯文本正文草稿，便于用户审阅，也可作为邮件客户端降级内容。
5. 不复制、输出或暴露邮箱密钥、授权码、SMTP 密码、邮件数据库内容。

## 工具路径

复用现有 mail-skill 安装：

- 技能目录：`/Users/qijingchun/.codex/skills/mail-skill`
- CLI：`/Users/qijingchun/.codex/skills/mail-skill/scripts/mail_cli.py`
- Python：`/Users/qijingchun/.codex/skills/mail-skill/.venv/bin/python`

发送命令形态：

```bash
/Users/qijingchun/.codex/skills/mail-skill/.venv/bin/python \
  /Users/qijingchun/.codex/skills/mail-skill/scripts/mail_cli.py send \
  --to recipient@example.com \
  --subject "邮件主题" \
  --body "纯文本正文" \
  --html-body "<!doctype html>..."
```

## qhy-card 正文生成

起草新邮件时，先判断邮件类型，再使用 `qhy-card`：

- 会议通知、发布通知、版本更新、评审邀请：优先 `qhy-card -i` 信息图。
- 周报、月报、进展同步：优先 `qhy-card -r` 周报板。
- 流程说明、方案说明、问题复盘：优先 `qhy-card -w` 白板图。
- 活动邀请、正式公告、对外宣传：优先 `qhy-card -p` 海报页。

使用 qhy-card 时必须读取 `/Users/qijingchun/.codex/skills/qhy-card/SKILL.md`，并按其要求继续读取相关 references 与模板。邮件 HTML 必须适配邮件客户端：

- CSS 内联或放在 `<style>` 内，不依赖外部 CSS、JS、远程字体。
- 宽度建议 680-760px，移动端可读。
- 避免复杂动画、脚本、悬浮交互和远程资源。
- 关键信息前置：收件人看到首屏就能知道时间、事项、动作和截止时间。

## 发送确认清单

发送前必须展示：

- 发件账号
- 收件人
- 抄送 / 密送
- 主题
- 正文预览：先给纯文本摘要，再说明已生成 HTML 卡片
- 附件
- 是否包含链接、会议号、截止时间等关键字段

只有用户明确确认后，才能调用 CLI 发送。用户只说“改一下”“再看看”“可以吗”都不算发送确认。

## 工作流

1. 收集邮件目的、对象、关键事实、语气和附件。
2. 如涉及人员邮箱，优先从用户提供的信息或本地邮件历史中确认；不确定时标记待确认，不猜同名联系人。
3. 生成纯文本正文草稿。
4. 调用 qhy-card 思路生成 HTML 卡片正文。
5. 展示确认清单，等待用户明确确认。
6. 确认后使用 mail CLI 发送，并把发送结果简要反馈给用户。

## 常见邮件语气

- 内部评审/会议通知：正式、清楚、动作导向。
- 跨部门协作：礼貌、边界清楚、明确需要对方做什么。
- 对外客户邮件：稳重、少术语、少内部缩写。
- 领导汇报：先结论，再背景，再行动。

## 失败处理

- SMTP/网络/认证失败：说明没有发送成功，保留草稿并给出错误摘要。
- 收件人缺失或疑似同名：停止发送，请用户补充或确认。
- HTML 生成不适合邮件客户端：退回更简单的 HTML 表格/卡片结构。
