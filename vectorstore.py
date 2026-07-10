import json
import os
import chromadb
from chromadb.utils import embedding_functions

# Configuration
CHROMA_DATA_PATH = "./chroma_db"
COLLECTION_NAME = "ai_news_collection"
CACHE_FILE = "news_cache.json"

# 1. Initialize local persistent client (No cloud, saves to disk)
client = chromadb.PersistentClient(path=CHROMA_DATA_PATH)

# 2. Set up the local sentence-transformer model (Runs on CPU, free)
# Chroma will download this model automatically the first time it runs.
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

def get_or_create_collection():
    """Retrieves or creates the Chroma collection with our local embedding function."""
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=sentence_transformer_ef
    )

def load_news_cache():
    """Loads the deduplicated news from the local JSON cache."""
    if not os.path.exists(CACHE_FILE):
        print(f"Warning: {CACHE_FILE} not found. Run fetch_news.py first.")
        return []
    
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print("Error: JSON cache is empty or corrupted.")
            return []

def reindex_news():
    """
    Reads news_cache.json, generates embeddings, and upserts them to ChromaDB.
    Safe to run repeatedly; it uses the URL as the ID to overwrite/ignore duplicates.
    """
    articles = load_news_cache()
    if not articles:
        return 0

    collection = get_or_create_collection()
    
    documents = []
    metadatas = []
    ids = []

    for article in articles:
        # Create a rich text representation for the embedding model to digest
        text_to_embed = f"Title: {article['title']}\nSummary: {article['summary']}"
        documents.append(text_to_embed)
        
        # Store metadata for filtering and citation in the UI
        metadatas.append({
            "title": article['title'],
            "link": article['link'],
            "source": article['source'],
            "published_date": article['published_date']
        })
        
        # Use the URL as a unique ID. Chroma's 'upsert' will update existing IDs 
        # or insert new ones, preventing duplicates in the vector space.
        ids.append(article['link'])

    print(f"Upserting {len(documents)} articles into local ChromaDB...")
    
    # Process in batches if the cache gets massive, but Chroma handles normal arrays fine
    collection.upsert(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    
    print("Database sync complete.")
    return len(documents)

def query_news(query_text, n_results=3):
    """
    Searches the local vector database for the most relevant articles.
    To be used by chatbot.py for the RAG pipeline.
    """
    collection = get_or_create_collection()
    
    # The embedding function automatically embeds the query_text
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results
    )
    
    return results

if __name__ == "__main__":
    # Test the re-indexing process manually
    processed_count = reindex_news()
    print(f"Ready! Vector store contains {processed_count} embedded documents.")