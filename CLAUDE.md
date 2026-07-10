# CLAUDE.md

## Project Overview
AI News Bot — a fully local, free RAG chatbot that answers questions about current AI news. No paid APIs, no cloud dependencies except free RSS feeds.

## Hard Constraints
- Everything must run locally. Never introduce a paid API, cloud LLM, or hosted vector DB.
- LLM = Ollama only (local). Do not suggest OpenAI/Anthropic/Gemini API calls for the chatbot itself.
- Embeddings = sentence-transformers, run on CPU locally. No hosted embedding APIs.
- Vector DB = ChromaDB, persisted to local disk (`./chroma_db`).
- News source = free RSS feeds only. No paid news APIs (e.g. NewsAPI.org paid tier).
- UI = Streamlit, runs on localhost only.

## Architecture
1. `fetch_news.py` — pulls + dedupes RSS articles → `news_cache.json`
2. `news_scheduler.py` — refreshes cache every 30 min in background
3. `vectorstore.py` — embeds articles, stores/queries ChromaDB
4. `chatbot.py` — RAG: retrieve top-k chunks → build prompt → call Ollama → return answer + sources
5. `app.py` — Streamlit chat UI, session-state history, source citations, manual refresh button

## Coding Conventions
- Python 3.10+, type hints where practical
- Keep functions small and single-purpose
- All file I/O should fail gracefully (try/except, no silent crashes)
- Config values (RSS feed list, model name, chunk size, top-k) go in a single `config.py`, not hardcoded across files
- Log errors to console with clear prefixes, e.g. `[fetch_news] Failed to parse feed: ...`

## When Adding Features
- Prefer editing existing files over creating new ones unless a new concern is being introduced
- If adding a new RSS source, add it to `config.py`'s `RSS_FEEDS` list, not inline in `fetch_news.py`
- If swapping the LLM model, update `config.py`'s `OLLAMA_MODEL` — don't hardcode model names in `chatbot.py`
- Always test that the app still runs fully offline (except RSS fetch) after changes

## Known Constraints / Gotchas
- Ollama must be running on `localhost:11434` before `chatbot.py` is called
- ChromaDB persistence directory (`./chroma_db`) must exist before first write
- Some RSS feeds occasionally return malformed XML — always wrap feedparser calls in try/except
- Large models (8B+) may be slow on CPU-only machines — default to a smaller model if no GPU detected

## Commands
- Run full app: `bash run.sh`
- Run news fetch manually: `python fetch_news.py`
- Rebuild vector index: `python vectorstore.py --reindex`
- Run Streamlit only: `streamlit run app.py`