# AI News Bot 🤖📰

A fully local, 100% free chatbot that fetches, indexes, and answers questions about the latest AI news — using RAG (Retrieval-Augmented Generation) with a locally-run LLM.

No API keys. No cloud services. No paid subscriptions.

## Stack
- **LLM**: [Ollama](https://ollama.com) (llama3.1:8b / mistral:7b / phi3:mini)
- **Embeddings**: sentence-transformers (all-MiniLM-L6-v2)
- **Vector DB**: ChromaDB (local, persisted to disk)
- **News source**: Free RSS feeds (TechCrunch, VentureBeat, MIT Tech Review, ArXiv, The Verge, Google News)
- **UI**: Streamlit

## Prerequisites
- Python 3.10+
- [Ollama](https://ollama.com) installed
- ~8GB free RAM (for 7-8B models) or use `phi3:mini`/`qwen2:1.5b` for lighter setups

## Setup

```bash
# 1. Clone the repo
git clone https://github.com/<your-username>/ai-news-bot.git
cd ai-news-bot

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Pull a local LLM via Ollama
ollama pull llama3.1:8b

# 5. Run everything
bash run.sh      # or run.bat on Windows
```

The app will open at `http://localhost:8501`.

## Project Structure
ai-news-bot/
├── fetch_news.py       # Pulls AI news from free RSS feeds
├── vectorstore.py       # Embeds + stores news in local ChromaDB
├── chatbot.py            # RAG pipeline using local Ollama LLM
├── app.py                    # Streamlit chat UI
├── news_scheduler.py  # Background auto-refresh (every 30 min)
├── run.sh / run.bat
├── requirements.txt
└── CLAUDE.md

## How It Works
1. RSS feeds are fetched and cached locally (`news_cache.json`)
2. Articles are embedded locally and stored in ChromaDB
3. User asks a question in the Streamlit UI
4. Top-5 relevant articles are retrieved and passed as context to the local LLM
5. Ollama generates an answer with cited sources

## Cost
$0. Everything runs on your machine except the RSS fetch (which is free, no key required).

## License
MIT