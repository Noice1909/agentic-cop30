# agentic-cop30

A small demo that fetches recent web content for a topic (COP30), ranks and deduplicates articles, and uses an LLM to produce a concise daily brief.

## Quick start

1. Install dependencies:
```sh
pip install .
# or for development
pip install -e .
```

2. Configure environment variables (optional):
- By default the writer posts to a local LLM HTTP server at `http://localhost:11434/v1/chat/completions` with model string `"llama3.1:8b"`.
- To use a local llama-cpp model via python bindings:
  - Set `USE_LOCAL_LLAMA=1`
  - Set `LLAMA_MODEL_PATH=C:\path\to\model.ggml`
  - Install: `pip install llama-cpp-python` and ensure a compatible model file.
- To use OpenAI instead, set `OPENAI_API_KEY` in your environment or `.env`.

3. Run the demo:
```sh
python main.py
```
The script loads the topic config at `topics/cop30.yaml` by default and prints a short daily brief.

## Project layout

- `main.py` — entrypoint with `run`.
- `graph.py` — orchestration graph built from `graph.State` and `graph.build_graph`.
- agents/
  - `agents/memory.py` — persistent seen URL memory (`agents.memory.Memory`).
  - `agents/planner.py` — lightweight task planner (`agents.planner.plan`).
  - `agents/web_searcher.py` — search/fetch + parse + rank (`agents.web_searcher.gather`).
  - `agents/writer.py` — composes LLM prompt and supports:
    - local HTTP LLM endpoint (default at `http://localhost:11434`),
    - optional llama-cpp-python local model (`USE_LOCAL_LLAMA=1` + `LLAMA_MODEL_PATH`),
    - or OpenAI (if `OPENAI_API_KEY` is set).
- tools/
  - `tools/fetch.py` — web search and fetch (`tools.fetch.search_and_fetch`).
  - `tools/parse.py` — HTML -> text (`tools.parse.to_text`).
  - `tools/rank.py` — scoring and dedupe (`tools.rank.rank_and_dedupe`).
- `topics/cop30.yaml` — topic configuration (queries, sources, cutoffs).
- `pyproject.toml` — packaging & dependencies.
- `.env` — optional environment variables.

## Notes & customization

- The demo uses HTML scraping (DuckDuckGo) in `tools/fetch.py`. Swap to a search API for production.
- The writer can call a local HTTP LLM, use llama-cpp-python for local models, or use OpenAI. Adjust `agents/writer.py` to change backends or models.
- Memory is a tiny SQLite DB stored as `memory.sqlite` by default (see `agents/memory.py`).
- Tune topic settings in `topics/cop30.yaml` (max_links, queries, sources, cutoffs).

## How it runs (high-level)

1. `main.run` loads topic config and creates `agents.memory.Memory`.
2. `graph.build_graph` orchestrates nodes:
   - `agents.planner.plan` → tasks
   - `agents.web_searcher.gather` → uses `tools.fetch.search_and_fetch`, `tools.parse.to_text`, `tools.rank.rank_and_dedupe`
   - `agents.writer.write_brief` → generates the brief via the selected LLM backend and updates memory
3. Final brief prints to stdout.

## License

Demo code — adapt as needed.