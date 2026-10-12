#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Submit new or changed sitemap URLs to IndexNow (Bing and partners).

Reads docs/sitemap.xml, compares each URL's lastmod with scripts/.indexnow-state.json,
and POSTs the changed set to https://api.indexnow.org/indexnow. The key file lives in
static/<key>.txt so the builder copies it to the site root on every build.

Usage:
  python3 scripts/indexnow.py            # submit changed URLs
  python3 scripts/indexnow.py --all      # submit every sitemap URL
  python3 scripts/indexnow.py --dry-run  # show what would be sent
Standard library only.
"""
from pathlib import Path
import json
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
SITEMAP = ROOT / "docs" / "sitemap.xml"
STATE = ROOT / "scripts" / ".indexnow-state.json"
ENDPOINT = "https://api.indexnow.org/indexnow"
BASE = "https://ai66man.github.io/chatgpt-plus-sub/"


def find_key():
    keys = [p for p in (ROOT / "static").glob("*.txt")
            if len(p.stem) == 32 and all(c in "0123456789abcdef" for c in p.stem)
            and p.read_text().strip() == p.stem]
    if len(keys) != 1:
        sys.exit("expected exactly one IndexNow key file in static/, found " + str(len(keys)))
    return keys[0].stem


def read_sitemap():
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    out = {}
    for url in ET.parse(SITEMAP).getroot().findall("s:url", ns):
        loc = url.find("s:loc", ns).text.strip()
        mod = url.find("s:lastmod", ns)
        out[loc] = mod.text.strip() if mod is not None else ""
    return out


def main(argv):
    dry = "--dry-run" in argv
    everything = "--all" in argv
    key = find_key()
    current = read_sitemap()
    state = json.loads(STATE.read_text()) if STATE.exists() else {}
    changed = [u for u, m in current.items() if everything or state.get(u) != m]
    if not changed:
        print("IndexNow: nothing changed since last submission.")
        return 0
    payload = {
        "host": "ai66man.github.io",
        "key": key,
        "keyLocation": BASE + key + ".txt",
        "urlList": changed,
    }
    print("IndexNow: " + str(len(changed)) + " URL(s)" + (" [dry-run]" if dry else ""))
    for u in changed:
        print("  " + u)
    if dry:
        return 0
    req = urllib.request.Request(
        ENDPOINT, data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8",
                 "User-Agent": "chatgpt-plus-sub-indexnow/1.0"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            status = resp.status
    except urllib.error.HTTPError as e:
        status = e.code
        print("IndexNow: HTTP " + str(status) + " " + e.read().decode("utf-8", "replace")[:300])
    except urllib.error.URLError as e:
        print("IndexNow: network error " + str(e.reason))
        return 1
    if status in (200, 202):
        print("IndexNow: accepted (HTTP " + str(status) + ")")
        for u in changed:
            state[u] = current[u]
        STATE.write_text(json.dumps(state, indent=1, sort_keys=True) + "\n")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
