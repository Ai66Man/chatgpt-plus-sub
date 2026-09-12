SOURCES={
 'plus':('OpenAI：ChatGPT Plus 说明','https://help.openai.com/en/articles/6950777-what-is-chatgpt-plus'),
 'pro':('OpenAI：Pro 档位与新购状态','https://help.openai.com/en/articles/9793128-about-chatgpt-pro-tiers'),
 'payment':('OpenAI：银行卡付款被拒','https://help.openai.com/en/articles/7232916-why-was-my-credit-card-declined'),
 'billing':('OpenAI：ChatGPT 与 API 账单','https://help.openai.com/en/articles/9039756-billing-settings-in-chatgpt-vs-platform'),
 'merchant':('GoPlus：套餐与服务说明','https://www.goplus.pro/'),
}
NOINDEX={'404','privacy','terms','chatgpt-pro-5x','chatgpt-pro-20x','claude-max-5x','claude-max-20x'}
# One page for each distinct reader problem; existing URLs remain available.
ARTICLES=[
 {'slug':'chatgpt-renewal','title':'ChatGPT Plus 怎么续费？自动扣款、手动续费与到期检查','desc':'分清 ChatGPT 网页订阅、App 订阅和第三方订单，了解 Plus 到期检查、重复扣款排查及续费前要确认的事项。','summary':'先查原来的订阅渠道，再决定怎样续费。还在自动续费的账号，不要另外重复下单。','sections':[
 ('先确认：你的订阅从哪里买的？','打开原来的购买邮件或付款记录，判断是 ChatGPT 官网、Apple / Google 应用商店，还是第三方订单。不同渠道的管理入口不同；仅凭支付工具名称，未必能判断实际订阅渠道。先记录账号邮箱、当前套餐和下一次扣款或到期日期。'),
 ('还没到期，要现在再买一个月吗？','先查看是否已开启自动续费。如果当前套餐会继续扣款，额外下单可能产生重复购买。第三方服务所说的“续费”也可能对应不同交付方式，应先问清是延长当前周期、到期后开通，还是替换套餐，不能默认剩余天数会叠加。'),
 ('自动扣款失败，先做什么？','查看原渠道的失败提示与订单状态。官方网页订阅检查账单资料和银行卡验证；应用商店订单回到原商店处理；第三方订单联系实际服务商。先确认有没有成功扣款，再决定是否重试。'),
 ('已经付款，会员却显示 Free？','先对照订单确认登录的是同一个账号和登录方式，再检查交易是已完成、处理中还是被撤销。保存订单号、时间、金额及页面提示，沿原购买渠道处理。还没核清前不要连续下单。'),
 ('续费前可以这样向客服确认','明确告知“当前套餐、购买渠道、到期日、是否自动续费”，再问“剩余时间是否保留、何时交付、失败怎样处理”。本网站不接收账号凭据；咨询时先提供订单与套餐信息即可。')], 'sources':['plus','billing'],'related':['chatgpt-plus','chatgpt-payment-failed','chatgpt-charged-not-upgraded'],'cta':'确认 Plus 续费方案'},
 {'slug':'chatgpt-payment-failed','title':'ChatGPT 充值付款失败怎么办？银行卡被拒与支付验证排查','desc':'ChatGPT Plus 付款失败、银行卡被拒或支付验证未完成时，按交易状态、卡片信息、银行验证与地区条件依次排查。','summary':'先确认是否扣款，再排查付款信息和银行验证。不要把所有失败都理解为“换个充值入口就能解决”。','sections':[
 ('第一步：区分未付款与已扣款','记录页面提示，并在银行或支付渠道查看这笔交易的状态。未完成付款、临时授权和已完成交易处理方式不同。如果已扣款却没有会员，先进入本站的到账异常指南，不要继续反复尝试付款。'),
 ('第二步：核对付款资料','OpenAI 建议检查卡号、有效期、CVC、账单地址及可用余额。按银行登记资料填写；不要为通过付款而编造地址。卡片资料正确但仍失败时，联系发卡行询问是否限制在线、跨境或周期性交易。'),
 ('第三步：完成银行身份验证','部分付款要求 3D Secure / SCA 验证。留意银行 App、短信或支付页面的验证提示，确认跳转未被拦截。验证码只应在可信银行或支付流程中使用，不应发给代充客服。'),
 ('第四步：检查地区与卡片适用条件','官方购买有支持地区和发卡地区要求。第三方收款方式并不改变产品本身的可用条件。若不满足适用条件，先查看官方规则，不要不断换卡或重复提交同一笔订单。'),
 ('排查之后仍失败，应该联系谁？','银行拦截找发卡行；官网订单问题找官方支持；应用商店订单找原商店；第三方订单找实际收款方。准备错误提示、交易时间和订单号，隐藏完整卡号与安全码后再沟通。')], 'sources':['payment'],'related':['chatgpt-charged-not-upgraded','buying-guide','chatgpt-plus'],'cta':'咨询可用购买方式'},
 {'slug':'chatgpt-charged-not-upgraded','title':'ChatGPT 扣款成功但没有 Plus？到账异常排查顺序','desc':'购买 ChatGPT Plus 后仍显示 Free，先检查登录账号、交易状态和原购买渠道，再准备订单记录联系对应支持方。','summary':'扣款成功与订阅已生效需要分别核对。先查账号、订单和购买渠道，再决定是否联系售后。','sections':[
 ('先核对登录的账号','对照收据中的账号信息，确认当前登录的是购买时使用的账号。邮箱密码登录、Google 登录或 Apple 登录可能涉及不同身份，不要只根据显示昵称判断。退出前先确认自己能重新登录。'),
 ('再核对订单是否真正完成','查看支付渠道中是已完成、待处理、授权中还是已退款。保留原始收据，不要把银行的临时授权误认为最终结算；具体交易状态应由支付方或服务商确认。'),
 ('按购买渠道分别处理','网页购买回到 ChatGPT 的订阅与账单页面；App 购买检查原应用商店账号和订单；第三方充值查看商家订单是否已交付。如果商家显示未完成，先让实际交付方核查，不要把等待处理的订单当作已到账。'),
 ('给售后提供一份能定位问题的记录','准备购买时间、金额、套餐、订单号，以及当前账号套餐页面的截图。遮挡完整付款资料和无关私人信息，不发送密码、验证码或会话令牌。这些凭据并不能替代订单定位。'),
 ('排查期间避免重复购买','重复下单会让订单与订阅状态更难对应。先处理原订单，明确是否交付、撤销或退款；若确实需要重新购买，再确认原交易不会继续扣款。')], 'sources':['plus','billing'],'related':['chatgpt-payment-failed','chatgpt-renewal','faq'],'cta':'前往服务商查询订单'},
 {'slug':'chatgpt-api-vs-plus','title':'GPT 充值是买 Plus 还是 API 余额？两种用途一次分清','desc':'ChatGPT Plus 会员与 OpenAI API 余额不是同一种充值。按聊天、Codex 编程或程序调用的用途，确认应购买的产品与账单。','summary':'在 ChatGPT 里聊天、读文件，关注会员订阅；让程序调用模型，关注 API 计费。购买一种，不会自动给另一种账户增加余额。','sections':[
 ('在网页或 App 中使用 ChatGPT','这类需求通常是在 ChatGPT 产品内使用功能。先查看账号提供的套餐选项，以及自己需要的功能和额度，再决定是否升级。本站展示的 Plus 购买入口面向订阅，不是 API 充值入口。'),
 ('在自己的程序中调用模型','如果使用 API Key 让脚本、插件或应用调用 OpenAI 模型，费用属于 API 平台。ChatGPT 和 API 使用独立账单，买了 Plus 不能用来抵扣 API 消费。也不要把 API Key 当成充值卡密交给服务商。'),
 ('使用 Codex 时，先看登录与计费方式','编程工具里可能出现不同的登录或用量选项。先核对当前工具实际使用的是订阅账号还是 API 凭据，再查看对应账单。不要仅凭“支持 Codex”四个字，就认为包含所有编程调用费用。'),
 ('下单前用一句话描述你的需求','例如“我要在 ChatGPT 网页里处理文档”，或“我要让自己的程序调用模型”。把用途说清楚，比单说“我要充 GPT”更能避免买错。不能确定时先咨询，不要先买再试。')], 'sources':['billing'],'related':['chatgpt-plus','choose-chatgpt','buying-guide'],'cta':'咨询适合自己的订阅'},
]
DETAILS={
 'chatgpt-plus':[
 ('ChatGPT Plus 充值多少钱？','官方 Plus 订阅为 20 美元/月，API 消费另计。本站的 165 元起是 GoPlus 的服务商参考报价，两者不是同一口径；实际成交价以小店为准。比较时还要确认周期、账号归属和售后范围。'),
 ('微信、支付宝开通 Plus 的步骤','先确认自己的账号可以正常使用、是否已有订阅；进入小店查看具体商品和库存；向服务商核对所需资料、交付方式与退款规则；付款后保留订单，最后在自己的账号中检查套餐状态。本站不直接收取充值信息。'),
 ('自助充值和人工咨询怎么选？','已经确认账号与套餐、且小店显示可购时，可以查看自助下单说明。现有订阅未到期、曾付款失败或不确定登录账号时，先咨询再付款，避免重复订单。'),
 ('买的是会员，不是无限额度','Plus 的可用模型、工具和使用上限可能变化。购买前确认自己需要的功能，不以“永久会员”或“无限调用”等说法判断实际权益。')],
 'claude-pro':[
 ('Claude 充值前，先确认 Pro 还是 Max','写作、读资料和阶段性编码，可先比较 Pro；如果工作中频繁遇到用量限制，再看 Max。本站列出的 Pro、Max 价格为服务商报价，最终权益和可用条件以产品官方与订单说明为准。'),
 ('Claude Pro 购买流程','先确认账号状态和当前订阅，再去小店查看套餐；有剩余订阅、升级需求或交付方式不清楚时，先联系服务商。确认后再下单，保留订单与实际开通结果。'),
 ('使用 Claude Code 要确认什么？','先核对当前使用的登录方式、所需套餐和用量规则。不要把更高档位理解为所有模型、所有任务无限使用。若经常触及限制，记录任务类型与发生频率，再决定是否升级。'),
 ('续费与售后如何处理？','提供当前套餐、到期日和原购买渠道，让服务商明确剩余时长如何处理。到账异常沿原订单查询，不通过重复购买解决。')],
 'grok-super':[
 ('Grok Super 订阅与购买入口','这里提供 Grok 套餐的购买导航，页面价格是服务商参考报价，不是 xAI 官方定价。购买前确认商品名称、订阅周期、目标账号以及当前可用权益。'),
 ('X 上的权益与 Grok 订阅不要混淆','不要仅因在 X 中能看到 Grok，就推断另一入口中的付费权益已开通。先核对实际使用的产品、登录账号和订阅页面，再选择对应商品；不确定时向服务商说明你从哪里使用 Grok。'),
 ('微信或支付宝购买前的检查','先查看小店实际支持的支付方式和库存。确认所需资料、交付时间与失败处理办法后再下单。本站不提供密码、验证码或会话信息提交表单。'),
 ('充值后怎样确认到账？','在对应账号的订阅页面检查套餐与有效期，对照订单内容核验。结果不符时保存收据和页面提示，联系实际交付方查询原订单。')],
}
RELATED={
 'index':['chatgpt-plus','chatgpt-pro','chatgpt-renewal','chatgpt-payment-failed','chatgpt-api-vs-plus','claude-pro','grok-super'],
 'chatgpt-plus':['chatgpt-renewal','chatgpt-payment-failed','chatgpt-charged-not-upgraded','choose-chatgpt'],
 'chatgpt-pro':['chatgpt-plus','choose-chatgpt','chatgpt-renewal','chatgpt-api-vs-plus'],
 'choose-chatgpt':['chatgpt-plus','chatgpt-pro','chatgpt-api-vs-plus'],
 'choose-claude':['claude-pro','claude-max-5x','claude-max-20x'],
 'claude-pro':['choose-claude','claude-max-5x','claude-max-20x','buying-guide'],
 'grok-super':['buying-guide','faq'],
 'buying-guide':['chatgpt-plus','chatgpt-payment-failed','chatgpt-api-vs-plus'],
}
