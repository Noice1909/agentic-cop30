import requests
import json
import os
from datetime import date

SYSTEM = """You write concise, neutral daily briefs.
- Keep it under 300 words with 4–6 bullets.
- Cite sources inline like [1], [2] mapping to URLs at the end.
- Include exact dates (e.g., "Nov 10, 2025").
- Prefer official + wire sources.
"""

def write_brief(topic, docs, memory):
    urls = [d["url"] for d in docs]
    sources_block = "\n".join(f"[{i+1}] {u}" for i, u in enumerate(urls[:10]))

    context = "\n\n".join(
        f"Title: {d['title'] or d['url']}\nSource: {d['source']}\nURL: {d['url']}\n---\n{d['text'][:2000]}"
        for d in docs[:8]
    )

    user_prompt = f"""Topic: {topic}
    Date: {date.today().isoformat()}

    Write a daily brief. Use only facts present in the context below; if unsure, say so.
    {sources_block}

    === CONTEXT START ===
    {context}
    === CONTEXT END ===
    """

    payload = {
        "model": "llama3.1:8b",
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": user_prompt},
        ],
        "stream": False,
        "temperature": 0.2,
    }

    r = requests.post("http://localhost:11434/v1/chat/completions", json=payload)
    data = r.json()

    return data["choices"][0]["message"]["content"]
