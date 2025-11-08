# tools/fetch.py
import httpx, re, time, json, itertools
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from urllib.parse import urlencode
import yaml, random

HEADERS = {"User-Agent":"Mozilla/5.0 (agentic-cop30 demo)"}

def _google_like(query, limit=8):
    # simple search via DuckDuckGo HTML (no API key); swap for real APIs in prod
    q = {"q": query}
    url = f"https://html.duckduckgo.com/html/?{urlencode(q)}"
    html = httpx.get(url, headers=HEADERS, timeout=30).text
    soup = BeautifulSoup(html, "lxml")
    links = []
    for a in soup.select("a.result__a")[:limit]:
        href = a.get("href")
        if href and href.startswith("http"):
            links.append(href)
    return links

def _get(url):
    for attempt in range(3):
        try:
            r = httpx.get(url, headers=HEADERS, timeout=30, follow_redirects=True)
            if r.status_code == 200 and "text/html" in r.headers.get("content-type",""):
                return r.text
        except Exception:
            time.sleep(1.5 * (attempt+1))
    return ""

def search_and_fetch(topic_yaml_path: str):
    cfg = yaml.safe_load(open(topic_yaml_path, "r", encoding="utf-8"))
    urls = set(cfg.get("sources", []))
    for q in cfg.get("queries", []):
        for u in _google_like(q, limit=6):
            urls.add(u)
    pages = []
    for url in list(urls)[: cfg.get("max_links", 25)]:
        html = _get(url)
        if not html: 
            continue
        pages.append({
            "url": url,
            "html": html,
            "source": url.split("/")[2],
            "title": None,
            "published": None,
            "min_words": cfg.get("min_word_count", 120),
        })
    return pages
