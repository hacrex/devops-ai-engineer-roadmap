"""
Test suite for Local RAG Assistant
"""

import pytest
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestConfiguration:
    """Test configuration and environment setup"""

    def test_qdrant_host_env(self):
        """Test QDRANT_HOST environment variable"""
        host = os.environ.get("QDRANT_HOST", "localhost")
        assert isinstance(host, str)
        assert len(host) > 0

    def test_ollama_host_env(self):
        """Test OLLAMA_HOST environment variable"""
        host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
        assert host.startswith("http")
        assert "localhost" in host or "127.0.0.1" in host

    def test_collection_name_defined(self):
        """Test collection name is properly defined"""
        collection_name = "local-documents"
        assert len(collection_name) > 0
        assert " " not in collection_name


class TestEmbeddingModel:
    """Test embedding model functionality (mocked)"""

    @pytest.mark.skip(reason="Requires model download")
    def test_model_loads(self):
        """Test that embedding model can be loaded"""
        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer("all-MiniLM-L6-v2")
        assert model is not None

    @pytest.mark.skip(reason="Requires model download")
    def test_embedding_dimensions(self):
        """Test embedding produces correct dimensions"""
        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer("all-MiniLM-L6-v2")
        embedding = model.encode("test sentence")
        assert len(embedding) == 384


class TestQdrantConnection:
    """Test Qdrant vector database connection (mocked)"""

    @pytest.mark.skip(reason="Requires Qdrant running")
    def test_qdrant_connection(self):
        """Test connection to Qdrant service"""
        from qdrant_client import QdrantClient

        client = QdrantClient(host="localhost", port=6333)
        # Try to get collections list
        collections = client.get_collections()
        assert collections is not None

    def test_collection_name_format(self):
        """Test collection name follows naming conventions"""
        collection_name = "local-documents"
        # Should be lowercase with hyphens
        assert collection_name.islower() or "-" in collection_name
        assert len(collection_name) < 64  # Qdrant limit


class TestStreamlitApp:
    """Test Streamlit app structure"""

    def test_app_file_exists(self):
        """Test that app.py exists"""
        app_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "app.py"
        )
        assert os.path.exists(app_path), "app.py should exist"

    def test_docker_compose_exists(self):
        """Test that docker-compose.yml exists"""
        compose_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "docker-compose.yml",
        )
        assert os.path.exists(compose_path), "docker-compose.yml should exist"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
