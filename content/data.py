# -*- coding: utf-8 -*-
"""Site-wide data for the comparison site. Prices are official list prices in USD
unless stated otherwise; CNY retail prices are intentionally not maintained here."""

SITE_NAME = "AI 订阅开通服务"
BASE = "https://ai66man.github.io/chatgpt-plus-sub/"
GA_ID = "G-76M2YEVGPJ"
CHECKED = "2026-09-15"
REPO = "https://github.com/Ai66Man/chatgpt-plus-sub"

# GoPlus destinations. Every outbound link gets UTM parameters at render time.
SHOP = "https://fe.dtyuedan.cn/shop/panghu"  # 小店自助下单入口
WECHAT = "https://www.goplus.pro/#wechat"    # 人工咨询入口

GOPLUS = {
    "home": "https://www.goplus.pro/",
    "wechat": "https://www.goplus.pro/#wechat",
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


# --------------------------------------------------------------------- 商品
# 人民币报价同步自 GoPlus 商品页（核对日见 CHECKED）。self 档走小店自助下单，
# manual 档需要人工确认账号状态后交付，入口指向 GoPlus 对应产品页。
PRODUCTS = [
    dict(slug="chatgpt-plus", group="chatgpt", brand="gpt", name="ChatGPT Plus",
         eyebrow="多数用户首选", badge="推荐", price="165", unit="元起",
         official="官方 Plus $20/月", mode="self", cta="前往小店下单",
         desc="适合日常写作、学习、办公和轻量编程，支持高级模型、文件分析、联网搜索和 Codex。",
         audience="普通用户、内容创作者、学生、轻量开发者",
         features=["支持最新模型、文件分析与联网搜索",
                   "可使用 Codex、Projects 与自定义 GPTs",
                   "无需海外信用卡，不需要提供账号密码",
                   "小店自助下单，也可先微信咨询"]),
    dict(slug="chatgpt-pro-5x", group="chatgpt", brand="gpt", name="ChatGPT Pro 5X",
         eyebrow="中重度使用", badge="", price="850", unit="/月",
         official="约 5 倍 Plus 额度", mode="manual", cta="查看档位详情", goplus="chatgpt_pro",
         desc="适合阶段性项目和中重度使用，包含 Plus 权益，支持 Pro 模型、Codex 与深度研究额度。",
         audience="开发者、研究生、数据分析师等中度使用者",
         features=["比 Plus 更高的模型与使用额度",
                   "适合中高强度使用 Codex 工作与研究",
                   "需先确认账号状态与套餐",
                   "由人工跟进开通过程与异常处理"]),
    dict(slug="chatgpt-pro-20x", group="chatgpt", brand="gpt", name="ChatGPT Pro 20X",
         eyebrow="高强度生产力", badge="顶配", price="1500", unit="/月",
         official="约 20 倍 Plus 额度", mode="manual", cta="查看档位详情", goplus="chatgpt_pro",
         desc="适合高频生产力和团队任务，提供更高的 Pro、Codex 与深度研究额度。",
         audience="高频开发、科研、数据分析与商业内容团队",
         features=["更高优先级与更大使用额度",
                   "适合长时间 Codex、多任务研究与复杂文档",
                   "需人工确认后再开通",
                   "售后由人工跟进，异常可快速处理"]),
    dict(slug="claude-pro", group="claude", brand="claude", name="Claude Pro",
         eyebrow="长文档与写作", badge="", price="185", unit="/月",
         official="官方 Pro $20/月", mode="self", cta="前往小店下单",
         desc="适合研究、写代码、资料整理与知识工作，支持 Claude Code。",
         audience="内容创作者、研究人员、产品经理、技术团队",
         features=["支持 Claude Code、Projects 与最新模型",
                   "适合编码、内容创作、分析与自动化",
                   "小店自助下单，也可先微信确认",
                   "到账与售后通过微信沟通处理"]),
    dict(slug="claude-max-5x", group="claude", brand="claude", name="Claude Max 5X",
         eyebrow="重度 Claude Code", badge="", price="900", unit="/月",
         official="约 5 倍 Pro 用量", mode="manual", cta="查看档位详情", goplus="claude_max_5x",
         desc="适合 Pro 额度经常不够、每天长时间使用 Claude Code 的开发者，用量与输出上限更高。",
         audience="重度 Claude Code 用户、开发者、高频写作与研究",
         features=["约为 Claude Pro 5 倍的使用量",
                   "适合每天长时间使用 Claude Code",
                   "需先确认账号状态与套餐",
                   "由人工跟进开通过程与异常处理"]),
    dict(slug="claude-max-20x", group="claude", brand="claude", name="Claude Max 20X",
         eyebrow="极限用量", badge="", price="1700", unit="/月",
         official="约 20 倍 Pro 用量", mode="manual", cta="查看档位详情", goplus="claude_max_20x",
         desc="面向全天候高强度使用 Claude Code、多任务并行的用户，提供最高档位的用量与输出上限。",
         audience="全天候 Claude Code、科研、团队与商业生产力场景",
         features=["约为 Claude Pro 20 倍的使用量",
                   "适合全天候 Claude Code 与多任务并行",
                   "需人工确认后再开通",
                   "售后由人工跟进，异常可快速处理"]),
    dict(slug="grok-super", group="grok", brand="grok", name="Grok Super",
         eyebrow="热点追踪", badge="现货", price="230", unit="/月",
         official="官方 $30/月", mode="self", cta="前往小店下单",
         desc="更快回复、更长对话与更多用量，支持 Grok Build、文件上传与 720p 视频。",
         audience="X 用户、信息研究者、AI 工具重度用户",
         features=["支持 Grok Build、文件上传与 720p 视频",
                   "适合实时信息、热点事件与海外内容检索",
                   "当前现货可购，支持小店自助下单",
                   "下单后按页面引导提交 UserID 完成开通"]),
]

PRODUCT_GROUPS = [
    ("chatgpt", "ChatGPT 套餐", "日常写作办公选 Plus，重度 Codex 与研究上 Pro。", "gpt", "¥165 起"),
    ("claude", "Claude 套餐", "长文档、细致写作与 Claude Code 工作流。", "claude", "¥185 起"),
    ("grok", "Grok 套餐", "关注实时话题、海外信息与 X 生态内容。", "grok", "¥230/月"),
]

TRUST = [("无需海外卡", "微信 / 支付宝直接付"), ("开在自己账号", "不是共享号、不是成品号"), ("不要密码", "按产品提交指定信息即可")]

STEPS = [
    ("选好产品与档位", "按使用强度选档，先确认当前账号与已有订阅状态。"),
    ("自助下单或微信咨询", "基础档前往小店直接下单；Pro / Max 高配档先微信确认。"),
    ("按订单说明完成开通", "核对交付方式与所需信息，保存订单号与沟通记录。"),
    ("检查到账与有效期", "在官方产品中确认订阅状态与到期时间，有问题联系客服。"),
]

CHANNEL_COMPARE = [
    ("购买入口", "小店自助下单 / 微信人工", "官方网站或官方 App", "个人卖家、聊天群"),
    ("付款方式", "微信、支付宝", "境外银行卡等官方支持方式", "微信、支付宝"),
    ("账号归属", "开在你自己的账号上", "你自己的账号", "常见成品号或共享号"),
    ("需要提供什么", "按产品不同：Session / Organization ID / UserID，不要密码", "无", "可能要密码"),
    ("售后", "有固定客服入口与订单记录", "官方支持渠道", "多为个人，难追溯"),
    ("适合谁", "没有境外卡、不想折腾的国内用户", "有境外卡且符合地区条件", "只图便宜、能承担风险"),
]


# 各产品开通时需要提供什么——这是服务边界，也是安全边界。
DELIVERY_INFO = [
    ("ChatGPT", "Session",
     "在已登录状态下获取。它具有账号访问能力，开通完成后退出重新登录即可重置。",
     "不需要密码、不需要短信验证码"),
    ("Claude", "Organization ID",
     "在 Settings → Account 里可以查到，本身不能用于登录你的账号。",
     "不需要登录你的账号，避免触发风控"),
    ("Grok", "UserID",
     "账号标识，不是登录凭据，可在账号会话信息里查到。",
     "不需要密码，只要一个 ID"),
]
