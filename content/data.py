# -*- coding: utf-8 -*-
"""Site-wide data for the comparison site. Prices are official list prices in USD
unless stated otherwise; CNY retail prices are intentionally not maintained here."""

SITE_NAME = "AI 订阅比价指南"
BASE = "https://ai66man.github.io/chatgpt-plus-sub/"
GA_ID = "G-76M2YEVGPJ"
CHECKED = "2026-09-15"
REPO = "https://github.com/Ai66Man/chatgpt-plus-sub"

# GoPlus destinations. Every outbound link gets UTM parameters at render time.
GOPLUS = {
    "home": "https://www.goplus.pro/",
    "chatgpt_plus": "https://www.goplus.pro/chatgpt-plus-recharge",
    "chatgpt_pro": "https://www.goplus.pro/chatgpt-pro-recharge",
    "claude": "https://www.goplus.pro/claude",
    "claude_max_5x": "https://www.goplus.pro/claude-max-5x-recharge",
    "claude_max_20x": "https://www.goplus.pro/claude-max-20x-recharge",
    "grok": "https://www.goplus.pro/grok",
    "chatgpt_choose": "https://www.goplus.pro/articles/chatgpt-plus-vs-pro-how-to-choose",
    "claude_choose": "https://www.goplus.pro/articles/claude-pro-vs-max-how-to-choose",
    "payment_declined": "https://www.goplus.pro/articles/chatgpt-payment-card-declined",
    "not_showing": "https://www.goplus.pro/articles/chatgpt-plus-not-showing-after-recharge",
    "renewal_failed": "https://www.goplus.pro/articles/chatgpt-renewal-failed-plus-disappeared",
}

SOURCES = {
    "openai_pricing": ("OpenAI：ChatGPT 定价页", "https://chatgpt.com/pricing"),
    "openai_plus": ("OpenAI：ChatGPT Plus 说明", "https://help.openai.com/en/articles/6950777-what-is-chatgpt-plus"),
    "openai_billing": ("OpenAI：ChatGPT 与 API 账单区别", "https://help.openai.com/en/articles/9039756-billing-settings-in-chatgpt-vs-platform"),
    "anthropic_pricing": ("Anthropic：Claude 定价页", "https://www.anthropic.com/pricing"),
    "claude_code": ("Anthropic：Claude Code 文档", "https://docs.anthropic.com/en/docs/claude-code/overview"),
    "google_ai": ("Google：Google AI 订阅方案", "https://one.google.com/about/google-ai-plans/"),
    "xai": ("xAI：Grok 定价", "https://x.ai/grok"),
    "cursor": ("Cursor：定价页", "https://cursor.com/pricing"),
    "copilot": ("GitHub：Copilot 定价", "https://github.com/features/copilot/plans"),
    "zhipu": ("智谱：GLM Coding Plan", "https://bigmodel.cn/"),
    "merchant": ("GoPlus：国内开通与报价", "https://www.goplus.pro/"),
}

