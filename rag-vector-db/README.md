# 🗄️ RAG, Embeddings & High-Performance Vector Databases: Qdrant & pgvector

Large Language Models are bound by their training cut-off dates and have no knowledge of private enterprise data. **Retrieval-Augmented Generation (RAG)** resolves this limitation by fetching relevant document contexts from high-speed **Vector Databases** (like **Qdrant** or **pgvector**) and appending them to the user prompt before sending the request to the LLM. A DevOps AI Engineer must master chunking strategies, vector index algorithms, and orchestrating vector databases at scale.

---

## 🏗️ Retrieval-Augmented Generation (RAG) Architecture

```
 ┌──────────┐  Query "Fix OOM"  ┌──────────┐  Vector Query  ┌──────────┐
 │  Client  │ ────────────────► │  Python  │ ─────────────► │ Vector DB│
 │  Request │                   │  Service │                │ (Qdrant) │
 └──────────┘                   └────┬─────┘                └────┬─────┘
                                     │                           │
                                     │ Constructs                │ Returns High-
                                     │ Augmented Prompt          │ Relevance Context
                                     ▼                           ▼ (Runbooks)
 ┌──────────┐   Return Tokens   ┌──────────┐  Annotated Prompt  ┌──────────┐
 │ User     │ ◄──────────────── │  vLLM    │ ◄────────────────  │ Context  │
 │ Browser  │                   │  Server  │                    │ Injected │
 └──────────┘                   └──────────┘                    └──────────┘
```

---

## 📘 Vector Database Core Concepts

### 1. Vector Embeddings
An embedding is a numerical representation of real-world text inside high-dimensional vector space (e.g. a list of 1536 floating-point values). Similar concepts or sentences map closer together in vector space.
* **Similarity Algorithms**: The distance between two vectors is calculated using mathematical formulas: **Cosine Similarity** (compares angles), **Dot Product** (compares magnitudes), or **Euclidean Distance** (compares straight-line distance).

### 2. High-Performance Indexing: HNSW vs. IVFFlat
Flat sequential searches across millions of high-dimensional vectors are extremely slow. We pre-build indexes to enable fast searches:
* **IVFFlat (Inverted File Index)**: Groups vectors into clusters, searching only the closest clusters. Fast to build, but accuracy drops slightly.
* **HNSW (Hierarchical Navigable Small World)**: Creates a multi-layer graph structure connecting vectors. HNSW provides lightning-fast search speeds and high accuracy, but consumes significant memory (RAM) to house the active graph.

---

## 🛠️ Hands-on Ingestion Lab: Python RAG Pipeline

In this lab, you will build a complete, runnable Python RAG pipeline that chunk-processes operational runbooks, generates semantic embeddings, stores them in Qdrant, and runs semantic search queries.

### Step 1: Install Dependencies
```bash
pip install qdrant-client sentence-transformers torch
```

### Step 2: Write the RAG Ingestion & Query Script (`rag_pipeline.py`)
```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer

# 1. Initialize local Qdrant Client (Runs in-memory for testing, or links to cluster)
client = QdrantClient(":memory:") 
# client = QdrantClient("http://localhost:6333") # Production path

# 2. Load a lightweight, high-performance semantic embedding model
print("🚀 Loading sentence-transformer embedding model...")
encoder = SentenceTransformer('all-MiniLM-L6-v2') # Outputs 384-dimensional vectors

COLLECTION_NAME = "sre-runbooks"

# 3. Create the target Vector Collection
client.create_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(
        size=384, # Dimensions
        distance=Distance.COSINE # Metric
    )
)
print(f"🟢 Collection '{COLLECTION_NAME}' successfully initialized.")

# 4. Define and chunk mock operational runbooks
RUNBOOKS = [
    {
        "id": 1,
        "title": "Resolving Pod CrashLoopBackOff due to Memory issues",
        "content": "To resolve container crash loop issues, check if exit code is 137. If so, memory constraints were hit. Increase cgroups memory limit in deployment spec or enable transparent hugepages."
    },
    {
        "id": 2,
        "title": "DNS Lookup Failures in CoreDNS",
        "content": "If CoreDNS queries time out, check if kube-dns service is running. Validate CoreDNS configmap settings and verify iptables/calico CNI routing rules are active."
    },
    {
        "id": 3,
        "title": "GPU vRAM allocations failures",
        "content": "When vLLM reports CUDA out of memory, reduce maximum context size parameter (num_ctx), offload model layers, or switch to a 4-bit AWQ quantized model."
    }
]

# 5. Ingestion: Generate vectors and upsert into Qdrant
print("\n📥 Generating embeddings and upserting data...")
points = []
for book in RUNBOOKS:
    # Generate high-dimensional vector for content
    vector = encoder.encode(book["content"]).tolist()
    
    points.append(
        PointStruct(
            id=book["id"],
            vector=vector,
            payload={
                "title": book["title"],
                "content": book["content"]
            }
        )
    )

# Upsert vectors to Qdrant collection
client.upsert(
    collection_name=COLLECTION_NAME,
    points=points
)
print("✨ Ingestion complete! Vectors successfully indexed.")

# 6. Query RAG System
user_query = "Help! My container keeps failing with out of memory errors and crashing."
print(f"\n🔍 Searching Qdrant database for: '{user_query}'...")

# Generate embedding for the search query
query_vector = encoder.encode(user_query).tolist()

# Query Qdrant for the top matching document
search_results = client.search(
    collection_name=COLLECTION_NAME,
    query_vector=query_vector,
    limit=1
)

for result in search_results:
    print(f"\n🏆 Best Match Found (Confidence Score: {result.score:.4f}):")
    print(f"📖 Title: {result.payload['title']}")
    print(f"📄 Content snippet: {result.payload['content']}")
```

