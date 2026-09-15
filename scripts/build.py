# -*- coding: utf-8 -*-
"""Static builder for the AI subscription comparison site.

Outputs to docs/. Only official USD list prices live on this site; CNY retail
prices stay with the merchant. Merged/retired URLs become noindex meta-refresh
pages and are kept out of the sitemap.
"""
from html import escape
from pathlib import Path
from urllib.parse import urlencode, urlsplit, urlunsplit, parse_qsl
import json
import shutil
import sys

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs"
sys.path.insert(0, str(ROOT / "content"))

import data  # noqa: E402
from articles import ARTICLES, SITE_FAQ, HOME_FAQ, table  # noqa: E402

BASE = data.BASE
NAV = [
    ("价格总表", "ai-subscription-price-compare.html"),
    ("跨品牌对比", "guides.html"),
    ("编程订阅", "ai-coding-subscription-price.html"),
    ("购买渠道", "buying-guide.html"),
    ("常见问题", "faq.html"),
]

# Retired product/problem pages: each keeps its URL but points at the canonical
# version on the merchant site.
REDIRECTS = {
    "chatgpt-plus": ("chatgpt_plus", "ChatGPT Plus 充值"),
    "chatgpt-pro": ("chatgpt_pro", "ChatGPT Pro 充值"),
    "chatgpt-pro-5x": ("chatgpt_pro", "ChatGPT Pro 5X"),
    "chatgpt-pro-20x": ("chatgpt_pro", "ChatGPT Pro 20X"),
    "claude-pro": ("claude", "Claude Pro 充值"),
    "claude-max-5x": ("claude_max_5x", "Claude Max 5X"),
    "claude-max-20x": ("claude_max_20x", "Claude Max 20X"),
    "grok-super": ("grok", "Grok Super 充值"),
    "choose-chatgpt": ("chatgpt_choose", "ChatGPT Plus / Pro 怎么选"),
    "choose-claude": ("claude_choose", "Claude Pro / Max 怎么选"),
    "chatgpt-payment-failed": ("payment_declined", "ChatGPT 付款失败"),
    "chatgpt-charged-not-upgraded": ("not_showing", "扣款成功但没有 Plus"),
    "chatgpt-renewal": ("renewal_failed", "ChatGPT 续费"),
}

PAGE_META = {
    "index": ("AI 订阅价格对比 2026：ChatGPT、Claude、Grok、Gemini 全档位比价与选购",
              "对比 ChatGPT、Claude、Gemini、Grok 全部消费级订阅档位的官方美元价、额度与适合人群，并按写作、编程、学生等用途给出选择建议。"),
    "guides": ("AI 订阅横评与对比文章索引：价格、编程、跨品牌选购",
               "本站全部对比文章的索引：AI 订阅价格总表、Claude 与 ChatGPT 对比、编程订阅比价、国内 Coding Plan 横评与购买渠道说明。"),
    "faq": ("AI 订阅常见问题：价格、额度、付款与选购",
            "集中回答 AI 订阅的价格区间、额度口径、年付是否划算、编程该订哪家、国内怎么付款等 15 个高频问题。"),
    "about": ("关于本站：定位、商业关系与资料核验方式",
              "AI 订阅比价指南的内容范围、与 GoPlus 的商业关系披露、价格核对方式与纠错渠道。"),
    "privacy": ("隐私与访问统计说明",
                "本站的访问统计方式、外部跳转说明，以及不收集任何账号凭据的声明。"),
    "terms": ("使用说明与免责声明",
              "本站信息的用途边界、价格时效说明，以及与各 AI 厂商无隶属关系的声明。"),
    "404": ("页面不存在", "该页面不存在或已合并，请从导航进入价格总表或对比文章。"),
}

ART_BY_SLUG = {a["slug"]: a for a in ARTICLES}


# --------------------------------------------------------------------------- helpers
def goplus(key, page, position):
    """Merchant URL with campaign attribution attached."""
    parts = urlsplit(data.GOPLUS[key])
    query = dict(parse_qsl(parts.query))
    query.update({
        "utm_source": "github_pages",
        "utm_medium": "referral",
        "utm_campaign": "ai66man_compare",
        "utm_content": page + "__" + position,
    })
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))


def cta(key, page, position, label, secondary=False):
    href = goplus(key, page, position)
    cls = "button secondary" if secondary else "button"
    return ('<a class="' + cls + '" href="' + escape(href) + '" rel="sponsored nofollow" '
            'target="_blank" data-conversion="consult" data-position="' + escape(position) + '">'
            + escape(label) + ' <span aria-hidden="true">↗</span></a>')


