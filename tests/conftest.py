"""Pytest configuration and shared fixtures"""
import sys
from pathlib import Path
import pytest

# Add tools/cleanshare directory to Python path for imports
repo_root = Path(__file__).parent.parent
sys.path.insert(0, str(repo_root / "tools" / "cleanshare"))

@pytest.fixture
def sample_url():
    return "https://example.com/page?utm_source=test&utm_medium=email&param=value"

@pytest.fixture
def sample_text_with_urls():
    return "Check https://example.com/?utm_source=twitter and https://another.com/?fbclid=123"
