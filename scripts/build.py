from pathlib import Path
from html import escape
import json, shutil, re
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'docs'; OUT.mkdir(exist_ok=True)
BASE='https://ai66man.github.io/chatgpt-plus-sub/'
SHOP='https://fe.dtyuedan.cn/shop/panghu'
CONTACT='https://www.goplus.pro/#wechat'
import sys
sys.path.insert(0,str(ROOT/'content'))
from catalog import products, faqs, guides
from search_content import ARTICLES, DETAILS, RELATED, SOURCES, NOINDEX

PAGE_META={
 'index':('GPT 充值指南：ChatGPT Plus 开通、Pro 订阅与续费','了解 GPT 充值的套餐价格、微信支付宝购买入口与开通步骤，解决 ChatGPT Plus 续费、付款失败和到账异常，并比较 Claude、Grok 订阅。'),
 'chatgpt-plus':('ChatGPT Plus 充值：价格、微信支付宝购买与开通步骤','ChatGPT Plus 怎么充值？比较官方月费与服务商报价，查看微信支付宝购买入口、自助开通流程、续费注意事项和到账检查。'),
 'claude-pro':('Claude 充值指南：Pro 购买、Max 选择与续费说明','了解 Claude Pro 充值入口、服务商报价、Max 档位比较和 Claude Code 使用前的确认事项，查看购买、续费与售后流程。'),
 'grok-super':('Grok Super 充值指南：订阅购买、支付与到账检查','了解 Grok Super 订阅购买入口与服务商报价，分清产品与账号，查看微信支付宝付款前确认事项及到账检查步骤。'),
 'guides':('GPT 充值教程与问题排查：开通、续费、付款失败','按需求查找 GPT 充值教程：ChatGPT Plus 开通、Pro 选择、续费、付款失败、扣款未到账，以及 Claude 与 Grok 购买指南。'),
 'faq':('GPT 充值常见问题：价格、支付、续费和售后','解答 ChatGPT Plus 充值价格、微信支付宝付款、Pro 档位、续费与到账问题，了解 Claude、Grok 订阅和服务商售后。'),
 'chatgpt-pro':('ChatGPT Pro 充值：5X / 20X 价格、区别与开通状态','比较 ChatGPT Pro 5X 与 20X 的参考报价和适用场景，了解 20X 新购暂停、已有订阅续费及升级前需要确认的事项。'),
}
for item in ARTICLES:
 PAGE_META[item['slug']]=(item['title'],item['desc'])
 RELATED[item['slug']]=item['related']
LABELS={p['slug']:p['name']+' 充值' for p in products}
LABELS.update({g[0]:g[1] for g in guides})
LABELS.update({k:v[0] for k,v in PAGE_META.items()})
for i,(q,a) in enumerate(faqs):
 if q.startswith('ChatGPT Plus、Pro'):
  faqs[i]=(q,a+' 2026-09-13 核对：Pro 20X 新购与升级暂时暂停，已有订阅续费不受此次暂停影响；详情见 Pro 充值页。')
for p in products:
 if p['slug']=='chatgpt-pro-20x':
  p.update(tag='新购 / 升级暂停',mode='查看当前状态',desc='OpenAI 已暂停 Pro 20X 新购与升级。已有订阅续费不受此次暂停影响；先核对账号状态。',features=['新购与升级自 9 月 10 日起暂停','已有订阅可按原规则续费','取消后可能无法重新开通','先阅读官方当前订阅说明'])

def source_block(keys):
 return '<aside class="sources"><strong>资料来源</strong><ul>'+''.join(f'<li><a href="{SOURCES[k][1]}">{SOURCES[k][0]}</a></li>' for k in keys)+'</ul><small>核对日期：2026-09-13。价格、功能与服务政策可能调整。</small></aside>'
def related_block(slug):
 links=RELATED.get(slug, ['chatgpt-plus','chatgpt-pro','claude-pro','grok-super','guides'])
 return '<aside class="related"><h2>继续了解</h2><div>'+''.join(f'<a href="{x}.html">{escape(LABELS.get(x,x))} →</a>' for x in links if x!=slug)+'</div></aside>'
