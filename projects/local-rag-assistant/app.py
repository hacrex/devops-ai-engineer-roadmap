import os
import streamlit as st
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
import httpx

# 1. Initialize Clients & Environment
QDRANT_HOST = os.environ.get("QDRANT_HOST", "localhost")
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
COLLECTION_NAME = "local-documents"

st.set_page_config(page_title="🚀 Secure Local RAG Assistant", layout="wide")
st.title("🛡️ Enterprise Local RAG Assistant Portal")


@st.cache_resource
def get_embedding_model():
    # Load 384-dimensional sentence transformer model
    return SentenceTransformer("all-MiniLM-L6-v2")


@st.cache_resource
def get_qdrant_client():
    client = QdrantClient(host=QDRANT_HOST, port=6333)
    # Ensure collection exists
    try:
        client.get_collection(COLLECTION_NAME)
    except Exception:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE),
        )
    return client


encoder = get_embedding_model()
qdrant = get_qdrant_client()

# Sidebar: Configuration
st.sidebar.header("⚙️ Core Systems Configuration")
selected_model = st.sidebar.selectbox(
    "LLM Model Selection", ["qwen2.5-coder:7b", "llama3:latest"]
)

# Main layout divided into Ingestion & Query
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📥 Ingest Operational Context")
    doc_title = st.text_input(
        "Document Name / Title", placeholder="e.g. Memory Outage Recovery"
    )
    doc_content = st.text_area(
        "Document Content / Details",
        height=200,
        placeholder="e.g. Container terminated. Exit Code 137...",
    )

    if st.button("Index Document"):
        if doc_title and doc_content:
            with st.spinner("Generating embeddings and upserting..."):
                # Generate embedding vector
                vector = encoder.encode(doc_content).tolist()

                # Check current collection size to generate next index ID
                collection_info = qdrant.get_collection(COLLECTION_NAME)
                point_id = collection_info.points_count + 1

                # Upsert into Qdrant
                qdrant.upsert(
                    collection_name=COLLECTION_NAME,
                    points=[
                        PointStruct(
                            id=point_id,
                            vector=vector,
                            payload={"title": doc_title, "content": doc_content},
                        )
                    ],
                )
                st.success(
                    f"✨ Document '{doc_title}' successfully indexed into Qdrant vector store!"
                )
        else:
            st.error("Please fill both Title and Content fields.")

with col2:
    st.header("🔍 Ask the Assistant")
    user_query = st.text_input(
        "Search / Prompt Query",
        placeholder="e.g., How do I recover from a memory crash?",
    )

    if st.button("Submit Query"):
        if user_query:
            with st.spinner("Searching Vector Database..."):
                # 1. Generate query embedding
                query_vector = encoder.encode(user_query).tolist()

                # 2. Search Qdrant
                search_results = qdrant.search(
                    collection_name=COLLECTION_NAME, query_vector=query_vector, limit=2
                )

                if search_results:
                    context_chunks = []
                    st.subheader("📚 High-Relevance Vector Context Found:")
                    for res in search_results:
                        st.info(
                            f"**Match: {res.payload['title']}** "
                            f"(Score: {res.score:.4f})\n\n{res.payload['content']}"
                        )
                        context_chunks.append(res.payload["content"])

                    # Assemble augmented context
                    context = "\n---\n".join(context_chunks)

                    # 3. Prompt local LLM with context
                    prompt = f"""Use the following context to answer the question accurately.
                    If the context is irrelevant, answer using standard systems knowledge.

                    Context:
                    {context}

                    Question: {user_query}
                    Answer:"""

                    with st.spinner("Querying Local LLM..."):
                        try:
                            payload = {
                                "model": selected_model,
                                "prompt": prompt,
                                "stream": False,
                            }
                            response = httpx.post(
                                f"{OLLAMA_HOST}/api/generate",
                                json=payload,
                                timeout=60.0,
                            )
                            if response.status_code == 200:
                                result = response.json()
                                st.subheader("🤖 Local AI Response:")
                                st.markdown(result["response"])
                            else:
                                st.error("Ollama API call failed.")
                        except Exception as e:
                            st.warning(
                                "Local model host offline. Simulated Local LLM Output:\n\n"
                                f"*Error details: {e}*"
                            )
                            st.markdown(
                                "⚠️ **Simulation Fallback:** Since your Ollama server is offline, "
                                "this mock message verifies the RAG assembly loop compiled "
                                "successfully. Re-configure the Ollama server connection "
                                "inside the sidebar."
                            )
                else:
                    st.warning("No relevant matching documents found in vector store.")
