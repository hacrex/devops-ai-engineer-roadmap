"""
Test suite for DevOps AI Copilot
"""
import pytest
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from copilot import load_config


class TestConfigLoading:
    """Test configuration loading functionality"""
    
    def test_config_file_exists(self):
        """Test that config file exists"""
        config_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "config.yaml"
        )
        assert os.path.exists(config_path), "config.yaml should exist"
    
    def test_load_config_returns_dict(self):
        """Test that load_config returns a dictionary"""
        config = load_config()
        assert isinstance(config, dict), "Config should be a dictionary"
    
    def test_config_has_required_keys(self):
        """Test that config has required keys"""
        config = load_config()
        required_keys = ["model", "ollama_url"]
        for key in required_keys:
            assert key in config, f"Config should have '{key}' key"
    
    def test_ollama_url_format(self):
        """Test that Ollama URL has correct format"""
        config = load_config()
        ollama_url = config.get("ollama_url", "")
        assert ollama_url.startswith("http"), "Ollama URL should start with http"
        assert "localhost" in ollama_url or "127.0.0.1" in ollama_url, \
            "Ollama URL should point to localhost"


class TestCLICommands:
    """Test CLI command functionality"""
    
    def test_cli_help(self):
        """Test that CLI shows help"""
        from click.testing import CliRunner
        from copilot import cli
        
        runner = CliRunner()
        result = runner.invoke(cli, ['--help'])
        assert result.exit_code == 0
        assert "DevOps AI Copilot" in result.output
    
    def test_generate_command_exists(self):
        """Test that generate command is available"""
        from click.testing import CliRunner
        from copilot import cli
        
        runner = CliRunner()
        result = runner.invoke(cli, ['generate', '--help'])
        assert result.exit_code == 0


class TestModelConnection:
    """Test model connection (mocked)"""
    
    def test_model_name_not_empty(self):
        """Test that model name is configured"""
        config = load_config()
        model = config.get("model", "")
        assert len(model) > 0, "Model name should not be empty"
    
    @pytest.mark.skip(reason="Requires Ollama running")
    def test_ollama_connection(self):
        """Test connection to Ollama service"""
        import httpx
        config = load_config()
        response = httpx.get(f"{config['ollama_url']}/api/tags")
        assert response.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