def schema_block(slug,title,desc):
 url=BASE+('' if slug=='index' else slug+'.html')
 data=[{'@context':'https://schema.org','@type':'WebSite','@id':BASE+'#website','url':BASE,'name':'AI Plus','inLanguage':'zh-CN'}, {'@context':'https://schema.org','@type':'WebPage','@id':url+'#webpage','url':url,'name':title,'description':desc,'isPartOf':{'@id':BASE+'#website'},'inLanguage':'zh-CN'}]
 if slug!='index':
  data.append({'@context':'https://schema.org','@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'首页','item':BASE},{'@type':'ListItem','position':2,'name':title,'item':url}]})
 if slug in {a['slug'] for a in ARTICLES}|{g[0] for g in guides}:
  data.append({'@context':'https://schema.org','@type':'Article','headline':title,'description':desc,'mainEntityOfPage':url,'author':{'@type':'Organization','name':'AI Plus','url':BASE+'about.html'},'publisher':{'@type':'Organization','name':'AI Plus','url':BASE+'about.html'}})
 return '<script type="application/ld+json">'+json.dumps(data,ensure_ascii=False).replace('<','\u003c')+'</script>'

def link(name):return name+'.html'
def logo(brand):return f'<img src="assets/{brand}.{"png" if brand=="gpt" else "svg"}" width="30" height="30" alt="{brand} 标志">'
def btn(text,url,secondary=False):return f'<a class="button {"secondary" if secondary else ""}" href="{url}">{text}<span aria-hidden="true">↗</span></a>'
def faq(items):return '<div class="faq-list">'+''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in items)+'</div>'
def heading(eyebrow,title,sub):return f'<div class="section-head"><span class="eyebrow">{eyebrow}</span><h2>{title}</h2><p>{sub}</p></div>'
def product_card(p):
 return f'''<article class="product {p['group']}"><div class="card-top"><span class="tag">{p['tag']}</span>{logo(p['brand'])}</div><h3>{p['name']}</h3><div class="price"><small>¥</small>{p['price']}<small>{p['unit']}</small></div><p class="price-note">参考服务商报价 · 以实际下单为准</p><p class="product-desc">{p['desc']}</p><div class="audience"><small>适合人群</small>{p['audience']}</div><ul class="checks">{''.join('<li>'+x+'</li>' for x in p['features'])}</ul><a class="detail-link" href="{link(p['slug'])}">{p['name']} 充值详情 <span>→</span></a><div class="card-actions">{btn(p['mode'],'chatgpt-pro.html' if p['slug']=='chatgpt-pro-20x' else SHOP if p['mode']=='自助充值' else CONTACT)}<a href="{CONTACT}">微信咨询</a></div></article>'''
def contact():return f'''<section class="contact-section" id="contact"><div class="container contact-inner"><div><span class="eyebrow">LET’S GET STARTED</span><h2>选好了，就让 AI 开始帮忙。</h2><p>还有疑问？先确认账号、套餐与售后，再决定下单。</p><div class="actions">{btn('前往小店购买',SHOP)}{btn('联系微信客服',CONTACT,True)}</div><small>购买与咨询将前往 GoPlus 服务商页面。</small></div><div class="contact-note"><span class="big-plus">＋</span><strong>你的账号，你的工作流。</strong><p>ChatGPT · Claude · Grok<br>找到适合自己的 AI 订阅。</p></div></div></section>'''
def page(title,desc,body,slug='index'):
 canonical=BASE+(link(slug) if slug!='index' else '')
 nav=[('GPT 充值','index.html'),('Plus','chatgpt-plus.html'),('Pro','chatgpt-pro.html'),('Claude','claude-pro.html'),('Grok','grok-super.html'),('充值教程','guides.html')]
 return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">{schema_block(slug,title,desc)}<meta name="robots" content="{'noindex, follow' if slug in NOINDEX else 'index, follow, max-image-preview:large'}"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{escape(title)} | AI Plus</title><meta name="description" content="{escape(desc)}"><meta name="theme-color" content="#28766d"><link rel="canonical" href="{canonical}"><meta property="og:title" content="{escape(title)}"><meta property="og:description" content="{escape(desc)}"><meta property="og:type" content="website"><meta property="og:url" content="{canonical}"><link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="assets/style.css"><script src="assets/app.js" defer></script></head><body><a class="skip-link" href="#main">跳到正文</a><header><div class="container header-inner"><a class="brand" href="index.html" aria-label="AI Plus 首页"><span class="brand-icon">A<span>＋</span></span><span><strong>AI Plus</strong><small>AI 订阅服务</small></span></a><nav id="navigation" aria-label="主导航">{''.join(f'<a href="{u}">{n}</a>' for n,u in nav)}</nav><a class="header-cta" href="{CONTACT}">咨询购买 ↗</a><button class="menu-toggle" aria-expanded="false" aria-controls="navigation" aria-label="展开导航">☰</button></div></header><main id="main">{body}</main><footer><div class="container footer-grid"><div><a class="brand" href="index.html"><span class="brand-icon">A<span>＋</span></span><span><strong>AI Plus</strong><small>把更多时间，留给创造。</small></span></a><p>ChatGPT、Claude、Grok 订阅信息与购买导航。<br>独立第三方信息站，与 OpenAI、Anthropic、xAI 无隶属关系。</p></div><div><strong>探索</strong><a href="index.html#products">全部套餐</a><a href="guides.html">选购指南</a><a href="faq.html">常见问题</a></div><div><strong>关于本站</strong><a href="about.html">关于我们</a><a href="privacy.html">隐私说明</a><a href="terms.html">使用说明</a></div></div><div class="container footer-bottom"><span>© 2026 AI Plus</span><span>价格与套餐信息参考 GoPlus · 更新于 2026-09-13</span></div></footer><div class="mobile-bar">{btn('微信咨询',CONTACT,True)}{btn('选择套餐','index.html#products')}</div></body></html>'''
def write(slug,title,desc,body):
 title,desc=PAGE_META.get(slug,(title,desc))
 if slug!='404':
  if slug!='index':
   body='<div class="container seo-breadcrumb"><a href="index.html">首页</a><span> / </span><span>'+escape(title)+'</span></div>'+body
  body+='<div class="container">'+related_block(slug)+'</div>'
 if slug in ['guides','faq']:
  body=body.replace('<h2>', '<h1>', 1).replace('</h2>', '</h1>', 1)
 html=page(title,desc,body,slug)
 for dest in (SHOP,CONTACT):
  html=html.replace('href="'+dest+'"','href="'+dest+'" rel="sponsored nofollow" data-conversion="'+('shop' if dest==SHOP else 'consult')+'"')
 (OUT/link(slug)).write_text(html)
def guidecards():return '<div class="guide-grid">'+''.join(f'<a class="guide-card" href="{link(s)}"><div class="guide-art {s}"><span>{t}</span><b>{"GPT" if t=="CHATGPT" else "Claude" if t=="CLAUDE" else "Before you buy."}</b><i>↗</i></div><div class="guide-text"><h3>{n}</h3><p>{d}</p><span>阅读指南 →</span></div></a>' for s,n,t,d,b in guides)+'</div>'
def quick_prices():
 rows=[]
 for p in products:
  url='chatgpt-pro.html' if p['slug']=='chatgpt-pro-20x' else SHOP if p['mode']=='自助充值' else CONTACT
  action='查看状态' if p['slug']=='chatgpt-pro-20x' else '购买' if p['mode']=='自助充值' else '咨询'
  rows.append(f'<tr><th scope="row"><a href="{link(p["slug"])}">{p["name"]}</a></th><td><strong>¥{p["price"]}</strong><small>{p["unit"]}</small></td><td><a class="price-action" href="{url}">{action} →</a></td></tr>')
 return '<section class="container price-overview" id="price-list"><div class="price-heading"><h2>AI 订阅价格表</h2><a href="#products">查看套餐权益 ↓</a></div><div class="price-table-wrap"><table class="price-table"><thead><tr><th scope="col">套餐</th><th scope="col">价格</th><th scope="col">开通入口</th></tr></thead><tbody>'+''.join(rows)+'</tbody></table></div><p class="price-footnote">实际成交价以订单为准。Pro 20X 新购与升级状态请先确认。<a href="chatgpt-pro.html">查看说明 →</a></p></section>'
hero='<section class="hero price-hero"><div class="container"><h1>ChatGPT 充值与 AI 订阅</h1><p>Plus / Pro、Claude、Grok，先看价格，再选套餐。支持微信、支付宝购买渠道。</p></div></section>'
intent='<section class="container intent-section"><h2>你现在遇到哪一种情况？</h2><div class="intent-grid">'+''.join(f'<a href="{slug}.html"><strong>{name}</strong><span>{desc}</span><b aria-hidden="true">→</b></a>' for slug,name,desc in [('chatgpt-plus','第一次开通 Plus','价格、购买入口和开通步骤'),('chatgpt-renewal','会员快到期了','确认续费渠道，避免重复购买'),('chatgpt-payment-failed','付款一直失败','银行卡被拒与验证问题排查'),('chatgpt-charged-not-upgraded','扣了款，没有会员','按账号、订单和渠道检查')])+'</div><p class="intent-note">GPT 会员与 API 余额不是同一产品。<a href="chatgpt-api-vs-plus.html">先分清你需要充哪一种 →</a></p></section>'
body=hero+quick_prices()+'<section class="container section" id="products">'+heading('SUBSCRIPTIONS','热门 AI 订阅套餐','先选工具，再选使用强度。价格为服务商参考报价，实际权益与库存请在购买前确认。')+'<div class="product-tabs">'+''.join(f'<a href="#{g}">{logo(b)}{n}<span>{p}</span></a>' for g,b,n,p in [('chatgpt','gpt','ChatGPT','¥165 起'),('claude','claude','Claude','¥185 /月起'),('grok','grok','Grok','¥230 /月')])+'</div>'
for g,n,d in [('chatgpt','ChatGPT','写作、学习、办公与 Codex 编程辅助。'),('claude','Claude','长文档、细致写作与 Claude Code 工作流。'),('grok','Grok','关注实时话题、海外信息与 X 生态内容。')]:
 body+=f'<div class="product-group" id="{g}"><div class="group-title"><h2>{n} 套餐</h2><p>{d}</p></div><div class="product-grid {"single-product" if g=="grok" else ""}">'+''.join(product_card(p) for p in products if p['group']==g)+('</div></div>')
body+='</section><section class="soft-section"><div class="container section">'+heading('WORKFLOW','开通订阅，步骤很清楚','先确认，再下单；开通后，在自己的账号中核对套餐。')+'<div class="steps">'+''.join(f'<article><span class="step-number">0{i}</span><h3>{n}</h3><p>{d}</p></article>' for i,n,d in [(1,'选好产品与套餐','按使用场景选档，先确认当前账号与订阅状态。'),(2,'咨询或自助下单','基础档前往小店，高配套餐先联系服务商确认。'),(3,'按订单说明开通','核对交付方式和所需信息，保存订单与沟通记录。'),(4,'检查到账与有效期','在官方产品中确认订阅状态，有问题联系服务商。')])+'</div></div></section>'
body+='<section class="container section">'+heading('COMPARE','购买渠道，先了解再选择','不同渠道各有适用条件，支付前看清最终价格和售后约定。')+'''<div class="table-wrap"><table><thead><tr><th scope="col">对比维度</th><th scope="col">第三方服务商</th><th scope="col">官方渠道</th></tr></thead><tbody><tr><th scope="row">购买入口</th><td>小店下单 / 人工咨询</td><td>产品官网或官方 App</td></tr><tr><th scope="row">付款方式</th><td>以小店支持的微信、支付宝等为准</td><td>以官方支持的地区与支付方式为准</td></tr><tr><th scope="row">套餐价格</th><td>商家报价，付款前确认</td><td>官方定价与适用税费</td></tr><tr><th scope="row">交付与售后</th><td>实际服务商负责</td><td>官方支持渠道负责</td></tr><tr><th scope="row">购买前重点</th><td>身份、账号信息要求、退款与交付规则</td><td>地区资格、支付条件与续费规则</td></tr></tbody></table></div></section>'''
body+=intent+'<section class="soft-section"><div class="container section">'+heading('GUIDES','开通教程与选购指南','不急着选最贵的，先找到最适合你的。')+guidecards()+'</div></section><section class="container section faq-section">'+heading('FAQ','购买前常见问题','关于套餐、付款、账号与售后，把关键问题放在前面。')+faq(faqs[:6])+'<a class="more-link" href="faq.html">查看全部常见问题 →</a></section>'+contact()
write('index','GPT 充值指南','AI Plus 提供 ChatGPT Plus / Pro、Claude Pro / Max、Grok Super 套餐比较、购买指南与微信支付宝购买入口。',body)
for p in products:
 body=f'<section class="container section"><div class="breadcrumb"><a href="index.html">首页</a> / <a href="index.html#{p["group"]}">订阅套餐</a> / {p["name"]}</div><div class="detail-layout"><div><span class="eyebrow">AI SUBSCRIPTION</span><h1>{p["name"]} 充值<br>价格、购买与开通指南</h1><p class="intro">{p["desc"]}</p><h2>适合谁？</h2><p>{p["audience"]}。建议从你的实际使用频率出发，购买前确认当前账号、已有订阅和所需权益。</p><h2>购买前确认</h2><ul class="checks">{''.join('<li>'+x+'</li>' for x in p['features'])}</ul><div class="notice">页面价格及档位名称参考 GoPlus（2026-09-13），不代表官方报价。具体功能、使用额度与可用地区以官方最新规则为准，成交价和交付政策以下单时服务商确认为准。</div><h2>怎样开通？</h2><p>先选择套餐，前往小店查看库存与实际价格；人工交付套餐先咨询客服。核对账号状态与交付步骤后再付款，完成后到官方产品中确认订阅状态。</p><a class="detail-link" href="buying-guide.html">阅读完整购买指南 →</a></div>{product_card(p)}</div></section>'+contact()
 if p['slug']=='chatgpt-plus':
  summary=f'<div class="detail-price-first"><span>ChatGPT Plus</span><div class="price"><small>¥</small>{p["price"]}<small>{p["unit"]}</small></div><p>参考报价，以实际订单为准。</p><div class="actions">{btn("自助购买 Plus",SHOP)}{btn("微信咨询",CONTACT,True)}</div></div>'
  body=body.replace('</h1>','</h1>'+summary,1)
 extra=''.join('<section><h2>'+h+'</h2><p>'+text+'</p></section>' for h,text in DETAILS.get(p['slug'],[]))
 if p['group']=='chatgpt':
  extra+=source_block(['plus' if p['slug']=='chatgpt-plus' else 'pro','merchant'])
 elif p['slug'] in DETAILS: extra+=source_block(['merchant'])
 body=body.replace('<h2>适合谁？</h2>',extra+'<h2>适合谁？</h2>')
 if p['slug']=='chatgpt-pro-20x':
  body=body.replace('<h2>怎样开通？</h2><p>', '<h2>当前新购状态</h2><p>Pro 20X 新购与升级暂停，不能把下列通用流程当作可开通承诺。请先阅读 <a href="chatgpt-pro.html">Pro 档位与状态说明</a>。</p><p>')
 write(p['slug'],p['name']+' 充值与订阅指南',p['desc'],body)
for s,n,t,d,sections in guides:
 body=f'<article class="container article section"><div class="breadcrumb"><a href="index.html">首页</a> / <a href="guides.html">选购指南</a></div><span class="eyebrow">{t} GUIDE</span><h1>{n}</h1><p class="intro">{d}</p><p class="article-meta">更新于 2026 年 9 月 13 日 · <a href="about.html">AI Plus</a></p>'+''.join(f'<section><h2>{h}</h2><p>{p}</p></section>' for h,p in sections)+f'<div class="notice">延伸阅读：<a href="https://www.goplus.pro/guide">GoPlus 购买说明</a>。产品权益请核对对应官方订阅页面。</div><div class="actions">{btn("查看全部套餐","index.html#products")}</div></article>'
 if s=='choose-chatgpt':
  body=body.replace('<section>', '<div class="notice">2026-09-13 核对：Pro 20X 新购和升级暂停。<a href="chatgpt-pro.html">查看当前 Pro 档位与续费说明 →</a></div><section>',1)
 write(s,n,d,body)

def article_directory():
 return '<div class="guide-directory"><h2>GPT 充值问题，按情况查找</h2>'+''.join(f'<a href="{a["slug"]}.html"><h3>{a["title"]}</h3><p>{a["desc"]}</p></a>' for a in ARTICLES)+'</div>'
for a in ARTICLES:
 toc='<nav class="article-toc" aria-label="文章目录"><strong>本页内容</strong>'+''.join(f'<a href="#step-{i}">{h}</a>' for i,(h,t) in enumerate(a['sections'],1))+'</nav>'
 body='<article class="container article section"><span class="eyebrow">GPT RECHARGE GUIDE</span><h1>'+a['title']+'</h1><p class="intro">'+a['summary']+'</p><p class="article-meta">内容整理：<a href="about.html">AI Plus</a> · 更新于 2026-09-13</p>'+toc+''.join(f'<section id="step-{i}"><h2>{h}</h2><p>{text}</p></section>' for i,(h,text) in enumerate(a['sections'],1))+source_block(a['sources'])+'<div class="article-cta"><h2>需要确认购买或续费方案？</h2><p>先把账号当前套餐、到期日和问题说清楚，再决定是否下单。</p>'+btn(a['cta'],CONTACT)+btn('查看 Plus 充值方案','chatgpt-plus.html',True)+'</div></article>'
 write(a['slug'],a['title'],a['desc'],body)
pro_body='<article class="container article section"><span class="eyebrow">CHATGPT PRO</span><h1>ChatGPT Pro 充值与档位选择</h1><p class="intro">先看账号能否开通，再比较 5X 与 20X。高档位适合确实需要更多用量的用户。</p><div class="notice"><strong>新购状态 · 2026-09-13 核对</strong><p>OpenAI 自 2026 年 9 月 10 日起暂停 Pro $200（20X）新购与升级，已有订阅续费及 Pro $100 不受此次暂停影响。20X 取消到期后，在暂停解除前可能无法再次开通。</p></div><h2>Pro 5X 和 20X 怎么比较？</h2><div class="table-wrap"><table><thead><tr><th>项目</th><th>Pro 5X</th><th>Pro 20X</th></tr></thead><tbody><tr><th>官方美元月费</th><td>$100</td><td>$200</td></tr><tr><th>服务商参考报价</th><td>¥850 /月</td><td>¥1500 /月</td></tr><tr><th>新购与升级</th><td>官方当前仍提供</td><td>官方当前暂停</td></tr><tr><th>购买前判断</th><td>高频编程、研究需求</td><td>先确认是否为现有订阅</td></tr></tbody></table></div><h2>先从工作需求判断是否升级</h2><p>如果只是偶尔遇到限制，先检查当前套餐的重置时间与任务安排。持续编程、复杂研究占据主要工作时间时，再考虑 Pro。两档主要区别在用量，不代表所有模型永远无上限。</p><h2>已有 Plus，升级前要问什么？</h2><p>核对当前周期、原购买渠道和账号可见的升级选项。官方升级与降档的生效方式不同；使用第三方服务时还需确认实际交付方式，不默认剩余时长自动保留。</p><h2>已有 Pro 20X，续费要注意什么？</h2><p>新购暂停期间，不要为重新购买而先取消已有订阅。先核实当前周期与扣款状态；出现失败时沿原购买渠道处理，避免到期后失去重新开通资格。</p>'+source_block(['pro','merchant'])+'<div class="actions">'+btn('咨询当前账号的 Pro 方案',CONTACT)+btn('比较 Plus 套餐','chatgpt-plus.html',True)+'</div></article>'
write('chatgpt-pro',*PAGE_META['chatgpt-pro'],pro_body)
write('guides','AI 订阅选购指南','了解 ChatGPT、Claude 套餐选择和购买流程。','<section class="container section">'+heading('GUIDES','少一点纠结，多一点了解','从使用场景出发，找到适合自己的 AI 订阅。')+guidecards()+article_directory()+'</section>'+contact())
write('faq','AI 订阅常见问题','AI 订阅购买、账号、充值与售后常见问题。','<section class="container section faq-section">'+heading('HELP CENTER','你想知道的，都在这里','付款之前，先把套餐、交付和售后问清楚。')+faq(faqs)+'</section>'+contact())
for slug,title,sections in [
 ('about','关于 AI Plus',[('让选择更清楚','AI Plus 整理 ChatGPT、Claude、Grok 的订阅参考信息，帮助读者比较套餐、了解购买步骤。本站为独立第三方信息与购买导航站，并非上述产品的官方站点。'),('内容与购买入口','套餐报价和服务入口参考 GoPlus，页面标注了信息整理日期。购买和咨询会跳转至外部服务商，实际交易、交付和售后由服务商负责。'),('品牌说明','ChatGPT、Claude、Grok 及相关标志归各自权利人所有，仅用于产品识别。')]),
 ('privacy','隐私说明',[('本站收集哪些信息','本站为静态信息页面，不提供账号登录，不设置支付表单，不主动收集密码、验证码、会话令牌或支付资料，也未接入第三方行为统计。'),('托管与外部链接','网站由 GitHub Pages 托管，托管服务可能按其隐私政策记录请求信息。点击购买或咨询后，会进入第三方网站，并适用对方的隐私政策。'),('账号信息提醒','请勿通过公开渠道或不明页面发送账号凭据。提交交付所需信息前，应明确了解接收方身份、信息用途和访问权限。')]),
 ('terms','网站使用说明',[('信息用途','本站内容为产品比较和购买参考，不构成官方承诺。价格、名称、功能、额度、地区与库存可能变化，请在下单前确认最新信息。'),('第三方交易','本站不直接收款或交付订阅。通过外部链接产生的交易，请与实际服务商确认订单、退款、售后和账号适用条件。'),('使用产品','请遵循对应产品的使用条款与账号安全要求。第三方服务并不能免除官方规则，也不能保证不发生账号或订阅异常。')])]:
 write(slug,title,title+'与网站相关说明。','<article class="container article section"><h1>'+title+'</h1>'+''.join('<section><h2>'+h+'</h2><p>'+p+'</p></section>' for h,p in sections)+'</article>')
write('404','页面未找到','返回 AI Plus 首页查找套餐与指南。','<section class="container section empty"><span class="eyebrow">404</span><h1>这个页面暂时找不到了</h1><p>你可以回到首页继续查看套餐与指南。</p>'+btn('返回首页',BASE)+'</section>')
# The error page can be served for arbitrary nested URLs.
f=OUT/'404.html';s=f.read_text();s=s.replace('href="assets/','href="'+BASE+'assets/').replace('src="assets/','src="'+BASE+'assets/');s=s.replace('<head>','<head><base href="'+BASE+'">');s=s.replace('<link rel="canonical" href="'+BASE+'404.html">','');f.write_text(s)
shutil.copytree(ROOT/'assets',OUT/'assets',dirs_exist_ok=True)
(OUT/'.nojekyll').touch()
# Keep ownership verification files verbatim and outside the content sitemap.
static_files={p.name for p in (ROOT/'static').iterdir() if p.is_file()}
shutil.copytree(ROOT/'static',OUT,dirs_exist_ok=True)
urls=[BASE]+[BASE+p.name for p in sorted(OUT.glob('*.html')) if p.stem not in NOINDEX|{'index'} and p.name not in static_files]
(OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+u+'</loc></url>' for u in urls)+'</urlset>')
print(f'Built {len(urls)} pages + 404')
