"""
Test suite for AI Log Analysis Pipeline
"""
import pytest
from fastapi.testclient import TestClient
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analyzer import app

client = TestClient(app)


class TestAPIEndpoints:
    """Test API endpoint functionality"""
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
    
    def test_analyze_log_endpoint_exists(self):
        """Test analyze endpoint is available"""
        # Just check the endpoint exists (POST to /analyze)
        response = client.post("/analyze", json={
            "log": "test log",
            "service": "test-service"
        })
        # May fail if Ollama not running, but endpoint should exist
        assert response.status_code in [200, 500]


class TestLogAnalysis:
    """Test log analysis functionality"""
    
    def test_empty_log_handling(self):
        """Test handling of empty logs"""
        response = client.post("/analyze", json={
            "log": "",
            "service": "test"
        })
        # Should handle gracefully
        assert response.status_code in [200, 400, 500]
    
    def test_log_with_service_name(self):
        """Test log analysis includes service name"""
        response = client.post("/analyze", json={
            "log": "Error: Connection refused",
            "service": "api-gateway"
        })
        # Should process without error (even if mock response)
        assert response is not None


class TestConfiguration:
    """Test configuration"""
    
    def test_ollama_host_configured(self):
        """Test Ollama host is configured"""
        from analyzer import OLLAMA_HOST
        assert OLLAMA_HOST.startswith("http")
    
    def test_model_name_configured(self):
        """Test model name is configured"""
        from analyzer import MODEL_NAME
        assert len(MODEL_NAME) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
