import ollama
from vectorstore import query_news

OLLAMA_MODEL = "llama3"

def generate_response(user_query):
    """
    RAG pipeline with connection safety constraints. 
    Returns descriptive error text instead of crashing if Ollama is unreachable.
    """
    # 1. Retrieve data chunks
    try:
        search_results = query_news(user_query, n_results=5)
    except Exception as db_error:
        return f"⚠️ Local Vector Store Error: Unable to query ChromaDB database ({db_error}). Try refreshing your database from the sidebar.", []
        
    context_text = ""
    citations = []
    
    if search_results['documents'] and search_results['documents'][0]:
        documents = search_results['documents'][0]
        metadatas = search_results['metadatas'][0]
        
        for i, (doc, meta) in enumerate(zip(documents, metadatas)):
            context_text += f"--- Article {i+1} ---\n{doc}\n\n"
            
            title = meta.get('title', 'Unknown Title')
            link = meta.get('link', '#')
            date = meta.get('published_date', 'Unknown Date')
            citations.append(f"* **[{title}]({link})** — _{date}_")

    if not context_text:
        return "I couldn't find any relevant news in my local database.", []

    # 2. Frame prompts
    system_instruction = (
        "You are an AI news assistant. Answer the user's question accurately using ONLY "
        "the provided context articles. If the context does not contain the answer, explicitly "
        "state that you don't have that information. Do not use outside knowledge."
    )
    user_prompt = f"Context Articles:\n{context_text}\n\nUser Question: {user_query}"

    # 3. Connection and Model validation for Ollama
    try:
        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_prompt}
            ]
        )
        return response['message']['content'], citations

    except Exception as ollama_error:
        # Build an easy-to-read troubleshooting message for the Streamlit UI
        error_message = (
            f"❌ **Ollama Service Unreachable**\n\n"
            f"The application was unable to process your request because the local LLM server failed to respond.\n\n"
            f"**Troubleshooting Steps:**\n"
            f"1. Check if the Ollama app is open and running in your Windows taskbar tray.\n"
            f"2. Verify that you have downloaded the required model by running `ollama pull {OLLAMA_MODEL}` in PowerShell.\n"
            f"3. Check that your local port is active by opening `http://localhost:11434` in your browser.\n\n"
            f"*(Technical Details: {ollama_error})*"
        )
        return error_message, []