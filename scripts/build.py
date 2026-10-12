# -*- coding: utf-8 -*-
"""Static builder for the AI subscription comparison site.

Outputs to docs/. Only official USD list prices live on this site; CNY retail
prices stay with the merchant. Merged/retired URLs become noindex meta-refresh
pages and are kept out of the sitemap. Every page carries its own last-modified
date (articles: `updated`; other pages: data.PAGE_DATES) for sitemap/schema.
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
from articles import ARTICLES, SITE_FAQ, table  # noqa: E402

BASE = data.BASE
NAV = [
    ("价格总表", "ai-subscription-price-compare.html"),
    ("对比文章", "guides.html"),
    ("编程订阅", "claude-code-vs-codex.html"),
    ("购买渠道", "buying-guide.html"),
    ("常见问题", "faq.html"),
    ("关于", "about.html"),
]

# Retired product/problem pages: each keeps its URL but points at the canonical
# version on the merchant side.
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
              "把 ChatGPT、Claude、Grok、Gemini 四家订阅的官方美元价格、额度口径和适合人群放在一张表里对比，按写作、编程、学生、图片视频、办公五种用途给出选购结论，并说明国内开通的几条路径。"),
    "guides": ("AI 订阅横评与对比文章索引：价格、编程、跨品牌选购",
               "本站全部对比文章的索引：AI 订阅价格总表、Claude 与 ChatGPT 对比、编程订阅比价、国内 Coding Plan 横评与购买渠道说明，每篇注明适合谁看。"),
    "faq": ("AI 订阅常见问题：价格、额度、付款与选购",
            "集中回答 AI 订阅的价格区间、额度口径、年付是否划算、编程该订哪家、国内怎么付款、第三方代充是否安全等 20 个高频问题。"),
    "about": ("关于本站：定位、比价口径、商业关系与资料核验方式",
              "AI 订阅比价指南的内容范围、只列官方美元价的比价口径、与 GoPlus 的商业关系披露、价格核对频率与纠错渠道。"),
    "privacy": ("隐私与访问统计说明",
                "本站的访问统计方式、外部跳转说明，以及不收集任何账号凭据的声明。"),
    "terms": ("使用说明与免责声明",
              "本站信息的用途边界、价格时效说明，以及与各 AI 厂商无隶属关系的声明。"),
    "404": ("页面不存在", "该页面不存在或已合并，请从导航进入价格总表或对比文章。"),
}

ART_BY_SLUG = {a["slug"]: a for a in ARTICLES}
UTM = {"utm_source": "github_pages", "utm_medium": "referral", "utm_campaign": "ai66man_compare"}


# --------------------------------------------------------------------------- helpers
def tagged(url, page, position):
    parts = urlsplit(url)
    query = dict(parse_qsl(parts.query))
    query.update(UTM)
    query["utm_content"] = page + "__" + position
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))


def goplus(key, page, position):
    """Merchant URL (goplus.pro or its shop) with campaign attribution."""
    return tagged(data.GOPLUS[key], page, position)


def shop(page, position):
    """Self-service shop URL with campaign attribution."""
    return tagged(data.SHOP, page, position)


def shop_link(page, position, label, secondary=False):
    cls = "button secondary" if secondary else "button"
    return ('<a class="' + cls + '" href="' + escape(shop(page, position)) + '" '
            'rel="sponsored nofollow" target="_blank" data-conversion="shop" '
            'data-position="' + escape(position) + '">' + escape(label)
            + ' <span aria-hidden="true">↗</span></a>')


def shop_text_link(page, position, label):
    return ('<a href="' + escape(shop(page, position)) + '" rel="sponsored nofollow" '
            'target="_blank" data-conversion="shop" data-position="' + escape(position) + '">'
            + escape(label) + "</a>")


def merchant_text_link(page, position, label):
    return ('<a href="' + escape(goplus("home", page, position)) + '" rel="sponsored nofollow noopener" '
            'target="_blank" data-conversion="consult" data-position="' + escape(position) + '">'
            + escape(label) + "</a>")


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


def page_date(slug):
    if slug in ART_BY_SLUG:
        return ART_BY_SLUG[slug]["updated"]
    return data.PAGE_DATES.get(slug, data.TODAY)


def schema_blocks(slug, title, desc, article=None):
    url = BASE + ("" if slug == "index" else slug + ".html")
    blocks = [
        {"@context": "https://schema.org", "@type": "WebSite", "@id": BASE + "#website",
         "url": BASE, "name": data.SITE_NAME, "inLanguage": "zh-CN"},
        {"@context": "https://schema.org", "@type": "WebPage", "@id": url + "#webpage",
         "url": url, "name": title, "description": desc, "dateModified": page_date(slug),
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
            "datePublished": article["published"],
            "dateModified": article["updated"], "inLanguage": "zh-CN",
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
        '<span><strong>' + data.SITE_NAME + "</strong><small>只列官方美元价，标注核对日期</small></span></a>"
        '<nav id="navigation" aria-label="主导航">' + nav + "</nav>"
        '<a class="header-cta" href="ai-subscription-price-compare.html">看价格总表</a>'
        '<button class="menu-toggle" aria-expanded="false" aria-controls="navigation" aria-label="展开导航">☰</button>'
        "</div></header><main id=\"main\">"
    )
    footer = (
        "</main><footer><div class=\"container footer-grid\">"
        '<div><a class="brand" href="index.html"><span class="brand-icon">AI<span>＋</span></span>'
        "<span><strong>" + data.SITE_NAME + "</strong><small>跨品牌比价与横评</small></span></a>"
        "<p>ChatGPT、Claude、Gemini、Grok 以及主流 AI 编程工具的订阅价格、额度口径与选购对比。<br>"
        "页面只列各家官方美元标价并注明核对日期，人民币开通价不在本站维护。<br>"
        "与 OpenAI、Anthropic、Google、xAI 均无隶属关系；本站为 GoPlus 提供商业导流。</p></div>"
        '<div><strong>对比文章</strong><a href="ai-subscription-price-compare.html">全档位价格表</a>'
        '<a href="claude-vs-chatgpt.html">Claude vs ChatGPT</a>'
        '<a href="claude-code-vs-codex.html">Claude Code vs Codex</a>'
        '<a href="coding-plan-compare.html">Coding Plan 对比</a>'
        '<a href="buying-guide.html">购买渠道对比</a></div>'
        '<div><strong>关于</strong><a href="about.html">关于本站</a>'
        '<a href="faq.html">常见问题</a>'
        '<a href="privacy.html">隐私说明</a><a href="terms.html">使用说明</a>'
        '<a href="' + data.REPO + '" rel="noopener" target="_blank">GitHub 仓库</a></div></div>'
        '<div class="container footer-bottom"><span>© 2026 ' + data.SITE_NAME + "</span>"
        "<span>官方美元价核对于 " + data.CHECKED + "，不含税费；实际扣款以各家结算页为准</span></div></footer></body></html>"
    )
    return head + header + body + footer


# --------------------------------------------------------------------------- pages
def plans_table():
    rows = []
    for brand, tier, price, unit, quota, who, _key in data.PLANS:
        if price == "0":
            continue  # 免费档在正文里单独说明，不占表格行
        rows.append([brand + " " + tier, "$" + price + " " + unit, quota, who])
    return table(["品牌与档位", "官方美元价", "额度与权益要点", "适合谁"], rows,
                 caption="四家消费级订阅全档位（官方美元标价，核对于 " + data.CHECKED + "）")


def render_home():
    use_cases = "".join(
        '<a href="' + slug + '.html"><strong>' + escape(name) + "</strong><span>" + escape(text)
        + "</span><b>→</b></a>" for name, text, slug in data.HOME_USE_CASES)

    cards = "".join(
        '<a class="guide-card" href="' + a["slug"] + '.html"><div class="guide-text">'
        "<h3>" + escape(a["title"]) + "</h3><p>" + escape(a["desc"]) + "</p>"
        "<span>阅读对比 →</span></div></a>" for a in ARTICLES)

    body = (
        '<section class="hero price-hero"><div class="container">'
        "<h1>ChatGPT、Claude、Grok、Gemini 订阅怎么选？价格、额度与国内开通对比</h1>"
        '<p class="intro">结论先说：$20 档四家里，<strong>功能最全选 ChatGPT Plus，写作和编程质量选 Claude Pro，'
        "已在用 Google 生态选 Google AI Pro，要实时信息选 SuperGrok</strong>。价格几乎一样，差距在额度算法和你已有的工具链。"
        "下面的表只列官方美元价，更新日 " + data.TODAY + "。</p></div></section>"

        '<section class="container price-overview section">'
        '<div class="price-heading"><h2>四家全档位价格对比表</h2>'
        '<a href="ai-subscription-price-compare.html">看完整版，含 $20 / $100 档横评 →</a></div>'
        + plans_table()
        + '<p class="note">表中为各家<strong>官方美元标价</strong>，不含当地税费，也不是本站或任何商家的报价。'
          "免费档四家都有，但用量和模型档次受限，付费前先把免费档用到撞上限再决定。"
          "<strong>国内人民币开通价本站不维护，见 GoPlus。</strong></p></section>"

        '<section class="soft-section"><div class="container section intent-section">'
        + heading("BY USE CASE", "按用途推荐", "先确定你一周里花时间最多的那类任务，再对照这五条。")
        + '<div class="intent-grid five">' + use_cases + "</div>"
        + '<p class="intent-note">每条结论的依据都在对应的对比文章里，包括竞品的优点和各家的短板。</p></div></section>'

        '<section class="container section">'
        + heading("COMPARISONS", "对比文章", "每篇以表格为核心，注明官方来源和核对日期，结论尽量可复核。")
        + '<div class="guide-grid">' + cards + "</div>"
        + '<a class="more-link" href="guides.html">查看文章索引，含每篇适合谁看 →</a></section>'

        '<section class="soft-section"><div class="container section article" id="domestic">'
        "<h2>国内怎么开通</h2>"
        "<p>上面所有价格都是官方美元标价。官方渠道需要符合条件的境外付款方式，国内发行的信用卡经常被拒。"
        "没有境外卡时，常见路径有四条：应用商店内订阅、礼品卡、虚拟卡和第三方代充，成本、风险与售后归属各不相同，"
        '完整比较见<a href="buying-guide.html">购买渠道对比</a>。</p>'
        "<p>选择第三方代充时先问清三件事：开在你自己的账号上还是成品号、需要提交什么信息、失败怎么退款。"
        "人民币报价由商家自行定价，与官方美元价不是固定汇率关系，本站不维护这类价格。</p>"
        '<div class="actions">' + shop_link("index", "domestic_shop", "到 GoPlus 小店查看当前档位与报价") + "</div>"
        "<small>下单将前往第三方服务商页面，开通、交付与售后由该服务商负责。</small></div></section>"

        '<section class="container section article" id="method">'
        "<h2>本站口径</h2>"
        "<ol><li><strong>只写官方美元价。</strong>所有价格来自各家官方定价页，不换算人民币，不转载任何商家报价。</li>"
        "<li><strong>标注核对日期。</strong>每月 1 号核对一次，页面上写的是最近一次核对的日期，重大调整随时更新。</li>"
        '<li><strong>商业关系公开。</strong>本站为 GoPlus 提供商业导流，与 OpenAI、Anthropic、Google、xAI 无隶属关系，详见<a href="about.html">关于本站</a>。</li></ol>'
        "</section>"
    )
    schemas = schema_blocks("index", *PAGE_META["index"])
    schemas.append({"@context": "https://schema.org", "@type": "ItemList",
                    "name": "AI 订阅对比文章", "itemListElement": [
                        {"@type": "ListItem", "position": i + 1, "name": a["title"],
                         "url": BASE + a["slug"] + ".html", "description": a["desc"]}
                        for i, a in enumerate(ARTICLES)]})
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
            return "<li>" + merchant_text_link(slug, "source", title) + "</li>"
        return '<li><a href="' + url + '" rel="noopener" target="_blank">' + title + "</a></li>"

    src = ('<aside class="sources"><strong>资料来源</strong><ul>'
           + "".join(source_item(k) for k in art["sources"])
           + "</ul><small>官方价格核对日期：" + data.CHECKED
           + "。价格与额度规则可能调整，请以各家官方页面为准。</small></aside>")
    related = ('<aside class="related"><h2>继续对比</h2><div>'
               + "".join('<a href="' + s + '.html">' + escape(ART_BY_SLUG[s]["title"]) + " →</a>"
                         for s in art["related"] if s in ART_BY_SLUG)
               + "</div></aside>")
    faq_html = ('<section class="section faq-section"><h2>常见追问</h2>'
                + faq_list(art["faq"]) + "</section>") if art.get("faq") else ""
    body = (
        '<div class="container seo-breadcrumb"><a href="index.html">首页</a><span> / </span>'
        "<span>" + escape(art["title"]) + "</span></div>"
        '<article class="container article">'
        "<h1>" + escape(art["title"]) + "</h1>"
        '<p class="article-meta">更新于 ' + art["updated"] + " · 官方价格核对于 " + data.CHECKED
        + " · " + data.SITE_NAME + "</p>"
        '<p class="intro">' + art["lead"] + "</p>"
        '<p class="note">国内没有境外卡的读者：档位定下来后，人民币开通价见 '
        + shop_text_link(slug, "article_top", "GoPlus 小店") + "，本站不维护报价。</p>"
        '<nav class="article-toc" aria-label="本页目录">' + toc + "</nav>"
        + sections + faq_html
        + '<aside class="article-cta"><h2>怎么开通</h2><p>本站不维护人民币报价。确定档位后，'
          "国内开通方式与当前价格请到服务商页面确认；选第三方时先问清账号归属、所需信息与退款条件。</p>"
        + shop_link(slug, "article_end", art["cta"]) + "</aside>"
        + src + related + "</article>"
    )
    schemas = schema_blocks(slug, art["title"], art["desc"], article=art)
    if art.get("faq"):
        schemas.append(faq_schema(art["faq"]))
    return page(slug, body, schemas)


def render_guides():
    items = "".join(
        '<a href="' + a["slug"] + '.html"><h3>' + escape(a["title"]) + "</h3>"
        "<p>" + escape(a["desc"]) + "</p>"
        '<p class="intent-note">适合谁看：' + escape(a["audience"]) + " · 更新于 " + a["updated"] + "</p></a>"
        for a in ARTICLES)
    body = (
        '<div class="container seo-breadcrumb"><a href="index.html">首页</a>'
        "<span> / </span><span>对比文章索引</span></div>"
        '<section class="container section article">'
        + heading("INDEX", "AI 订阅横评与对比文章", "全部对比文章按阅读顺序排列，每篇注明适合谁看和最近更新日期。", level="h1")
        + "<p>建议的阅读顺序：先看<strong>全档位价格表</strong>确定预算区间，再按用途看跨品牌对比，"
        "最后看<strong>购买渠道对比</strong>决定怎么付款。所有价格都是官方美元标价，核对于 " + data.CHECKED
        + "；每篇文末列出官方来源，便于自己复核。</p>"
        '<div class="guide-directory">' + items + "</div>"
        '<p class="price-footnote">还没写到的对比（如 Gemini 与 ChatGPT、$20 档四家横评、年付与月付）会陆续补充，'
        '可先看<a href="faq.html">常见问题</a>里的短答案。</p></section>')
    return page("guides", body, schema_blocks("guides", *PAGE_META["guides"]))


def render_faq():
    body = (
        '<div class="container seo-breadcrumb"><a href="index.html">首页</a>'
        "<span> / </span><span>常见问题</span></div>"
        '<section class="container section faq-section article">'
        + heading("FAQ", "AI 订阅常见问题：价格、额度、付款与选购",
                  "20 个高频问题，先给可以直接用的答案，需要细节时点进对应对比页。", level="h1")
        + "<p>这一页回答的是订阅之前最常被问到的问题：多少钱、哪家值得、额度怎么算、年付划不划算、编程该订哪家、"
        "国内怎么付款、第三方代充是否安全。答案以各家官方说明和本站的对比文章为依据，官方价格核对于 "
        + data.CHECKED + "。</p>"
        + faq_list(SITE_FAQ)
        + '<p class="price-footnote">完整价格对比见'
          '<a href="ai-subscription-price-compare.html">全档位价格表</a>，'
          '开通渠道见<a href="buying-guide.html">渠道对比</a>，编程订阅见'
          '<a href="claude-code-vs-codex.html">Claude Code 与 Codex 对比</a>。</p></section>')
    schemas = schema_blocks("faq", *PAGE_META["faq"])
    schemas.append(faq_schema(SITE_FAQ))
    return page("faq", body, schemas)


STATIC_PAGES = {
    "about": (
        "<h2>本站做什么</h2><p>本站只做一件事：<strong>把 ChatGPT、Claude、Gemini、Grok 以及主流 AI 编程工具的订阅放在一起比</strong>。"
        "比价格、比额度口径、比适合谁、比国内用户怎么开通。目标读者是准备第一次订 AI、或者正在考虑换一家、升一档的人。</p>"
        "<p>本站不做单品充值页，不写单一产品的付款排查教程，也不提供跨区订阅或绕过地区限制的方法。"
        "这些内容要么属于各家官方帮助中心，要么属于服务商自己的站点。</p>"
        "<h2>比价口径</h2>"
        "<p><strong>价格只写官方美元标价。</strong>所有价格取自各家官方定价页（OpenAI、Anthropic、Google、xAI、Cursor、GitHub 等），"
        "按官方标价原样记录，不含当地税费，不做汇率换算，也不转载任何商家的人民币报价。"
        "一个档位在官方页面上有多种计费方式时（如 Claude Pro 的月付与年付），两种都列出并注明。</p>"
        "<p><strong>额度只写计算方式，不写具体条数。</strong>各家对额度的描述口径不同：Claude 按滚动窗口，ChatGPT 按模型和功能分别限制，"
        "国内 Coding Plan 按积分或请求次数。官方会根据容量随时调整上限，而且不公布可长期依赖的数字，"
        "所以本站只描述「怎么算」，并引用官方的倍数说法（如「约为 Pro 的 5 倍用量」），不写任何「每 3 小时多少条」之类的具体数字。</p>"
        "<p><strong>能力对比写两面。</strong>每篇跨品牌对比都要同时写出各家的强项和短板，包括国内方案价格低、海外方案质量稳这类不利于导流的事实。"
        "只写一家好处的页面没有参考价值，也不会被当成可信的对比。</p>"
        "<p><strong>核对频率。</strong>官方价格每月 1 号核对一次，核对日期写在每页的表格说明和页脚；"
        "任何一家发布新模型或调价后 48 小时内更新价格表和对应对比文章。每篇文章的「更新于」日期表示最近一次实质内容修改，"
        "不会为了显得新而只改日期不改内容。</p>"
        "<p><strong>为什么不写人民币价格。</strong>人民币开通价是第三方服务商的报价，由商家自行定价，随成本和交付形态变动，"
        "与官方美元价不是固定汇率关系。写在本站上会很快过期，也容易被误当成官方价格。需要人民币报价时请直接到服务商页面查看当前价格。</p>"
        "<h2>商业关系披露</h2><p>本站为 GoPlus 提供商业导流：页面中的「国内开通」入口会跳转到该第三方服务商及其小店页面，"
        "并带有来源标识参数（utm_campaign=ai66man_compare）。本站不销售、不开通任何订阅，也不收取任何款项；"
        "实际的开通、交付、退款与售后全部由该服务商负责，本站无法查询订单。</p>"
        "<p>本站与 OpenAI、Anthropic、Google、xAI、Cursor、GitHub 均无隶属、合作或授权关系，也不是任何一家的官方网站。"
        "页面上引用的第三方服务说明均来自其公开页面，不构成本站的承诺。</p>"
        "<h2>不做什么</h2><p>不提供跨区订阅或绕过地区限制的方法；不提供任何成功率、到账时间或质保承诺；"
        "不编造订单量、用户评价或成功案例；不收集任何账号凭据或支付信息。</p>"
        "<h2>怎么报错</h2><p>发现价格过期、额度描述与官方不符、对比结论有误，可在 "
        '<a href="' + data.REPO + '/issues" rel="noopener" target="_blank">GitHub 仓库 Issues</a> '
        "反馈，请附页面地址、需要修正的表述和可核验的官方来源。确认后会在 7 天内修正并更新该页的「更新于」日期。"
        "请不要在反馈中提交订单、账号或支付资料。</p>"),
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
        "<h2>第三方交易</h2><p>本站不销售任何订阅，也不收款。通过本站进入第三方服务商后，"
        "交易、交付、退款与售后均由其负责，与本站无关。本站展示的第三方服务说明引自其公开页面，不构成本站的承诺。</p>"
        "<h2>商标与隶属关系</h2><p>ChatGPT、Claude、Gemini、Grok 等名称归各自权利人所有。"
        "本站与 OpenAI、Anthropic、Google、xAI 均无隶属、合作或授权关系。</p>"),
}


def render_static(slug):
    title, _ = PAGE_META[slug]
    body = ('<div class="container seo-breadcrumb"><a href="index.html">首页</a>'
            "<span> / </span><span>" + escape(title) + "</span></div>"
            '<section class="container section article"><h1>' + escape(title) + "</h1>"
            '<p class="article-meta">更新于 ' + page_date(slug) + "</p>"
            + STATIC_PAGES[slug] + "</section>")
    return page(slug, body, schema_blocks(slug, *PAGE_META[slug]))


def render_404():
    body = ('<section class="container section article"><h1>页面不存在</h1>'
            "<p>这个地址不存在，或者对应的页面已经合并到新的对比文章里。</p>"
            '<p><a class="button" href="' + BASE + '">回到首页</a></p></section>')
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

    written = []  # (slug, filename)
    (OUT / "index.html").write_text(render_home(), encoding="utf-8")
    written.append(("index", "index.html"))
    for art in ARTICLES:
        (OUT / (art["slug"] + ".html")).write_text(render_article(art), encoding="utf-8")
        written.append((art["slug"], art["slug"] + ".html"))
    (OUT / "guides.html").write_text(render_guides(), encoding="utf-8")
    written.append(("guides", "guides.html"))
    (OUT / "faq.html").write_text(render_faq(), encoding="utf-8")
    written.append(("faq", "faq.html"))
    for slug in STATIC_PAGES:
        (OUT / (slug + ".html")).write_text(render_static(slug), encoding="utf-8")
        written.append((slug, slug + ".html"))
    (OUT / "404.html").write_text(render_404(), encoding="utf-8")
    for slug, (key, label) in REDIRECTS.items():
        (OUT / (slug + ".html")).write_text(render_redirect(slug, key, label), encoding="utf-8")

    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>',
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for slug, name in written:
        url = BASE + ("" if name == "index.html" else name)
        sitemap.append("  <url><loc>" + url + "</loc><lastmod>" + page_date(slug) + "</lastmod></url>")
    sitemap.append("</urlset>")
    (OUT / "sitemap.xml").write_text("\n".join(sitemap) + "\n", encoding="utf-8")
    (OUT / "robots.txt").write_text(
        "# GitHub project deployment: crawlers read https://ai66man.github.io/robots.txt,\n"
        "# not this project-path file. Submit the sitemap in Search Console.\n"
        "User-agent: *\nAllow: /\nSitemap: " + BASE + "sitemap.xml\n", encoding="utf-8")
    (OUT / ".nojekyll").write_text("", encoding="utf-8")
    print("Built " + str(len(written)) + " indexable pages, "
          + str(len(REDIRECTS)) + " redirects, 404 and sitemap.")


if __name__ == "__main__":
    main()