def heading(eyebrow, title, sub, level="h2"):
    return ('<div class="section-head"><span class="eyebrow">' + eyebrow + '</span>'
            '<' + level + '>' + title + '</' + level + '>'
            '<p>' + sub + '</p></div>')


def analytics():
    gid = data.GA_ID
    return (
        '<script async src="https://www.googletagmanager.com/gtag/js?id=' + gid + '"></script>\n'
        '<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}'
        "gtag('js',new Date());gtag('config'," + json.dumps(gid) + ","
        "{page_location:location.origin+location.pathname,"
        "page_referrer:document.referrer?document.referrer.split('?')[0].split('#')[0]:''});"
        "document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest("
        "'a[data-conversion]');if(!a)return;var u=a.getAttribute('href')||'';"
        "gtag('event','outbound_click',{link_domain:(u.split('/')[2]||''),"
        "link_url:u.split('?')[0],page_name:document.body.getAttribute('data-page')||'',"
        "cta_position:a.getAttribute('data-position')||''});});</script>"
    )


def schema_blocks(slug, title, desc, article=None):
    url = BASE + ("" if slug == "index" else slug + ".html")
    blocks = [
        {"@context": "https://schema.org", "@type": "WebSite", "@id": BASE + "#website",
         "url": BASE, "name": data.SITE_NAME, "inLanguage": "zh-CN"},
        {"@context": "https://schema.org", "@type": "WebPage", "@id": url + "#webpage",
         "url": url, "name": title, "description": desc,
         "isPartOf": {"@id": BASE + "#website"}, "inLanguage": "zh-CN"},
    ]
    if slug != "index":
        blocks.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "首页", "item": BASE},
            {"@type": "ListItem", "position": 2, "name": title, "item": url}]})
    if article:
        blocks.append({
            "@context": "https://schema.org", "@type": "Article",
            "headline": title, "description": desc, "mainEntityOfPage": url, "url": url,
            "datePublished": article.get("published", data.CHECKED),
            "dateModified": data.CHECKED, "inLanguage": "zh-CN",
            "author": {"@type": "Organization", "name": data.SITE_NAME, "url": BASE + "about.html"},
            "publisher": {"@type": "Organization", "name": data.SITE_NAME, "url": BASE + "about.html"}})
    return blocks


def faq_schema(items):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q,
         "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}} for q, a in items]}


def strip_tags(html):
    out = []
    depth = 0
    for ch in html:
        if ch == "<":
            depth += 1
        elif ch == ">":
            depth -= 1
        elif depth == 0:
            out.append(ch)
    return "".join(out)


def faq_list(items):
    return ('<div class="faq-list">' + "".join(
        "<details><summary>" + escape(q) + "</summary><p>" + a + "</p></details>"
        for q, a in items) + "</div>")


