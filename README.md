# 📰 AI News Bot (100% Local RAG Pipeline)

An intelligent Retrieval-Augmented Generation (RAG) chatbot that pulls tech news from free public RSS feeds, indexes documents into a local vector database, and enables offline synthesis and chatting using a completely open-source, local large language model (LLM).

## 🔒 Privacy & Architecture Highlights
* **Zero External API Dependencies:** No OpenAI, Anthropic, or cloud service keys are needed.
* **100% Local Processing:** Embeddings, vector storage, and model execution run natively on your machine's hardware.
* **Fully Offline-Capable:** Once your initial model files are pulled down and the scraper fetches text news items, the entire system operates with your network adapter fully disconnected.

---

## 🛠️ The Local Stack
| Component | Technology | Footprint / Details |
| :--- | :--- | :--- |
| **Frontend UI** | `Streamlit` | Locally hosted interactive web interface (`localhost:8501`) |
| **Local LLM Server** | `Ollama` | System-level local model runtime host (`localhost:11434`) |
| **LLM Model** | `Llama 3 (8B)` | Meta's open-weights model optimized for local inference |
| **Embedding Engine** | `Sentence-Transformers` | `all-MiniLM-L6-v2` (Runs entirely on CPU; ~90MB footprint) |
| **Vector Database** | `ChromaDB` | Persistent file-based embedded vector store (`./chroma_db`) |
| **Automation** | `schedule` | Lightweight background thread routine |

---

## 🚀 Step-by-Step Setup Instructions

### 1. Prerequisite: Install Ollama Natively
Before configuring Python, install Ollama on your Windows operating system:
1. Open PowerShell and download Ollama via Windows Package Manager:
   ```powershell
   winget install Ollama.Ollama