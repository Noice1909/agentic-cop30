import os, textwrap
from datetime import date
from openai import OpenAI

SYSTEM = """You write concise, neutral daily briefs.
- Keep it under 300 words with 4–6 bullets.
- Cite sources inline like [1], [2] mapping to URLs at the end.
- Include exact dates (e.g., "Nov 10, 2025") for time clarity.
- Prefer official + wire sources.
"""

def write_brief(topic, docs, memory):
    urls = [d["url"] for d in docs]
    sources_block = "\n".join(f"[{i+1}] {u}" for i, u in enumerate(urls[:10]))
    # Compose context
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

    # LLM call (swap to your provider of choice)
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    resp = client.chat.completions.create(
        model="gpt-4o-mini",  # fast & cheap; use any model you like
        messages=[{"role":"system","content":SYSTEM},
                  {"role":"user","content":user_prompt}],
        temperature=0.2,
    )
    return resp.choices[0].message.content.strip()
