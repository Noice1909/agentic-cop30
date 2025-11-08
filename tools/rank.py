# tools/rank.py
from rapidfuzz import fuzz

def rank_and_dedupe(docs):
    # score authority by domain and novelty by length
    domain_score = {
        "unfccc.int": 0.9, "cop30.br": 0.85, "un.org": 0.85,
        "reuters.com": 0.9, "apnews.com": 0.88, "ipcc.ch": 0.85
    }
    for d in docs:
        base = domain_score.get(d["source"], 0.6)
        novelty = min(len(d["text"]) / 5000, 1.0)
        d["score"] = 0.5*base + 0.5*novelty
    # simple near-duplicate removal by title/text similarity
    keep = []
    for d in sorted(docs, key=lambda x: x["score"], reverse=True):
        if any(fuzz.partial_ratio(d["text"][:2000], k["text"][:2000]) > 95 for k in keep):
            continue
        keep.append(d)
    return keep[:12]