def page(slug, body, schemas, noindex=False):
    title, desc = PAGE_META.get(slug, ("", ""))
    canonical = BASE + ("" if slug == "index" else slug + ".html")
    robots = "noindex, follow" if noindex else "index, follow, max-image-preview:large"
    nav = "".join('<a href="' + u + '">' + n + "</a>" for n, u in NAV)
    ld = "".join('<script type="application/ld+json">'
                 + json.dumps(s, ensure_ascii=False).replace("<", "\\u003c")
                 + "</script>" for s in schemas)
    head = (
        '<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        '<title>' + escape(title) + " | " + data.SITE_NAME + "</title>"
        '<meta name="description" content="' + escape(desc) + '">'
        '<meta name="robots" content="' + robots + '">'
        + ("" if slug == "404" else '<link rel="canonical" href="' + canonical + '">')
        + '<meta name="theme-color" content="#28766d">'
        '<meta property="og:type" content="website">'
        '<meta property="og:title" content="' + escape(title) + '">'
        '<meta property="og:description" content="' + escape(desc) + '">'
        + ("" if slug == "404" else '<meta property="og:url" content="' + canonical + '">')
        + '<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">'
        '<link rel="stylesheet" href="assets/style.css">'
        '<script src="assets/app.js" defer></script>'
        + ld + analytics() + "</head>"
    )
    header = (
        '<body data-page="' + slug + '"><a class="skip-link" href="#main">跳到正文</a>'
        '<header><div class="container header-inner">'
        '<a class="brand" href="index.html" aria-label="' + data.SITE_NAME + ' 首页">'
        '<span class="brand-icon">比<span>价</span></span>'
        '<span><strong>' + data.SITE_NAME + "</strong><small>官方价格 · 额度 · 选购对比</small></span></a>"
        '<nav id="navigation" aria-label="主导航">' + nav + "</nav>"
        '<a class="header-cta" href="' + escape(goplus("home", slug, "header")) + '" '
        'rel="sponsored nofollow" target="_blank" data-conversion="consult" data-position="header">国内开通 ↗</a>'
        '<button class="menu-toggle" aria-expanded="false" aria-controls="navigation" aria-label="展开导航">☰</button>'
        "</div></header><main id=\"main\">"
    )
    footer = (
        "</main><footer><div class=\"container footer-grid\">"
        '<div><a class="brand" href="index.html"><span class="brand-icon">比<span>价</span></span>'
        "<span><strong>" + data.SITE_NAME + "</strong><small>先看价格，再看额度。</small></span></a>"
        "<p>独立的 AI 订阅比价与横评站，与 OpenAI、Anthropic、xAI、Google 均无隶属关系。<br>"
        "本站为 GoPlus 提供商业导流，详见关于本站。</p></div>"
        '<div><strong>对比</strong><a href="ai-subscription-price-compare.html">价格总表</a>'
        '<a href="claude-vs-chatgpt.html">Claude vs ChatGPT</a>'
        '<a href="coding-plan-compare.html">Coding Plan 对比</a></div>'
        '<div><strong>关于</strong><a href="about.html">关于本站</a>'
        '<a href="privacy.html">隐私说明</a><a href="terms.html">使用说明</a>'
        '<a href="' + data.REPO + '" rel="noopener" target="_blank">GitHub 仓库</a></div></div>'
        '<div class="container footer-bottom"><span>© 2026 ' + data.SITE_NAME + "</span>"
        "<span>价格核对于 " + data.CHECKED + "，以各家官方定价页为准</span></div></footer></body></html>"
    )
    return head + header + body + footer


# --------------------------------------------------------------------------- pages
def render_home():
    rows = []
    for brand, tier, price, unit, quota, who, _key in data.PLANS:
        label = brand + " " + tier
        cost = "免费" if price == "0" else "$" + price + " " + unit
        rows.append([escape(label), cost, escape(quota), escape(who)])
    price_table = table(["档位", "官方美元价", "额度与权益要点", "适合谁"], rows)

    cases = "".join(
        '<a class="guide-card" href="' + slug + '.html"><div class="guide-text">'
        "<h3>" + name + "</h3><p>" + desc + "</p><span>查看对比 →</span></div></a>"
        for name, desc, slug in data.USE_CASES)

    body = (
        '<section class="hero"><div class="container">'
        '<div class="hero-badges"><span>官方美元标价</span><span>每月核对</span><span>不做单品充值页</span></div>'
        "<h1>ChatGPT、Claude、Grok、Gemini 订阅怎么选？<br>价格、额度与国内开通对比</h1>"
        '<p class="hero-lead">一张表看完四家全部消费级档位的官方价格、额度说明和适合人群。</p>'
        '<p class="hero-sub">本站只列各家官方美元标价并注明核对日期，不维护人民币报价；'
        "国内开通价格与档位请前往 GoPlus 确认。</p>"
        '<div class="actions">'
        '<a class="button" href="#price-list">查看全档位价格表</a>'
        '<a class="button secondary" href="claude-vs-chatgpt.html">Claude 和 ChatGPT 怎么选</a>'
        '<a class="text-button" href="ai-coding-subscription-price.html">编程订阅要花多少 →</a>'
        "</div></div></section>"

        '<section class="container section" id="price-list">'
        + heading("PRICING", "2026 年 AI 订阅全档位价格表", "核对于 " + data.CHECKED
                  + "，为各家官方美元标价，不含当地税费。", level="h2")
        + price_table
        + '<p class="price-footnote">完整对比与选购建议见'
          '<a href="ai-subscription-price-compare.html">价格对比详解</a>。</p></section>'

        '<section class="soft-section"><div class="container section">'
        + heading("BY USE CASE", "按用途找对比", "先确定自己要用来做什么，再比价格。")
        + '<div class="guide-grid">' + cases + "</div></div></section>"

        '<section class="container section">'
        + heading("HOW TO READ", "这张表该怎么看", "三条规律，比记住具体数字更有用。")
        + "<ol><li><strong>入门档价格高度趋同。</strong>四家的主力个人档都在 20 美元上下，"
          "差别在功能面和额度口径，不在价格。</li>"
          "<li><strong>高价档卖的是额度，不是更聪明。</strong>100 和 200 美元档提升的是用量上限，"
          "官方的倍数说明针对整体用量，个别功能可能有独立限制。</li>"
          "<li><strong>先用满一个档再升级。</strong>记录每周被额度打断的次数，"
          "和差价比较后再决定，比凭感觉升级省钱。</li></ol></section>"

        '<section class="container section">'
        + heading("FAQ", "下单前最常问的五个问题", "关于价格口径和档位选择，先把这几件事说清楚。")
        + faq_list(HOME_FAQ)
        + '<a class="more-link" href="faq.html">查看全部常见问题 →</a></section>'

        '<section class="contact-section"><div class="container contact-inner"><div>'
        '<span class="eyebrow">国内开通</span><h2>选好了档位，再看怎么开通。</h2>'
        "<p>本站不维护人民币报价。具体档位、当前价格与交付方式，前往 GoPlus 确认后再下单。</p>"
        '<div class="actions">' + cta("home", "index", "footer_primary", "查看国内开通档位")
        + cta("chatgpt_plus", "index", "footer_chatgpt", "ChatGPT 开通", secondary=True) + "</div>"
        '<small>购买与咨询将前往第三方服务商页面，本站与其为商业导流关系。</small></div>'
        '<div class="contact-note"><span class="big-plus">＝</span><strong>先比价，再下单。</strong>'
        "<p>官方价格 · 额度口径 · 开通渠道<br>三件事分开看。</p></div></div></section>"
    )
    schemas = schema_blocks("index", *PAGE_META["index"])
    schemas.append(faq_schema(HOME_FAQ))
    return page("index", body, schemas)