### Step 3: Run the Ingestion Pipeline
```bash
python rag_pipeline.py
```

---

## ⚡ Production Kubernetes Qdrant StatefulSet YAML

Deploying Qdrant in production requires persistent volumes, replication, and structured configurations to maintain high search availability.

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: qdrant-cluster
  namespace: ai-platform
spec:
  serviceName: qdrant-headless
  replicas: 3
  selector:
    matchLabels:
      app: qdrant-db
  template:
    metadata:
      labels:
        app: qdrant-db
    spec:
      containers:
      - name: qdrant
        image: qdrant/qdrant:v1.8.0
        ports:
        - containerPort: 6333
          name: http
        - containerPort: 6334
          name: grpc
        resources:
          requests:
            cpu: "2"
            memory: "8Gi"
          limits:
            cpu: "4"
            memory: "16Gi" # Must be large enough to house HNSW index in RAM!
        volumeMounts:
        - name: qdrant-data
          mountPath: /qdrant/storage
  volumeClaimTemplates:
  - metadata:
      name: qdrant-data
    spec:
      accessModes: [ "ReadWriteOnce" ]
      resources:
        requests:
          storage: 50Gi
```

---

## 🔒 Security Considerations
1. **Document-Level Permissions**: When building enterprise RAG, ensure search systems validate user permissions before fetching context. A junior developer must never retrieve high-relevance chunks representing payroll or executive keys!
2. **Database isolation**: Encrypt connection paths to Qdrant/pgvector using secure SSL/TLS. Restrict API port access (`6333`) using network security boundaries.
3. **Data Poisoning**: Sanitize documents before vector ingestion to block malicious injection data from poisoning model contexts.

---

## 📈 Scaling & Observability Considerations
* **Index Building Latency**: Building HNSW graph indexes consumes 100% CPU. Run index creation routines during low-traffic windows or schedule them on isolated background node pools.
* **VRAM/RAM Sizing**: HNSW vectors reside in system RAM. Ensure your nodes have sufficient RAM capacity using the calculation:
  $$\text{Required RAM} = \text{Vector Count} \times \text{Dimension Size} \times 4\text{ bytes} \times 1.5\text{ overhead multiplier}$$

---

## 🔍 Troubleshooting Guide

### 💥 Issue: Qdrant Database Pod crashes with `OOMKilled` (Out of Memory)
* **Root Cause**: The physical size of the HNSW index has outgrown the memory limits declared in the container's Kubernetes resources.
* **Mitigation**:
  1. Increase the container RAM limit in the StatefulSet manifest.
  2. Configure Qdrant to use **on-disk** HNSW vectors (reduces RAM usage drastically at the cost of slight query latency increases).
  3. Switch indexing configurations to use `IVFFlat` algorithms which have lower memory overhead.

---

## 🌟 Best Practices & Open-Source Tools
* **Qdrant**: A lightning-fast, production-grade vector database written in Rust.
* **pgvector**: An open-source Postgres extension to store and query vectors natively inside Postgres databases.
