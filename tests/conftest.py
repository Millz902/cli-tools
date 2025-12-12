"""Pytest configuration and shared fixtures"""

import sys
from pathlib import Path
import pytest

# Add tools directory to Python path
tools_dir = Path(__file__).parent.parent / "tools"
sys.path.insert(0, str(tools_dir))
sys.path.insert(0, str(tools_dir / "cleanshare"))


@pytest.fixture
def sample_url():
    return "https://example.com/page?utm_source=test&utm_medium=email&param=value"


@pytest.fixture
def sample_text_with_urls():
    return "Check https://example.com/?utm_source=twitter and https://another.com/?fbclid=123"