def render_article(art):
    slug = art["slug"]
    PAGE_META[slug] = (art["title"], art["desc"])
    sections = "".join(
        '<section class="section" id="s' + str(i + 1) + '"><h2>' + h2 + "</h2>" + html + "</section>"
        for i, (h2, html) in enumerate(art["sections"]))
    toc = "".join('<a href="#s' + str(i + 1) + '">' + h2 + "</a>"
                  for i, (h2, _) in enumerate(art["sections"]))
    def source_item(k):
        title, url = data.SOURCES[k]
        if "goplus.pro" in url:
            return ('<li><a href="' + escape(goplus("home", slug, "source"))
                    + '" rel="sponsored nofollow noopener" target="_blank" '
                      'data-conversion="consult" data-position="source">' + title + "</a></li>")
        return '<li><a href="' + url + '" rel="noopener" target="_blank">' + title + "</a></li>"

    src = ('<aside class="sources"><strong>资料来源</strong><ul>'
           + "".join(source_item(k) for k in art["sources"])
           + "</ul><small>核对日期：" + data.CHECKED
           + "。价格与额度规则可能调整，请以各家官方页面为准。</small></aside>")
    related = ('<aside class="related"><h2>继续对比</h2><div>'
               + "".join('<a href="' + s + '.html">' + escape(ART_BY_SLUG[s]["title"]) + " →</a>"
                         for s in art["related"] if s in ART_BY_SLUG)
               + "</div></aside>")
    faq_html = ('<section class="section faq-section"><h2>常见追问</h2>'
                + faq_list(art["faq"]) + "</section>") if art.get("faq") else ""
    key, label = art["cta"]
    body = (
        '<div class="container seo-breadcrumb"><a href="index.html">首页</a><span> / </span>'
        "<span>" + escape(art["title"]) + "</span></div>"
        '<article class="container article">'
        "<h1>" + escape(art["title"]) + "</h1>"
        '<p class="article-meta">核对于 ' + data.CHECKED + " · " + data.SITE_NAME + "</p>"
        '<p class="intro">' + art["lead"] + "</p>"
        '<nav class="article-toc" aria-label="本页目录">' + toc + "</nav>"
        + sections + faq_html
        + '<aside class="article-cta"><p>本站不维护人民币报价。确定档位后，'
          "国内开通方式与当前价格请在 GoPlus 确认。</p>"
        + cta(key, slug, "article_end", label) + "</aside>"
        + src + related + "</article>"
    )
    schemas = schema_blocks(slug, art["title"], art["desc"], article=art)
    if art.get("faq"):
        schemas.append(faq_schema(art["faq"]))
    return page(slug, body, schemas)


