# Day 09: RAG + Vector Databases

## 🎯 Learning Objectives
- Understand Retrieval-Augmented Generation (RAG) architecture
- Learn vector database fundamentals and embeddings
- Implement a complete RAG pipeline from scratch
- Optimize retrieval strategies for production use cases
- Handle common RAG challenges (hallucinations, context limits)

## 📚 Table of Contents
1. [RAG Fundamentals](#rag-fundamentals)
2. [Vector Databases Deep Dive](#vector-databases-deep-dive)
3. [Building Your First RAG System](#building-your-first-rag-system)
4. [Advanced RAG Techniques](#advanced-rag-techniques)
5. [Lab Exercises](#lab-exercises)
6. [Knowledge Check](#knowledge-check)

---

## RAG Fundamentals

### What is RAG?

Retrieval-Augmented Generation (RAG) combines the power of:
- **Retrieval**: Finding relevant information from external knowledge sources
- **Generation**: Using LLMs to synthesize answers based on retrieved context

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   User Query    │────▶│   Retriever      │────▶│  Relevant Docs  │
└─────────────────┘     │ (Vector Search)  │     └─────────────────┘
                        └──────────────────┘              │
                               ▲                          ▼
                        ┌──────────────────┐     ┌─────────────────┐
                        │  Knowledge Base  │     │      LLM        │
                        │ (Vector Database)│     │  (Generator)    │
                        └──────────────────┘     └─────────────────┘
                                                         │
                                                         ▼
                                                ┌─────────────────┐
                                                │   Final Answer  │
                                                └─────────────────┘
```

### Why RAG?

**Benefits:**
- ✅ Access to up-to-date information beyond training cutoff
- ✅ Reduced hallucinations with grounded responses
- ✅ Domain-specific knowledge without fine-tuning
- ✅ Cost-effective vs. model fine-tuning
- ✅ Explainable AI with source citations

**Use Cases:**
- Customer support chatbots with product documentation
- Legal document analysis and case research
- Medical literature Q&A systems
- Internal company knowledge bases
- Technical documentation assistants

---

## Vector Databases Deep Dive

### Understanding Embeddings

Embeddings transform text into high-dimensional vectors where semantic similarity is preserved:

```python
from sentence_transformers import SentenceTransformer

# Load pre-trained embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Generate embeddings
texts = ["AI is transforming healthcare", "Machine learning in medicine"]
embeddings = model.encode(texts)

print(f"Embedding shape: {embeddings.shape}")  # (2, 384)
```

### Popular Vector Databases

| Database | Type | Best For | Key Features |
|----------|------|----------|--------------|
| **Chroma** | Embedded | Prototyping, small apps | Simple API, no setup |
| **FAISS** | In-memory | High-performance search | Facebook, GPU support |
| **Pinecone** | Managed | Production, scale | Serverless, auto-scaling |
| **Weaviate** | Hybrid | Complex queries | GraphQL, multi-modal |
| **Qdrant** | Self-hosted | Custom deployments | Filtering, payload |
| **Milvus** | Distributed | Large-scale | Cloud-native, horizontal scaling |

### Vector Similarity Metrics

```python
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def calculate_similarity(vec1, vec2):
    """Calculate cosine similarity between two vectors"""
    return cosine_similarity([vec1], [vec2])[0][0]

# Example usage
vec1 = np.random.rand(384)
vec2 = np.random.rand(384)
similarity = calculate_similarity(vec1, vec2)
print(f"Similarity: {similarity:.4f}")  # Range: -1 to 1
```

**Common Metrics:**
- **Cosine Similarity**: Angle between vectors (most common)
- **Euclidean Distance**: Straight-line distance
- **Dot Product**: Magnitude-aware similarity

---

## Building Your First RAG System

### Complete RAG Pipeline Example

See `examples/basic_rag.py` for a fully working implementation using ChromaDB.

#### Step 1: Document Ingestion

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# Sample documents
documents = [
    "Python is a high-level programming language known for its simplicity.",
    "Machine learning is a subset of AI that enables systems to learn from data.",
    "Vector databases store embeddings for efficient similarity search."
]

# Split documents into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    length_function=len
)
chunks = text_splitter.create_documents(documents)

# Create embeddings and vector store
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"
)
```

#### Step 2: Retrieval

```python
# Perform similarity search
query = "What is machine learning?"
results = vectorstore.similarity_search(query, k=2)

for i, doc in enumerate(results):
    print(f"Result {i+1}: {doc.page_content}")
```

#### Step 3: Generation with Context

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# Create RAG prompt template
template = """Answer the question based only on the following context:

Context:
{context}

Question: {question}

If you cannot find the answer in the context, say "I don't have enough information."

Answer:"""

prompt = ChatPromptTemplate.from_template(template)

# Initialize LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Create RAG chain
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

retriever = vectorstore.as_retriever()

rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# Execute query
response = rag_chain.invoke("What is machine learning?")
print(f"Answer: {response}")
```

### Running the Example

```bash
cd examples
pip install -r requirements.txt
python basic_rag.py
```

---

## Advanced RAG Techniques

### 1. Hybrid Search

Combine dense (vector) and sparse (keyword) retrieval:

```python
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever

# Dense retriever (vector-based)
dense_retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# Sparse retriever (keyword-based)
bm25_retriever = BM25Retriever.from_documents(chunks)
bm25_retriever.k = 3

# Combine both
ensemble_retriever = EnsembleRetriever(
    retrievers=[dense_retriever, bm25_retriever],
    weights=[0.7, 0.3]
)
```

### 2. Multi-Query Retrieval

Generate multiple query variations for better coverage:

```python
from langchain.retrievers.multi_query import MultiQueryRetriever

multi_query_retriever = MultiQueryRetriever.from_llm(
    retriever=vectorstore.as_retriever(),
    llm=llm
)

results = multi_query_retriever.invoke("Explain quantum computing")
```

### 3. Parent Document Retriever

Store large documents but retrieve smaller chunks:

```python
from langchain.retrievers import ParentDocumentRetriever
from langchain.storage import InMemoryStore

parent_store = InMemoryStore()
parent_retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=parent_store,
    child_splitter=RecursiveCharacterTextSplitter(chunk_size=200),
    parent_splitter=RecursiveCharacterTextSplitter(chunk_size=1000)
)
```

### 4. Reranking for Better Results

```python
from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain_community.cross_encoders import HuggingFaceCrossEncoder

# Initialize reranker
cross_encoder = HuggingFaceCrossEncoder(model_name="cross-encoder/ms-marco-TinyBERT-L-2-v2")
reranker = CrossEncoderReranker(model=cross_encoder, top_n=2)

# Apply reranking
compressed_docs = reranker.compress_documents(
    query=query,
    documents=initial_results
)
```

### 5. Handling Long Context

**Strategies:**
- **Map-Reduce**: Process chunks in parallel, then combine
- **Refine**: Iteratively update answer with each chunk
- **Map-Rerank**: Score and rank chunk contributions

```python
from langchain.chains import MapReduceDocumentsChain, ReduceDocumentsChain

# Define reduce chain
reduce_chain = ReduceDocumentsChain(
    combine_documents_chain=stuff_chain,
    collapse_documents_chain=stuff_chain,
    token_max=4000
)

# Create map-reduce chain
map_reduce_chain = MapReduceDocumentsChain(
    llm_chain=map_chain,
    reduce_documents_chain=reduce_chain,
    document_variable_name="context"
)
```

---

## Lab Exercises

### Lab 1: Build a Basic RAG System

**Objective**: Create a RAG system for technical documentation

**Files**: See `labs/lab1_basic_rag/starter_code.py`

**Tasks**:
1. Load and chunk a dataset of technical articles
2. Set up ChromaDB with appropriate embeddings
3. Implement retrieval with configurable k-value
4. Create a prompt template for accurate answers
5. Test with 5 different queries

**Success Criteria**:
- ✅ Documents properly chunked (300-500 tokens)
- ✅ Retrieval returns relevant documents (>0.7 similarity)
- ✅ Answers cite sources correctly
- ✅ Handles out-of-context questions gracefully

### Lab 2: Advanced Retrieval Strategies

**Objective**: Compare different retrieval approaches

**Tasks**:
1. Implement hybrid search (dense + sparse)
2. Add query expansion with LLM
3. Experiment with reranking
4. Measure precision@k for each approach

**Deliverable**: Comparison report with metrics

### Lab 3: Production RAG Pipeline

**Objective**: Build a scalable RAG system

**Tasks**:
1. Add caching layer for frequent queries
2. Implement async processing
3. Add monitoring for retrieval quality
4. Create evaluation dataset with ground truth

---

## Knowledge Check

### Questions

1. **What are the three main components of a RAG system?**
   <details>
   <summary>Click to reveal answer</summary>
   
   - **Retriever**: Finds relevant documents from knowledge base
   - **Generator (LLM)**: Synthesizes answer from retrieved context
   - **Knowledge Base**: Vector database storing document embeddings
   
   </details>

2. **Why might you choose hybrid search over pure vector search?**
   <details>
   <summary>Click to reveal answer</summary>
   
   Hybrid search combines:
   - **Semantic understanding** from dense vectors
   - **Exact keyword matching** from sparse methods (BM25)
   
   This improves recall for queries with specific terminology, acronyms, or when exact phrase matching matters.
   
   </details>

3. **What is the purpose of chunking in RAG?**
   <details>
   <summary>Click to reveal answer</summary>
   
   Chunking serves multiple purposes:
   - Fits content within LLM context window limits
   - Improves retrieval precision (smaller, focused chunks)
   - Enables better relevance scoring
   - Reduces noise in retrieved context
   
   Optimal chunk size depends on content type (typically 200-500 tokens).
   
   </details>

4. **How do you evaluate RAG system performance?**
   <details>
   <summary>Click to reveal answer</summary>
   
   **Retrieval Metrics**:
   - Precision@K, Recall@K
   - Mean Reciprocal Rank (MRR)
   - Normalized Discounted Cumulative Gain (NDCG)
   
   **Generation Metrics**:
   - Faithfulness (answer grounded in context)
   - Relevance (answers the question)
   - Context utilization efficiency
   
   **End-to-end**: Human evaluation, A/B testing
   
   </details>

5. **What are common failure modes in RAG systems?**
   <details>
   <summary>Click to reveal answer</summary>
   
   - **Poor retrieval**: Irrelevant documents retrieved
   - **Lost in the middle**: Important info buried in long context
   - **Contradictory sources**: Multiple documents conflict
   - **Outdated information**: Knowledge base not updated
   - **Prompt injection**: Malicious content in retrieved docs
   - **Hallucination**: LLM ignores provided context
   
   Mitigation strategies include reranking, better chunking, and guardrails.
   
   </details>

---

## Next Steps

### Further Learning
- Explore multi-modal RAG (images + text)
- Implement agentic RAG with tool use
- Study GraphRAG for structured knowledge
- Learn about RAG fine-tuning techniques

### Practice Projects
1. Build a customer support bot for a mock e-commerce site
2. Create a legal document analyzer for case precedents
3. Develop a medical literature assistant (with disclaimers)
4. Design an internal wiki search for a fictional company

### Resources
Check the `resources/` folder for curated links to:
- Vector database documentation
- Embedding model comparisons
- RAG evaluation frameworks
- Production deployment guides

---

**Congratulations!** You've learned how to build production-ready RAG systems with vector databases. Continue to Day 10 to learn about AI Observability and monitoring your RAG pipelines.
