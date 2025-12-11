"""Tests for cleanshare tool"""
import sys
from pathlib import Path
import subprocess
import pytest

# Import cleanshare module
sys.path.insert(0, str(Path(__file__).parent.parent / "tools" / "cleanshare"))
from cleanshare import clean_url, clean_text, main  # type: ignore

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

def test_clean_url_no_query_params():
    """Test URL with no query parameters"""
    url = "https://example.com/page"
    result = clean_url(url)
    assert result == url

def test_clean_url_only_tracking_params():
    """Test URL with only tracking parameters (resulting in no query string)"""
    url = "https://example.com/page?utm_source=test&fbclid=123"
    result = clean_url(url)
    assert "utm_source" not in result
    assert "fbclid" not in result
    assert result == "https://example.com/page"

def test_clean_url_empty_string():
    """Test empty string input"""
    result = clean_url("")
    assert result == ""

def test_clean_url_malformed():
    """Test malformed URL - should return original"""
    malformed = "not a url at all"
    result = clean_url(malformed)
    # Should return original since it can't be parsed
    assert result == malformed

def test_clean_url_with_fixtures(sample_url):
    """Test using fixture"""
    result = clean_url(sample_url)
    assert "utm_source" not in result
    assert "param=value" in result

def test_clean_text_with_fixtures(sample_text_with_urls):
    """Test using fixture"""
    result = clean_text(sample_text_with_urls)
    assert "utm_source" not in result
    assert "fbclid" not in result

# CLI Integration Tests
def test_cli_single_url():
    """Test CLI with a single URL argument"""
    script_path = Path(__file__).parent.parent / "tools" / "cleanshare" / "cleanshare.py"
    result = subprocess.run(
        [sys.executable, str(script_path), "https://example.com/?utm_source=test&id=123"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "utm_source" not in result.stdout
    assert "id=123" in result.stdout

def test_cli_text_mode():
    """Test CLI with --text flag"""
    script_path = Path(__file__).parent.parent / "tools" / "cleanshare" / "cleanshare.py"
    text_input = "Check https://example.com/?utm_source=test"
    result = subprocess.run(
        [sys.executable, str(script_path), "--text", text_input],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "utm_source" not in result.stdout
    assert "example.com" in result.stdout

def test_cli_stdin():
    """Test CLI reading from stdin"""
    script_path = Path(__file__).parent.parent / "tools" / "cleanshare" / "cleanshare.py"
    url = "https://example.com/?utm_source=test&id=456"
    result = subprocess.run(
        [sys.executable, str(script_path)],
        input=url,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "utm_source" not in result.stdout
    assert "id=456" in result.stdout

def test_cli_help():
    """Test CLI help message"""
    script_path = Path(__file__).parent.parent / "tools" / "cleanshare" / "cleanshare.py"
    result = subprocess.run(
        [sys.executable, str(script_path), "--help"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "Clean tracking parameters" in result.stdout