def render_guides():
    cards = "".join(
        '<a class="guide-card" href="' + a["slug"] + '.html"><div class="guide-text">'
        "<h3>" + escape(a["title"]) + "</h3><p>" + escape(a["desc"]) + "</p>"
        "<span>阅读对比 →</span></div></a>" for a in ARTICLES)
    body = (
        '<div class="container seo-breadcrumb"><a href="index.html">首页</a>'
        "<span> / </span><span>对比文章索引</span></div>"
        '<section class="container section">'
        + heading("INDEX", "AI 订阅横评与对比文章", "全部对比文章按主题排列，价格数据每月核对。", level="h1")
        + '<div class="guide-grid">' + cards + "</div></section>")
    return page("guides", body, schema_blocks("guides", *PAGE_META["guides"]))


def render_faq():
    body = (
        '<div class="container seo-breadcrumb"><a href="index.html">首页</a>'
        "<span> / </span><span>常见问题</span></div>"
        '<section class="container section faq-section">'
        + heading("FAQ", "AI 订阅常见问题：价格、额度、付款与选购",
                  "15 个高频问题，先给短答案，需要细节时点进对应对比页。", level="h1")
        + faq_list(SITE_FAQ)
        + '<p class="price-footnote">完整价格对比见'
          '<a href="ai-subscription-price-compare.html">全档位价格表</a>，'
          '开通渠道见<a href="buying-guide.html">渠道对比</a>。</p></section>')
    schemas = schema_blocks("faq", *PAGE_META["faq"])
    schemas.append(faq_schema(SITE_FAQ))
    return page("faq", body, schemas)


STATIC_PAGES = {
    "about": (
        "<h2>本站做什么</h2><p>本站只做一件事：把 ChatGPT、Claude、Gemini、Grok 以及主流 AI 编程工具的"
        "<strong>官方订阅价格、额度口径和适用场景</strong>整理成可以横向比较的表格，并标注核对日期。</p>"
        "<h2>不做什么</h2><p>本站不做单品充值页，不维护人民币报价，不提供跨区订阅或绕过地区限制的方法，"
        "也不提供任何成功率承诺。</p>"
        "<h2>商业关系披露</h2><p>本站为 GoPlus 提供商业导流：页面中的「国内开通」入口会跳转到该第三方服务商，"
        "并带有来源标识参数。本站与 OpenAI、Anthropic、xAI、Google 均无隶属关系，"
        "也不是任何一家的官方网站。第三方的报价、交付与售后由该商家负责。</p>"
        "<h2>价格怎么核对</h2><p>价格以各家官方定价页为准，每月 1 号核对一次，页面上标注核对日期。"
        "官方随时可能调整，付款前请以结算页显示为准。发现价格过期或错误，欢迎通过下方渠道指出。</p>"
        "<h2>纠错渠道</h2><p>内容问题可在 "
        '<a href="' + data.REPO + '/issues" rel="noopener" target="_blank">GitHub 仓库 Issues</a> '
        "反馈，请附页面地址和需要修正的表述。请不要提交订单、账号或支付资料。</p>"),
    "privacy": (
        "<h2>访问统计</h2><p>本站使用 Google Analytics 4 统计页面访问与外部链接点击。"
        "统计服务可能使用 Cookie 与设备、来源等信息，处理方式参见 "
        '<a href="https://policies.google.com/privacy" rel="noopener" target="_blank">Google 隐私政策</a>。'
        "浏览器的隐私设置或拦截工具可能阻止这些统计。</p>"
        "<h2>我们记录什么</h2><p>外部入口点击会记录页面名称、按钮位置和清理过查询参数的目标地址，"
        "用于判断哪些对比内容更有用。点击不代表购买，本站也无法获知你在第三方页面的行为。</p>"
        "<h2>本站不收集账号信息</h2><p>本站没有任何表单，不接收密码、验证码、会话凭据或支付信息。"
        "任何要求你在本站提交这些内容的页面都不是本站。</p>"
        "<h2>离开本站之后</h2><p>外部链接带有来源标识参数。离开后由目标网站负责其数据处理与交易。</p>"),
    "terms": (
        "<h2>信息用途</h2><p>本站内容用于购买前的比较参考，不构成任何购买建议或保证。"
        "各家产品的功能、价格、额度与可用地区以官方最新说明为准。</p>"
        "<h2>价格时效</h2><p>页面标注的核对日期表示最近一次核对时间。官方定价随时可能调整，"
        "本站不承诺表中价格与当前官方价格完全一致。</p>"
        "<h2>第三方交易</h2><p>本站不销售任何订阅。通过本站进入第三方服务商后，"
        "交易、交付与售后均由该商家负责，与本站无关。</p>"
        "<h2>商标与隶属关系</h2><p>ChatGPT、Claude、Gemini、Grok 等名称归各自权利人所有。"
        "本站与 OpenAI、Anthropic、Google、xAI 均无隶属、合作或授权关系。</p>"),
}


