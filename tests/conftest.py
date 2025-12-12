from pathlib import Path
import sys
import pytest

# Add cleanshare directory to Python path (avoid ambiguity by not adding tools_dir itself)
tools_dir = Path(__file__).parent.parent / "tools"
cleanshare_dir = tools_dir / "cleanshare"
sys.path.insert(0, str(cleanshare_dir))

# Fixtures used by tests/test_cleanshare.py
@pytest.fixture
def sample_url():
    return "https://example.com/page?utm_source=test&utm_medium=email&param=value"

@pytest.fixture
def sample_text_with_urls():
    return "Visit https://example.com/?utm_source=twitter and https://another.com/page?fbclid=123"