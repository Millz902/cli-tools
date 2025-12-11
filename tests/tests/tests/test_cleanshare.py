"""Tests for cleanshare tool"""
import sys
from pathlib import Path

# Import cleanshare module
sys.path.insert(0, str(Path(__file__).parent.parent / "tools" / "cleanshare"))
from cleanshare import clean_url, clean_text  # type: ignore

def test_clean_url_removes_tracking_params():
    url = "https://example.com/page?utm_source=test&utm_medium=email&param=value"
    result = clean_url(url)
    assert "utm_source" not in result
    assert "utm_medium" not in result
    assert "param=value" in result

def test_clean_url_preserves_non_tracking_params():
    url = "https://example.com/page?id=123&name=test&utm_source=twitter"
    result = clean_url(url)
    assert "id=123" in result
    assert "name=test" in result
    assert "utm_source" not in result

def test_clean_text_multiple_urls():
    text = "Visit https://example.com/?utm_source=twitter and https://another.com/page?fbclid=123"
    result = clean_text(text)
    assert "utm_source" not in result
    assert "fbclid" not in result
    assert "example.com" in result
    assert "another.com" in result
