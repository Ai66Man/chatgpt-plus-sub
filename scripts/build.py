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
    ("ChatGPT", "index.html#chatgpt"),
    ("Claude", "index.html#claude"),
    ("Grok", "index.html#grok"),
    ("选购对比", "guides.html"),
    ("购买指南", "buying-guide.html"),
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
    "index": ("AI 订阅充值：ChatGPT Plus、Claude Pro、Grok Super 微信支付宝直达",
              "ChatGPT Plus、Pro 5X / 20X，Claude Pro、Max，Grok Super 的人民币价格与开通入口，无需海外信用卡；另附各档位官方价格对比与选购建议。"),
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


def shop(page, position):
    """Self-service shop URL with campaign attribution."""
    parts = urlsplit(data.SHOP)
    query = dict(parse_qsl(parts.query))
    query.update({
        "utm_source": "github_pages",
        "utm_medium": "referral",
        "utm_campaign": "ai66man_compare",
        "utm_content": page + "__" + position,
    })
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))


def shop_link(page, position, label, secondary=False):
    cls = "button secondary" if secondary else "button"
    return ('<a class="' + cls + '" href="' + escape(shop(page, position)) + '" '
            'rel="sponsored nofollow" target="_blank" data-conversion="shop" '
            'data-position="' + escape(position) + '">' + escape(label)
            + ' <span aria-hidden="true">↗</span></a>')


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
        '<span class="brand-icon">AI<span>＋</span></span>'
        '<span><strong>' + data.SITE_NAME + "</strong><small>充值 · 价格 · 选购对比</small></span></a>"
        '<nav id="navigation" aria-label="主导航">' + nav + "</nav>"
        '<a class="header-cta" href="' + escape(goplus("home", slug, "header")) + '" '
        'rel="sponsored nofollow" target="_blank" data-conversion="consult" data-position="header">微信咨询 ↗</a>'
        '<button class="menu-toggle" aria-expanded="false" aria-controls="navigation" aria-label="展开导航">☰</button>'
        "</div></header><main id=\"main\">"
    )
    footer = (
        "</main><footer><div class=\"container footer-grid\">"
        '<div><a class="brand" href="index.html"><span class="brand-icon">AI<span>＋</span></span>'
        "<span><strong>" + data.SITE_NAME + "</strong><small>微信支付宝直达，开在自己账号。</small></span></a>"
        "<p>AI 订阅充值入口与跨品牌选购对比。与 OpenAI、Anthropic、xAI、Google 均无隶属关系。<br>"
        "开通、交付与售后由 GoPlus 负责，本站为其提供商业导流，详见关于本站。</p></div>"
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
def logo(brand):
    ext = "png" if brand == "gpt" else "svg"
    alt = {"gpt": "ChatGPT", "claude": "Claude", "grok": "Grok"}[brand]
    return ('<img src="assets/' + brand + "." + ext + '" width="30" height="30" alt="'
            + alt + ' 标志" loading="lazy">')


def product_card(prod):
    mode_label = "可自助下单" if prod["mode"] == "self" else "人工交付"
    badge = ('<span class="tag badge">' + prod["badge"] + "</span>") if prod["badge"] else ""
    if prod["mode"] == "self":
        action = shop_link("index", "card_" + prod["slug"], prod["cta"])
    else:
        action = cta(prod["goplus"], "index", "card_" + prod["slug"], prod["cta"])
    consult = ('<a href="' + escape(goplus("wechat", "index", "card_consult_" + prod["slug"]))
               + '" rel="sponsored nofollow" target="_blank" data-conversion="consult" '
                 'data-position="card_consult">微信咨询</a>')
    return (
        '<article class="product ' + prod["group"] + '" id="p-' + prod["slug"] + '">'
        '<div class="card-top"><span class="tag">' + prod["eyebrow"] + "</span>" + badge
        + logo(prod["brand"]) + "</div>"
        "<h3>" + escape(prod["name"]) + "</h3>"
        '<div class="price"><small>¥</small>' + prod["price"] + "<small>" + prod["unit"] + "</small></div>"
        '<p class="price-note">' + prod["official"] + " · " + mode_label + "</p>"
        '<p class="product-desc">' + escape(prod["desc"]) + "</p>"
        '<div class="audience"><small>适合人群</small>' + escape(prod["audience"]) + "</div>"
        '<ul class="checks">' + "".join("<li>" + escape(f) + "</li>" for f in prod["features"]) + "</ul>"
        '<div class="card-actions">' + action + consult + "</div></article>")


def render_home():
    tabs = "".join(
        '<a href="#' + key + '">' + logo(brand) + label.replace(" 套餐", "")
        + "<span>" + price + "</span></a>"
        for key, label, _tag, brand, price in data.PRODUCT_GROUPS)

    groups = ""
    for key, label, tagline, _brand, _price in data.PRODUCT_GROUPS:
        items = [x for x in data.PRODUCTS if x["group"] == key]
        single = " single-product" if len(items) == 1 else ""
        groups += ('<div class="product-group" id="' + key + '">'
                   '<div class="group-title"><h2>' + label + "</h2><p>" + tagline + "</p></div>"
                   '<div class="product-grid' + single + '">'
                   + "".join(product_card(x) for x in items) + "</div></div>")

    quick_rows = "".join(
        '<tr><th scope="row"><a href="#p-' + x["slug"] + '">' + escape(x["name"]) + "</a></th>"
        '<td><strong>¥' + x["price"] + "</strong><small>" + x["unit"] + "</small></td>"
        '<td>' + x["official"] + "</td>"
        '<td>' + ("自助下单" if x["mode"] == "self" else "人工交付") + "</td></tr>"
        for x in data.PRODUCTS)
    quick = ('<section class="container price-overview" id="price-list">'
             '<div class="price-heading"><h2>套餐与价格一览</h2>'
             '<a href="#products">查看套餐权益 ↓</a></div>'
             '<div class="price-table-wrap"><table class="price-table"><thead><tr>'
             '<th scope="col">套餐</th><th scope="col">价格</th>'
             '<th scope="col">官方价 / 额度</th><th scope="col">开通方式</th>'
             "</tr></thead><tbody>" + quick_rows + "</tbody></table></div>"
             '<p class="price-footnote">人民币价格同步自 GoPlus 商品页，核对于 ' + data.CHECKED
             + "，实际成交价以下单页面为准。</p></section>")

    trust = ('<div class="hero-bottom">'
             + "".join("<span><b>" + v + "</b>" + k + "</span>" for v, k in data.TRUST) + "</div>")

    steps = ('<div class="steps">' + "".join(
        "<article><span class=\"step-number\">0" + str(i + 1) + "</span><h3>" + n + "</h3><p>" + d + "</p></article>"
        for i, (n, d) in enumerate(data.STEPS)) + "</div>")

    compare = table(["对比维度", "本站 / GoPlus", "官方直购", "个人代充"],
                    [[r[0], r[1], r[2], r[3]] for r in data.CHANNEL_COMPARE])

    picks = ["ai-subscription-price-compare", "claude-vs-chatgpt", "claude-code-vs-codex"]
    guide_cards = "".join(
        '<a class="guide-card" href="' + a["slug"] + '.html"><div class="guide-text">'
        "<h3>" + escape(a["title"]) + "</h3><p>" + escape(a["desc"]) + "</p>"
        "<span>阅读对比 →</span></div></a>"
        for a in ARTICLES if a["slug"] in picks)

    body = (
        '<section class="hero"><div class="container">'
        '<div class="hero-badges"><span>国内用户可用</span><span>微信 / 支付宝付款</span>'
        "<span>无需海外信用卡</span></div>"
        "<h1><span>ChatGPT · Claude · Grok</span><br>订阅充值，微信支付宝直达</h1>"
        '<p class="hero-lead">支持 ChatGPT Plus / Pro 5X / 20X、Claude Pro / Max、Grok Super，'
        "开通在你自己的账号上。</p>"
        '<p class="hero-sub">不用折腾海外信用卡，基础档小店自助下单，高配档微信人工确认后交付。</p>'
        '<div class="actions">'
        '<a class="button" href="#price-list">查看套餐与价格</a>'
        + cta("wechat", "index", "hero_wechat", "微信咨询", secondary=True)
        + '<a class="text-button" href="buying-guide.html">购买前指南 →</a>'
        "</div>" + trust + "</div></section>"

        + quick +

        '<section class="container section" id="products">'
        + heading("SERVICE", "热门 AI 订阅充值入口",
                  "先选工具，再选强度档位。基础档可小店自助下单，Pro / Max 高配人工交付。")
        + '<div class="product-tabs">' + tabs + "</div>"
        + groups + "</section>"

        '<section class="soft-section"><div class="container section">'
        + heading("WORKFLOW", "开通流程", "先确认，再下单；开通后回自己的账号核对套餐。")
        + steps + "</div></section>"

        '<section class="container section">'
        + heading("COMPARE", "购买渠道对比", "和官方直购、个人代充相比，先看清差别再决定。")
        + compare
        + '<p class="price-footnote">官方直购总成本最低，前提是你有符合条件的境外付款方式；'
          '完整渠道说明见<a href="buying-guide.html">购买指南</a>。</p></section>'

        '<section class="soft-section"><div class="container section">'
        + heading("GUIDES", "选购参考", "不确定选哪一档？先看这几篇对比再下单。")
        + '<div class="guide-grid">' + guide_cards + "</div>"
        + '<a class="more-link" href="guides.html">查看全部对比文章 →</a></div></section>'

        '<section class="container section faq-section">'
        + heading("FAQ", "购买前常见问题", "最容易卡住的几个问题，先看完再决定下单还是咨询。")
        + faq_list(HOME_FAQ)
        + '<a class="more-link" href="faq.html">查看更多常见问题 →</a></section>'

        '<section class="contact-section"><div class="container contact-inner"><div>'
        '<span class="eyebrow">LET\u2019S GET STARTED</span><h2>选好了，就让 AI 开始帮忙。</h2>'
        "<p>基础档直接前往小店下单；Pro / Max 高配档先微信确认账号状态与套餐。</p>"
        '<div class="actions">' + shop_link("index", "footer_shop", "前往小店购买")
        + cta("wechat", "index", "footer_wechat", "联系微信客服", secondary=True) + "</div>"
        '<small>下单与咨询将前往 GoPlus 及其小店页面，交付与售后由该服务商负责。</small></div>'
        '<div class="contact-note"><span class="big-plus">＋</span>'
        "<strong>你的账号，你的工作流。</strong>"
        "<p>ChatGPT · Claude · Grok<br>开在自己的账号上。</p></div></div></section>"
    )
    schemas = schema_blocks("index", *PAGE_META["index"])
    schemas.append({"@context": "https://schema.org", "@type": "ItemList",
                    "name": "AI 订阅充值套餐", "itemListElement": [
                        {"@type": "ListItem", "position": i + 1, "name": x["name"],
                         "url": BASE + "#p-" + x["slug"], "description": x["desc"]}
                        for i, x in enumerate(data.PRODUCTS)]})
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
        "<h2>本站做什么</h2><p>本站提供两件事：一是 ChatGPT、Claude、Grok 订阅的"
        "<strong>国内开通入口与人民币价格</strong>；二是各家订阅的"
        "<strong>官方价格、额度口径与跨品牌选购对比</strong>，并标注核对日期。</p>"
        "<h2>谁在交付</h2><p>本站不销售、不开通任何订阅，也不收取任何款项。"
        "页面上的下单与咨询入口会跳转到 GoPlus 及其小店，实际的开通、交付、退款与售后全部由该服务商负责。"
        "遇到订单问题请通过该服务商的客服入口处理，本站无法查询订单。</p>"
        "<h2>不做什么</h2><p>本站不提供跨区订阅或绕过地区限制的方法，不提供任何成功率或到账时间承诺，"
        "也不编造订单量、用户评价或成功案例。页面上引用的服务承诺均来自 GoPlus 的公开说明，"
        "具体条款以下单时页面为准。</p>"
        "<h2>商业关系披露</h2><p>本站为 GoPlus 提供商业导流：页面中的「国内开通」入口会跳转到该第三方服务商，"
        "并带有来源标识参数。本站与 OpenAI、Anthropic、xAI、Google 均无隶属关系，"
        "也不是任何一家的官方网站。第三方的报价、交付与售后由该商家负责。</p>"
        "<h2>价格怎么核对</h2><p>页面上有两套价格。<strong>官方美元标价</strong>以各家官方定价页为准；"
        "<strong>人民币价格</strong>同步自 GoPlus 商品页，是该服务商的报价，不是官方价格，也不是汇率换算。"
        "两者每月 1 号核对一次并标注核对日期。价格随时可能调整，实际成交价以下单页面为准；"
        "发现价格过期或错误，欢迎通过下方渠道指出。</p>"
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
        "<h2>第三方交易</h2><p>本站不销售任何订阅，也不收款。页面上的人民币价格是 GoPlus 的报价，"
        "并非官方定价。通过本站进入该服务商后，交易、交付、退款与售后均由其负责，与本站无关。"
        "本站展示的服务承诺（如质保范围）引自其公开说明，不构成本站的承诺。</p>"
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
