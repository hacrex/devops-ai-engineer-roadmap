"""
Basic RAG System Example
=========================
This example demonstrates a complete Retrieval-Augmented Generation (RAG) pipeline
using ChromaDB as the vector store and HuggingFace embeddings.

Requirements:
    pip install langchain langchain-community langchain-chroma sentence-transformers
"""

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Sample technical documentation
DOCUMENTS = [
    """Python is a high-level, interpreted programming language known for its 
    simplicity and readability. Created by Guido van Rossum in 1991, Python 
    emphasizes code readability with significant whitespace. It supports multiple 
    programming paradigms including procedural, object-oriented, and functional 
    programming.""",
    """Machine Learning (ML) is a subset of artificial intelligence that enables 
    systems to learn and improve from experience without being explicitly programmed. 
    ML algorithms build mathematical models based on sample data (training data) to 
    make predictions or decisions. Common types include supervised, unsupervised, 
    and reinforcement learning.""",
    """Vector databases are specialized database systems designed to store, index, 
    and query high-dimensional vectors (embeddings). They use approximate nearest 
    neighbor (ANN) search algorithms to efficiently find similar vectors. Popular 
    examples include Chroma, Pinecone, Weaviate, and Qdrant.""",
    """Retrieval-Augmented Generation (RAG) is an AI framework that combines 
    information retrieval with text generation. It retrieves relevant documents 
    from a knowledge base and uses them as context for a language model to generate 
    accurate, grounded responses. This reduces hallucinations and provides citations.""",
    """Natural Language Processing (NLP) is a branch of AI focused on enabling 
    computers to understand, interpret, and generate human language. Key NLP tasks 
    include text classification, named entity recognition, machine translation, 
    sentiment analysis, and question answering.""",
]


def create_vector_store(documents, persist_directory="./chroma_db"):
    """
    Create a vector store from documents.

    Args:
        documents: List of text documents
        persist_directory: Directory to store the vector database

    Returns:
        Chroma vector store
    """
    print("📝 Splitting documents into chunks...")

    # Split documents into manageable chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=30,
        length_function=len,
        separators=["\n\n", "\n", ". ", " "],
    )
    chunks = text_splitter.create_documents(documents)

    print(f"✅ Created {len(chunks)} chunks")

    # Load embedding model
    print("🔄 Loading embedding model...")
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )

    # Create vector store
    print("💾 Creating vector store...")
    vectorstore = Chroma.from_documents(
        documents=chunks, embedding=embeddings, persist_directory=persist_directory
    )

    print(f"✅ Vector store created with {vectorstore._collection.count()} documents")
    return vectorstore


def create_rag_chain(vectorstore):
    """
    Create a RAG chain for question answering.

    Args:
        vectorstore: Chroma vector store

    Returns:
        RAG chain
    """
    # Create retriever
    retriever = vectorstore.as_retriever(
        search_type="similarity", search_kwargs={"k": 2}
    )

    # Create prompt template
    template = """You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer based on the context, say so.

Context:
{context}

Question: {question}

Answer:"""

    prompt = ChatPromptTemplate.from_template(template)

    # For this example, we'll use a simple mock LLM response
    # In production, replace with actual LLM (OpenAI, Anthropic, etc.)
    def mock_llm(input_dict):
        """Mock LLM that generates responses based on context"""
        context = input_dict["context"]
        question = input_dict["question"]

        # Simple extractive approach for demonstration
        context_text = "\n".join([doc.page_content for doc in context])

        response = f"""Based on the provided context:

{context_text}

The answer to '{question}' can be found in the documentation above. 
In a production system, this would be processed by an LLM like GPT-4 or Claude."""

        return response

    # Create RAG chain
    rag_chain = {"context": retriever, "question": RunnablePassthrough()} | mock_llm

    return rag_chain


def main():
    """Main function to demonstrate RAG pipeline"""
    print("=" * 60)
    print("🚀 Basic RAG System Example")
    print("=" * 60)

    # Step 1: Create vector store
    print("\n📚 Step 1: Creating Vector Store")
    print("-" * 40)
    vectorstore = create_vector_store(DOCUMENTS)

    # Step 2: Create RAG chain
    print("\n⛓️  Step 2: Creating RAG Chain")
    print("-" * 40)
    rag_chain = create_rag_chain(vectorstore)

    # Step 3: Test queries
    print("\n🔍 Step 3: Testing Queries")
    print("-" * 40)

    test_queries = [
        "What is Python?",
        "How does machine learning work?",
        "What are vector databases used for?",
        "Explain RAG architecture",
        "What is NLP?",
    ]

    for i, query in enumerate(test_queries, 1):
        print(f"\n❓ Query {i}: {query}")
        print("-" * 30)

        # Get retrieved documents
        retriever = vectorstore.as_retriever(search_kwargs={"k": 2})
        docs = retriever.invoke(query)

        print("📄 Retrieved documents:")
        for j, doc in enumerate(docs, 1):
            print(f"  [{j}] {doc.page_content[:100]}...")

        # Generate response
        response = rag_chain.invoke(query)
        print(f"\n💬 Response:\n{response}")
        print()

    print("=" * 60)
    print("✅ RAG Pipeline Complete!")
    print("=" * 60)

    print("\n💡 Next Steps:")
    print("  1. Replace mock LLM with actual API (OpenAI, Anthropic, etc.)")
    print("  2. Add streaming support for real-time responses")
    print("  3. Implement hybrid search for better retrieval")
    print("  4. Add evaluation metrics and monitoring")
    print("  5. Deploy with FastAPI or similar framework")


if __name__ == "__main__":
    main()
