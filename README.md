# agentic-cop30

A small demo that fetches recent web content for a topic (COP30), ranks and deduplicates articles, and uses an LLM to produce a concise daily brief.

## Quick start

1. Install dependencies (from pyproject.toml):
```sh
pip install .
# or
pip install -r <your-favorite-requirements-list>
```

2. Provide an OpenAI API key in `.env` (or set `OPENAI_API_KEY` in your environment). See [.env](.env).

3. Run the demo:
```sh
python main.py
```

The script loads the topic config at [topics/cop30.yaml](topics/cop30.yaml) by default and prints a short daily brief.

## Project layout

- [main.py](main.py) — entrypoint with `run`.
- [graph.py](graph.py) — orchestration graph built from [`graph.State`](graph.py) and [`graph.build_graph`](graph.py).
- agents/
  - [agents/memory.py](agents/memory.py) — persistent seen URL memory (`agents.memory.Memory`).
  - [agents/planner.py](agents/planner.py) — lightweight task planner (`agents.planner.plan`).
  - [agents/web_searcher.py](agents/web_searcher.py) — search/fetch + parse + rank (`agents.web_searcher.gather`).
  - [agents/writer.py](agents/writer.py) — composes LLM prompt and calls OpenAI (`agents.writer.write_brief`).
- tools/
  - [tools/fetch.py](tools/fetch.py) — web search and fetch (`tools.fetch.search_and_fetch`).
  - [tools/parse.py](tools/parse.py) — HTML -> text (`tools.parse.to_text`).
  - [tools/rank.py](tools/rank.py) — scoring and dedupe (`tools.rank.rank_and_dedupe`).
- [topics/cop30.yaml](topics/cop30.yaml) — topic configuration (queries, sources, cutoffs).
- [pyproject.toml](pyproject.toml) — packaging & dependencies.

## Notes & customization

- The demo uses HTML scraping (DuckDuckGo) in [tools/fetch.py](tools/fetch.py). Swap to a proper search API for production.
- LLM call is in [agents/writer.py](agents/writer.py). Replace model or client as needed; ensure `OPENAI_API_KEY` is set.
- Memory is a tiny SQLite DB stored as `memory.sqlite` by default (see [agents/memory.py](agents/memory.py)).

## License

Demo code — adapt as needed.