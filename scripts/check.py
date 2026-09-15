# -*- coding: utf-8 -*-
"""Pre-publish checks for the comparison site: links, metadata, schema, sitemap,
redirect hygiene, outbound attribution and word counts."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote, parse_qs
import json
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
BASE = "https://ai66man.github.io/chatgpt-plus-sub/"
MIN_CHARS = 1500  # 汉字下限，正文页


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids = set(); self.refs = []; self.h1 = 0; self.outbound = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if "id" in d:
            self.ids.add(d["id"])
        if tag == "h1":
            self.h1 += 1
        if tag in ("a", "link", "img", "script"):
            value = d.get("href", d.get("src"))
            if value:
                self.refs.append(value)
        if tag == "img":
            assert d.get("alt"), "image needs alt"
        if tag == "a" and "goplus.pro" in (d.get("href") or ""):
            self.outbound.append(d)


static_files = {p.name for p in (ROOT / "static").iterdir() if p.is_file()}
for name in static_files:
    assert (DOCS / name).read_bytes() == (ROOT / "static" / name).read_bytes(), \
        "Static verification file changed"

html_files = [p for p in DOCS.glob("*.html") if p.name not in static_files]
redirects, content = {}, {}
for p in html_files:
    text = p.read_text(encoding="utf-8")
    if 'http-equiv="refresh"' in text:
        redirects[p] = text
    else:
        content[p] = text

# ---------- redirect pages
for p, text in redirects.items():
    assert "noindex" in text, (p.name, "redirect must be noindex")
    target = re.search(r'http-equiv="refresh" content="0; url=([^"]+)"', text).group(1)
    canonical = re.findall(r'<link rel="canonical" href="([^"]+)"', text)
    assert canonical == [target.replace("&", "&amp;")] or canonical == [target], \
        (p.name, "canonical must match refresh target", canonical)
    assert "utm_campaign=ai66man_compare" in text, (p.name, "redirect needs campaign tag")

# ---------- content pages
pages = {p: Page(t) for p, t in content.items()}
titles, descriptions, indexed = set(), set(), set()
inbound = {p.name: 0 for p in content}
for p, text in content.items():
    data = pages[p]
    assert data.h1 == 1, (p.name, "heading")
    assert "/Users/" not in text, (p.name, "private path leaked")

    title = re.search(r"<title>(.*?)</title>", text).group(1)
    desc = re.search(r'<meta name="description" content="([^"]+)"', text).group(1)
    assert title not in titles, (p.name, "duplicate title")
    assert desc not in descriptions, (p.name, "duplicate description")
    titles.add(title); descriptions.add(desc)

    robots = re.findall(r'<meta name="robots" content="([^"]+)"', text)
    assert len(robots) == 1, (p.name, "robots")
    canonical = re.findall(r'<link rel="canonical" href="([^"]+)"', text)
    expected = BASE + ("" if p.stem == "index" else p.name)
    if p.stem == "404":
        assert not canonical, (p.name, "404 must not be canonical")
    else:
        assert canonical == [expected], (p.name, "canonical", canonical)
    if "noindex" not in robots[0]:
        indexed.add(expected)

    assert "googletagmanager.com/gtag/js?id=G-" in text, (p.name, "GA4 missing")
    assert "outbound_click" in text, (p.name, "outbound_click event missing")

    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', text, re.S):
        schema = json.loads(block)
        assert schema["@type"] not in ("Product", "AggregateRating", "Review"), p.name

    # outbound attribution
    for a in data.outbound:
        q = parse_qs(urlsplit(a["href"].replace("&amp;", "&")).query)
        assert q.get("utm_campaign") == ["ai66man_compare"], (p.name, "missing utm_campaign", a)
        assert q.get("utm_content"), (p.name, "missing utm_content", a)
        assert "sponsored" in (a.get("rel") or ""), (p.name, "outbound needs rel=sponsored", a)

    # local link targets
    for ref in data.refs:
        u = urlsplit(ref)
        if u.scheme or u.netloc:
            continue
        target = (p.parent / unquote(u.path)).resolve() if u.path else p
        assert target.exists(), (p.name, ref, "missing file")
        if u.fragment and target in pages:
            assert unquote(u.fragment) in pages[target].ids, (p.name, ref, "missing anchor")
        if u.path in inbound and u.path != p.name:
            inbound[u.path] += 1

# every content page is reachable
assert all(c > 0 for n, c in inbound.items() if n != "404.html"), inbound

# no cross-account linking: A 站与 B 站不互链
for p, text in {**content, **redirects}.items():
    assert "imi0801.github.io" not in text, (p.name, "cross-account link found")

# sitemap
sitemap = {n.text for n in ET.parse(DOCS / "sitemap.xml").findall(".//{*}loc")}
assert sitemap == indexed, ("sitemap mismatch", sitemap ^ indexed)
assert all("lastmod" in ET.tostring(u, encoding="unicode")
           for u in ET.parse(DOCS / "sitemap.xml").findall(".//{*}url")), "lastmod missing"
for p in redirects:
    assert BASE + p.name not in sitemap, (p.name, "redirect must stay out of sitemap")

# word counts for the comparison articles
thin = []
for p, text in content.items():
    if p.stem in ("404", "privacy", "terms", "about", "guides"):
        continue
    body = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", text, flags=re.S)
    chars = len(re.findall(r"[一-鿿]", re.sub(r"<[^>]+>", "", body)))
    if chars < MIN_CHARS:
        thin.append((p.name, chars))
if thin:
    print("WARN thin pages:", thin, file=sys.stderr)

print("PASS: " + str(len(content)) + " content pages, " + str(len(redirects))
      + " redirects, " + str(len(indexed)) + " indexable URLs; links, anchors, metadata, "
      "JSON-LD, GA4, outbound attribution, sitemap and cross-site rules.")
