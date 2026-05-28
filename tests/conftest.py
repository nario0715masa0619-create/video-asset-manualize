"""
Pytest configuration and fixtures.
"""
import pytest
import os
from unittest.mock import patch

@pytest.fixture
def mock_openai_api_key():
    """Mock OPENAI_API_KEY for tests."""
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-mock-key"}):
        yield "test-mock-key"

@pytest.fixture
def clear_openai_api_key():
    """Ensure OPENAI_API_KEY is not set during tests."""
    with patch.dict(os.environ):
        if "OPENAI_API_KEY" in os.environ:
            del os.environ["OPENAI_API_KEY"]
        yield
