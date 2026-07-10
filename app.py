import streamlit as st
from fetch_news import fetch_ai_news
from vectorstore import reindex_news
from chatbot import generate_response

# 1. Page Configuration
st.set_page_config(
    page_title="Local AI News Bot",
    page_icon="📰",
    layout="centered"
)

# Title & Description
st.title("📰 Local AI News RAG Bot")
st.markdown(
    "Ask questions about recent AI breakthroughs. This application processes everything "
    "locally via **Ollama (Llama 3)** and **ChromaDB** — no data leaves your machine."
)

# 2. Sidebar - Management Controls
with st.sidebar:
    st.header("Database Management")
    st.write(
        "The background scheduler updates the cache file every 30 minutes. "
        "Use the button below to force an immediate refresh and re-index."
    )
    
    # "Refresh news now" button
    if st.button("🔄 Refresh news now", use_container_width=True):
        with st.spinner("Fetching latest RSS feeds..."):
            try:
                # Step 1: Pull from RSS feeds and write to news_cache.json
                fetch_ai_news()
                st.write("Cache updated. Synchronizing vectors...")
                
                # Step 2: Push items from news_cache.json into local ChromaDB
                total_docs = reindex_news()
                
                st.success(f"Success! {total_docs} articles indexed in ChromaDB.")
            except Exception as e:
                st.error(f"An error occurred during refresh: {e}")

# 3. Initialize Chat History in Session State
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! I have scanned your local AI news database. Ask me anything about recent developments!",
            "citations": []
        }
    ]

# 4. Display Existing Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        # If the assistant message has citations, display them in an expander
        if message["role"] == "assistant" and message["citations"]:
            with st.expander("📚 View Sources Used"):
                for citation in message["citations"]:
                    st.markdown(citation)

# 5. Handle User Input
if user_query := st.chat_input("e.g., What are the latest developments in large language models?"):
    
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(user_query)
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_query})
    
    # Generate response from the RAG pipeline
    with st.chat_message("assistant"):
        with st.spinner("Querying local vector store and generating answer via Ollama..."):
            try:
                answer, citations = generate_response(user_query)
                
                # Render answer
                st.markdown(answer)
                
                # Render sources inside an expandable section if present
                if citations:
                    with st.expander("📚 View Sources Used"):
                        for citation in citations:
                            st.markdown(citation)
                
                # Add assistant response to session state history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "citations": citations
                })
                
            except Exception as e:
                error_msg = f"Failed to get a response from your local model. Make sure Ollama is running (`ollama serve`). Error: {e}"
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg,
                    "citations": []
                })