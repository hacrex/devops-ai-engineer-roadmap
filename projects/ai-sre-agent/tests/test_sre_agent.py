"""
Test suite for AI SRE Agent
"""

import pytest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestConfiguration:
    """Test configuration and environment setup"""

    def test_ollama_host_env(self):
        """Test OLLAMA_HOST environment variable"""
        host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
        assert isinstance(host, str)
        assert host.startswith("http")

    def test_model_name_env(self):
        """Test MODEL_NAME environment variable"""
        model = os.environ.get("MODEL_NAME", "qwen2.5-coder:7b")
        assert isinstance(model, str)
        assert len(model) > 0


class TestK8sInitialization:
    """Test Kubernetes initialization (mocked)"""

    def test_k8s_init_function_exists(self):
        """Test that k8s init function is defined"""
        from sre_agent import initialize_k8s

        assert callable(initialize_k8s)

    def test_graceful_k8s_failure(self):
        """Test that K8s init handles missing config gracefully"""
        from sre_agent import initialize_k8s

        # Should not raise exception even without kubeconfig
        result = initialize_k8s()
        # Returns None if no config found, which is expected
        assert result is None or hasattr(result, "read_namespaced_pod_log")


class TestLogGathering:
    """Test log gathering functionality"""

    def test_gather_logs_function_exists(self):
        """Test that log gathering function exists"""
        from sre_agent import gather_container_logs

        assert callable(gather_container_logs)

    def test_gather_logs_without_k8s(self):
        """Test log gathering works without K8s connection (simulation mode)"""
        from sre_agent import gather_container_logs

        logs = gather_container_logs("test-pod", "default")
        assert isinstance(logs, str)
        assert len(logs) > 0


class TestFlaskApp:
    """Test Flask application structure"""

    def test_app_exists(self):
        """Test that Flask app is created"""
        from sre_agent import app

        assert app is not None
        assert app.name == __name__.split(".")[0] or app.name == "sre_agent"

    def test_app_has_routes(self):
        """Test that app has routes defined"""
        from sre_agent import app

        rules = [rule.rule for rule in app.url_map.iter_rules()]
        assert len(rules) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
