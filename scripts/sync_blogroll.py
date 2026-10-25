#!/usr/bin/env python3
"""Keep blogroll/index.md and blogroll/index.html listing the same links.

  --from md    index.md is the source: new URLs are added to the HTML with a
               fetched title and favicon, removed URLs are dropped.
  --from html  index.html is the source: index.md is rewritten from it.

A line in index.md may be a bare URL or [Custom title](URL). Featured status
and edited titles live only in the HTML and are kept across syncs.
"""
import argparse
import html
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MD = ROOT / "blogroll" / "index.md"
HTML = ROOT / "blogroll" / "index.html"
FAVICONS = ROOT / "favicons"

UA = "Mozilla/5.0 (compatible; threadlocked-blogroll-sync)"
LIST_RE = re.compile(r'(<ul id="blogroll">\n)(.*?)(\n    </ul>)', re.S)
ITEM_RE = re.compile(r'^\s*<li[^>]*><a href="([^"]+)">.*</li>\s*$')
MD_LINK_RE = re.compile(r"^\[(.+)\]\((\S+)\)$")
ICON = ('<img class="link-icon" src="../favicons/{}" width="16" height="16" '
        'alt="" aria-hidden="true" loading="lazy" decoding="async">')


def read_md():
    """Return [(url, title_or_None)] in file order."""
    entries = []
    for line in MD.read_text().splitlines():
        line = line.strip().lstrip("-* ").strip()
        if not line:
            continue
        m = MD_LINK_RE.match(line)
        entries.append((m.group(2), m.group(1)) if m else (line, None))
    return entries


def read_html():
    """Return (page text, list match, {url: <li> line}) with insertion order."""
    page = HTML.read_text()
    match = LIST_RE.search(page)
    if not match:
        sys.exit(f"{HTML}: could not find <ul id=\"blogroll\">")
    items = {}
    for line in match.group(2).splitlines():
        m = ITEM_RE.match(line)
        if not m:
            sys.exit(f"{HTML}: unexpected line in blogroll list:\n{line}")
        items[html.unescape(m.group(1))] = line
    return page, match, items


def fetch(url, limit=None):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.read(limit)


def fetch_title(url):
    try:
        page = fetch(url, 512 * 1024).decode("utf-8", "replace")
    except (urllib.error.URLError, TimeoutError, ValueError) as e:
        print(f"warning: could not fetch {url}: {e}", file=sys.stderr)
        return url
    for pattern in (r'<meta[^>]+property="og:title"[^>]+content="([^"]*)"',
                    r"<title[^>]*>(.*?)</title>"):
        m = re.search(pattern, page, re.I | re.S)
        if m and m.group(1).strip():
            return " ".join(html.unescape(m.group(1)).split())
    print(f"warning: no title found for {url}", file=sys.stderr)
    return url


def favicon_for(url):
    host = urllib.parse.urlsplit(url).hostname
    for name in (f"{host}.png", f"{host}.svg"):
        if (FAVICONS / name).exists():
            return name
    api = f"https://www.google.com/s2/favicons?domain={host}&sz=32"
    try:
        (FAVICONS / f"{host}.png").write_bytes(fetch(api))
        return f"{host}.png"
    except (urllib.error.URLError, TimeoutError) as e:
        print(f"warning: no favicon for {host} ({e}); using link.svg", file=sys.stderr)
        return "link.svg"


def new_item(url, title):
    title = title or fetch_title(url)
    print(f"adding: {title} <{url}>")
    return (f'      <li><a href="{html.escape(url)}">{ICON.format(favicon_for(url))}'
            f"{html.escape(title, quote=False)}</a></li>")


def md_to_html():
    page, match, items = read_html()
    entries = read_md()
    wanted = {url for url, _ in entries}
    for url in items:
        if url not in wanted:
            print(f"removing: {url}")
    lines = [items.get(url) or new_item(url, title) for url, title in entries]
    body = "\n".join(lines)
    if body != match.group(2):
        HTML.write_text(page[:match.start(2)] + body + page[match.end(2):])


def html_to_md():
    _, _, items = read_html()
    custom = {url: f"[{title}]({url})" for url, title in read_md() if title}
    text = "\n\n".join(custom.get(url, url) for url in items) + "\n"
    if text != MD.read_text():
        MD.write_text(text)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--from", dest="source", choices=["md", "html"], required=True)
    args = parser.parse_args()
    md_to_html() if args.source == "md" else html_to_md()
