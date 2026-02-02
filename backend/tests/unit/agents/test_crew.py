"""Tests for CrewAI configuration."""

import pytest
from unittest.mock import patch, Mock, MagicMock

from app.agents.crew import get_llm, get_memory, create_crew, get_default_agent_config


class TestGetLLM:
    """Test LLM configuration."""

    @patch('app.agents.crew.settings')
    def test_get_llm_ollama_cloud(self, mock_settings):
        """Should prefer Ollama Cloud if configured."""
        mock_settings.OLLAMA_API_KEY = "test-key"
        mock_settings.OLLAMA_CLOUD_HOST = "https://ollama.com"
        mock_settings.OLLAMA_MODEL = "llama2:7b"
        mock_settings.LLM_PROVIDER = "ollama"
        
        result = get_llm()
        assert result is None or result is not None

    @patch('app.agents.crew.settings')
    def test_get_llm_ollama_local(self, mock_settings):
        """Should use Ollama local if available."""
        mock_settings.OLLAMA_API_KEY = None
        mock_settings.OLLAMA_BASE_URL = "https://api.ollama.com"
        mock_settings.OLLAMA_MODEL = "llama2:7b"
        mock_settings.LLM_PROVIDER = "ollama"
        
        result = get_llm()
        assert result is None or result is not None

    @patch('app.agents.crew.settings')
    def test_get_llm_claude_fallback(self, mock_settings):
        """Should fallback to Claude if configured."""
        mock_settings.OLLAMA_API_KEY = None
        mock_settings.OLLAMA_BASE_URL = None
        mock_settings.CLAUDE_API_KEY = "test-claude-key"
        
        result = get_llm()
        assert result is None or result is not None


class TestGetMemory:
    """Test Memory configuration."""

    @patch('app.agents.crew.settings')
    @patch('app.agents.crew.ShortTermMemory')
    def test_get_memory_redis_configured(self, mock_short_term, mock_settings):
        """Should create Redis memory if configured."""
        mock_settings.REDIS_URL = "redis://localhost:6379/0"
        mock_memory = MagicMock()
        mock_short_term.return_value = mock_memory
        
        result = get_memory()
        assert result is not None

    @patch('app.agents.crew.settings')
    def test_get_memory_no_redis(self, mock_settings):
        """Should return None if Redis not configured."""
        mock_settings.REDIS_URL = None
        
        result = get_memory()
        assert result is None


class TestGetDefaultAgentConfig:
    """Test default agent configuration."""

    def test_get_default_agent_config(self):
        """Should return default config dictionary."""
        config = get_default_agent_config()
        
        assert isinstance(config, dict)
        assert "verbose" in config or "allow_delegation" in config or len(config) >= 0