# 全档位对比。price 为官方美元标价，注明计费单位；国内开通价不在本站维护。
PLANS = [
    # (品牌, 档位, 官方美元价, 计费单位, 主要额度/权益, 适合谁, goplus key)
    ("ChatGPT", "Free", "0", "/月", "基础模型，日常用量有限", "只是偶尔试用", None),
    ("ChatGPT", "Go", "8", "/月", "比免费版更长的对话与更高基础用量", "预算有限、轻度使用", None),
    ("ChatGPT", "Plus", "20", "/月", "主力模型、文件分析、图像、Codex 编程辅助", "绝大多数个人用户的默认选择", "chatgpt_plus"),
    ("ChatGPT", "Pro（5×）", "100", "/月", "官方说明约为 Plus 的 5 倍用量", "每周多次撞上限的重度用户", "chatgpt_pro"),
    ("ChatGPT", "Pro（20×）", "200", "/月", "官方说明约为 Plus 的 20 倍用量，含更多专属能力", "全职高强度使用", "chatgpt_pro"),
    ("Claude", "Free", "0", "/月", "滚动额度，适合轻量问答", "试用", None),
    ("Claude", "Pro", "20", "/月", "含 Claude Code、Projects、更高用量；年付约 $17/月", "写作、长文档、入门编程", "claude"),
    ("Claude", "Max 5×", "100", "/月", "官方说明约为 Pro 的 5 倍用量", "高频 Claude Code 用户", "claude_max_5x"),
    ("Claude", "Max 20×", "200", "/月", "官方说明约为 Pro 的 20 倍用量", "全天候编码与研究", "claude_max_20x"),
    ("Gemini", "Free", "0", "/月", "基础模型，日用量受限", "试用", None),
    ("Gemini", "Google AI Plus", "4.99", "/月", "入门付费档，含额外存储", "价格敏感、轻度使用", None),
    ("Gemini", "Google AI Pro", "19.99", "/月", "主力模型与更高额度，含 2TB 级存储", "已在用 Google 生态的人", None),
    ("Gemini", "Google AI Ultra", "99.99", "/月", "最高消费级额度与专属功能", "重度使用 + 需要大存储", None),
    ("Grok", "Free", "0", "/月", "按时间窗口限流", "试用", None),
    ("Grok", "X Premium", "8", "/月", "基础 Grok 访问 + X 会员权益", "X 重度用户", None),
    ("Grok", "SuperGrok", "30", "/月", "标准独立订阅，含 DeepSearch 等", "关注实时信息与 X 生态", "grok"),
    ("Grok", "SuperGrok Heavy", "300", "/月", "多智能体与最高额度", "极少数重度场景", "grok"),
]

# 开发者/编程向订阅
CODING_PLANS = [
    ("Claude Pro", "$20/月", "Claude Code 包含在订阅内，按用量窗口限流", "个人开发者最常见的起点", "claude"),
    ("Claude Max 5×", "$100/月", "约 Pro 的 5 倍用量", "每天数小时 Claude Code", "claude_max_5x"),
    ("Claude Max 20×", "$200/月", "约 Pro 的 20 倍用量", "全职重度编码", "claude_max_20x"),
    ("ChatGPT Plus", "$20/月", "含 Codex 编程辅助，额度与对话共享", "同时需要写作与编程", "chatgpt_plus"),
    ("ChatGPT Pro（5×/20×）", "$100 / $200 每月", "Codex 额度随档位提升", "把 Codex 当主力的用户", "chatgpt_pro"),
    ("Cursor Pro", "$20/月", "编辑器内多模型，额度按请求计", "习惯在 IDE 内完成全部工作", None),
    ("Cursor Ultra", "约 $200/月", "官方以倍数描述，金额会调整", "重度 IDE 内代理编程", None),
    ("GitHub Copilot Pro", "$10/月", "补全为主，代理能力按档位区分", "主要需要补全而非代理", None),
]

# 国内 Coding Plan（人民币，官方标价；活动价常低于此）
DOMESTIC_CODING = [
    ("智谱 GLM Coding Plan", "Lite ¥118 / Pro ¥538 / Max ¥1078 每月", "按积分计费：Lite 每 5 小时 2,000 积分、每周 10,000 积分", "国内网络直连，价格低"),
    ("火山方舟 Coding Plan", "¥40 起 / 月", "官方宣传为数倍 Claude Pro 用量", "字节生态、国内直连"),
    ("阿里云百炼 Coding Plan", "¥40 起 / 月", "Lite 档每 5 小时 1,200 次请求、每月上限 18,000 次", "已在用阿里云的团队"),
    ("Kimi 编程套餐", "¥49 起 / 月", "按档位提供专属额度，按周更新", "长上下文任务"),
    ("MiniMax 编程套餐", "¥29 起 / 月", "Starter 档每 5 小时 40 prompts", "预算最低的入门选择"),
]

USE_CASES = [
    ("写作与内容", "长文打磨、风格一致性、资料整理", "claude-vs-chatgpt"),
    ("编程开发", "代理式编码、仓库级修改、终端工作流", "claude-code-vs-codex"),
    ("学生与学习", "论文资料、解题讲解、语言学习", "ai-subscription-price-compare"),
    ("实时信息", "热点追踪、社交平台内容、检索", "ai-subscription-price-compare"),
    ("预算优先", "国内直连、按量付费、低价档位", "coding-plan-compare"),
]