def render_static(slug):
    title, _ = PAGE_META[slug]
    body = ('<div class="container seo-breadcrumb"><a href="index.html">首页</a>'
            "<span> / </span><span>" + escape(title) + "</span></div>"
            '<section class="container section article"><h1>' + escape(title) + "</h1>"
            + STATIC_PAGES[slug] + "</section>")
    return page(slug, body, schema_blocks(slug, *PAGE_META[slug]))


def render_404():
    body = ('<section class="container section article"><h1>页面不存在</h1>'
            "<p>这个地址不存在，或者对应的页面已经合并到新的对比文章里。</p>"
            '<p><a class="button" href="' + BASE + '">回到价格总表</a></p></section>')
    return page("404", body, schema_blocks("404", *PAGE_META["404"]), noindex=True)


def render_redirect(slug, key, label):
    target = goplus(key, slug, "redirect")
    title = label + "已迁移 | " + data.SITE_NAME
    return (
        '<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        "<title>" + escape(title) + "</title>"
        '<meta name="robots" content="noindex, follow">'
        '<meta name="description" content="' + escape(label) + '页面已迁移，正在跳转到当前页面。">'
        '<meta http-equiv="refresh" content="0; url=' + escape(target) + '">'
        '<link rel="canonical" href="' + escape(target) + '">'
        '<link rel="stylesheet" href="assets/style.css"></head>'
        '<body data-page="' + slug + '"><main class="container section article">'
        "<h1>" + escape(label) + "页面已迁移</h1>"
        "<p>本站已转为 AI 订阅比价与横评站，不再维护单品充值页。"
        '如果没有自动跳转，请<a href="' + escape(target) + '" rel="sponsored nofollow">前往当前页面</a>，'
        '或回到<a href="index.html">价格总表</a>。</p></main></body></html>')


# --------------------------------------------------------------------------- main
def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "assets").mkdir(parents=True)
    for item in (ROOT / "assets").iterdir():
        if item.is_file():
            shutil.copy2(item, OUT / "assets" / item.name)
    for item in (ROOT / "static").iterdir():
        if item.is_file():
            shutil.copy2(item, OUT / item.name)

    written = []  # (filename, indexable)
    (OUT / "index.html").write_text(render_home(), encoding="utf-8")
    written.append(("index.html", True))
    for art in ARTICLES:
        (OUT / (art["slug"] + ".html")).write_text(render_article(art), encoding="utf-8")
        written.append((art["slug"] + ".html", True))
    (OUT / "guides.html").write_text(render_guides(), encoding="utf-8")
    written.append(("guides.html", True))
    (OUT / "faq.html").write_text(render_faq(), encoding="utf-8")
    written.append(("faq.html", True))
    for slug in STATIC_PAGES:
        (OUT / (slug + ".html")).write_text(render_static(slug), encoding="utf-8")
        written.append((slug + ".html", True))
    (OUT / "404.html").write_text(render_404(), encoding="utf-8")
    for slug, (key, label) in REDIRECTS.items():
        (OUT / (slug + ".html")).write_text(render_redirect(slug, key, label), encoding="utf-8")

    urls = []
    for name, indexable in written:
        if not indexable:
            continue
        urls.append(BASE + ("" if name == "index.html" else name))
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>',
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url in urls:
        sitemap.append("  <url><loc>" + url + "</loc><lastmod>" + data.CHECKED + "</lastmod></url>")
    sitemap.append("</urlset>")
    (OUT / "sitemap.xml").write_text("\n".join(sitemap) + "\n", encoding="utf-8")
    (OUT / "robots.txt").write_text(
        "# GitHub project deployment: crawlers read https://ai66man.github.io/robots.txt,\n"
        "# not this project-path file. Submit the sitemap in Search Console.\n"
        "User-agent: *\nAllow: /\nSitemap: " + BASE + "sitemap.xml\n", encoding="utf-8")
    (OUT / ".nojekyll").write_text("", encoding="utf-8")
    print("Built " + str(len(urls)) + " indexable pages, "
          + str(len(REDIRECTS)) + " redirects, 404 and sitemap.")


if __name__ == "__main__":
    main()
