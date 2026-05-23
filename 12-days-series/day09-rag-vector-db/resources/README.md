# Day 09: RAG + Vector Databases - Resources

## 📚 Documentation & Guides

### Vector Databases
- [Chroma Documentation](https://docs.trychroma.com/) - Simple, open-source vector database
- [Pinecone Developer Guide](https://docs.pinecone.io/) - Managed vector database service
- [Weaviate Docs](https://weaviate.io/developers/weaviate) - GraphQL-enabled vector database
- [Qdrant Documentation](https://qdrant.tech/documentation/) - High-performance vector search
- [FAISS GitHub](https://github.com/facebookresearch/faiss) - Facebook AI Similarity Search

### Embedding Models
- [Sentence Transformers](https://www.sbert.net/) - Pre-trained models for embeddings
- [HuggingFace Embedding Models](https://huggingface.co/models?pipeline_tag=sentence-similarity)
- [OpenAI Embeddings Guide](https://platform.openai.com/docs/guides/embeddings)
- [Cohere Embeddings](https://docs.cohere.com/docs/embeddings)

### RAG Frameworks
- [LangChain RAG Guide](https://python.langchain.com/docs/use_cases/question_answering/)
- [LlamaIndex Documentation](https://docs.llamaindex.ai/) - Data framework for LLMs
- [Haystack Tutorials](https://haystack.deepset.ai/tutorials) - NLP pipeline framework

## 🎓 Learning Resources

### Tutorials & Courses
- [RAG Course by DeepLearning.AI](https://www.deeplearning.ai/short-courses/)
- [Vector Databases Explained (YouTube)](https://www.youtube.com/results?search_query=vector+database+tutorial)
- [Building RAG Systems with LangChain](https://python.langchain.com/docs/tutorials/rag/)

### Research Papers
- [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks (2020)](https://arxiv.org/abs/2005.11401)
- [Dense Passage Retrieval for Open-Domain Question Answering](https://arxiv.org/abs/2004.04906)
- [The Curse of Recursion in RAG (2024)](https://arxiv.org/abs/2404.04475)

## 🛠️ Tools & Libraries

### Python Libraries
```bash
# Core RAG libraries
pip install langchain langchain-community langchain-chroma
pip install sentence-transformers
pip install chromadb
pip install faiss-cpu

# Advanced features
pip install rank-bm25  # For hybrid search
pip install InstructorEmbedding  # Better embeddings
pip install cohere  # Alternative embeddings
```

### Evaluation Tools
- [RAGAS](https://github.com/explodinggradients/ragas) - RAG evaluation framework
- [TruLens](https://github.com/truera/trulens) - LLM evaluation toolkit
- [Arize Phoenix](https://github.com/Arize-ai/phoenix) - Observability for RAG

## 📊 Datasets for Practice

### Free Datasets
- [Wikipedia Dump](https://huggingface.co/datasets/wikipedia) - General knowledge
- [arXiv Papers](https://huggingface.co/datasets/arxiv_dataset) - Scientific papers
- [Stack Overflow Questions](https://huggingface.co/datasets/stackexchange) - Technical Q&A
- [Legal Case Reports](https://huggingface.co/datasets/legal_case_reports) - Legal domain
- [Medical PubMed](https://huggingface.co/datasets/pubmed) - Medical literature

### Sample Data Generators
- [Faker Library](https://faker.readthedocs.io/) - Generate fake documents
- [Synthetic Data Generator](https://github.com/mostly-ai/mostly-ai) - Create test datasets

## 🏗️ Production Patterns

### Architecture Examples
- [RAG Reference Architecture (AWS)](https://aws.amazon.com/blogs/machine-learning/rag-reference-architecture/)
- [Azure AI Search RAG](https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview)
- [Google Cloud RAG Patterns](https://cloud.google.com/blog/products/ai-machine-learning/rag-patterns)

### Best Practices
- [RAG Optimization Guide](https://weaviate.io/blog/rag-optimization)
- [Advanced RAG Techniques](https://learn.deeplearning.ai/courses/advanced-rag)
- [Production RAG Checklist](https://github.com/MLOps-guide/rag-checklist)

## 💬 Communities & Support

### Forums & Discord
- [LangChain Discord](https://discord.gg/langchain)
- [LlamaIndex Discord](https://discord.gg/dGJ9dYzEYk)
- [r/MachineLearning](https://www.reddit.com/r/MachineLearning/)
- [HuggingFace Forums](https://discuss.huggingface.co/)

### Newsletters
- [The Batch by DeepLearning.AI](https://www.deeplearning.ai/the-batch/)
- [Import AI](https://jack-clark.net/)
- [NLP News](https://www.linkedin.com/newsletters/nlp-news-6883912040109498368/)

## 🔍 Troubleshooting

### Common Issues
- [RAG Troubleshooting Guide](https://docs.llamaindex.ai/en/stable/module_guides/deploying/troubleshooting/)
- [Vector Database Performance Tuning](https://qdrant.tech/articles/performance-tuning/)
- [Embedding Model Selection Guide](https://sbartula.medium.com/which-sentence-transformers-embedding-model-to-choose-8acbe96c636d)

### Debugging Tools
- [LangSmith](https://smith.langchain.com/) - Debug and monitor LLM apps
- [Weights & Biases](https://wandb.ai/) - Track experiments
- [Prometheus + Grafana](https://prometheus.io/) - Monitoring stack

## 📈 Performance Benchmarks

### Leaderboards
- [MTEB Leaderboard](https://huggingface.co/spaces/mteb/leaderboard) - Embedding model rankings
- [BEIR Benchmark](https://github.com/beir-cellar/beir) - Information retrieval benchmark
- [RAG Evaluation Datasets](https://github.com/ranjaykrishna/datasets-rag)

---

**Last Updated**: January 2025

**Contributing**: Found a great resource? Submit a PR to add it to this list!
