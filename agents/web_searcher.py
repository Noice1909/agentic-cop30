import time, hashlib
from tools.fetch import search_and_fetch
from tools.rank import rank_and_dedupe
from tools.parse import to_text

def gather(tasks, memory):
    # 1) search + fetch from queries and seed sources
    raw_pages = search_and_fetch("topics/cop30.yaml")
    # 2) parse
    docs = []
    for p in raw_pages:
        text = to_text(p["html"])
        if len(text.split()) < p["min_words"]: 
            continue
        h = hashlib.sha256(p["url"].encode()).hexdigest()
        if memory.seen(h): 
            continue
        docs.append({
            "url": p["url"],
            "title": p.get("title") or p["url"],
            "published": p.get("published"),
            "source": p.get("source"),
            "text": text,
            "hash": h
        })
    # 3) rank + dedupe
    return rank_and_dedupe(docs)
