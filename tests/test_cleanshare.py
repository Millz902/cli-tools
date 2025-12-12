"""Tests for cleanshare tool"""
from cleanshare import clean_url, clean_text  # type: ignore

def test_clean_url_removes_tracking_params(sample_url):
    result = clean_url(sample_url)
    assert "utm_source" not in result
    assert "utm_medium" not in result
    assert "param=value" in result

def test_clean_url_preserves_non_tracking_params():
    url = "https://example.com/page?id=123&name=test&utm_source=twitter"
    result = clean_url(url)
    assert "id=123" in result
    assert "name=test" in result
    assert "utm_source" not in result

def test_clean_text_multiple_urls(sample_text_with_urls):
    result = clean_text(sample_text_with_urls)
    assert "utm_source" not in result
    assert "fbclid" not in result
    assert "example.com" in result
    assert "another.com" in result

def test_clean_url_no_query_params():
    """Test URL with no query parameters."""
    url = "https://example.com/page"
    result = clean_url(url)
    assert result == url

def test_clean_url_only_tracking_params():
    """Test URL with only tracking parameters (no query string after cleaning)."""
    url = "https://example.com/page?utm_source=test&fbclid=123"
    result = clean_url(url)
    assert "?" not in result
    assert "utm_source" not in result
    assert "fbclid" not in result

def test_clean_url_empty_string():
    """Test with empty string."""
    result = clean_url("")
    assert result == ""

def test_clean_url_malformed():
    """Test with malformed URL - should return original."""
    malformed = "not a valid url"
    result = clean_url(malformed)
    assert result == malformed


# CLI Integration Tests
import subprocess
import sys
from pathlib import Path

def test_cli_basic_url():
    """Test CLI with a basic URL argument."""
    script_path = Path(__file__).parent.parent / "tools" / "cleanshare" / "cleanshare.py"
    url = "https://example.com/page?utm_source=test&param=value"
    result = subprocess.run(
        [sys.executable, str(script_path), url],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "utm_source" not in result.stdout
    assert "param=value" in result.stdout

def test_cli_text_mode():
    """Test CLI with --text flag."""
    script_path = Path(__file__).parent.parent / "tools" / "cleanshare" / "cleanshare.py"
    text = "Visit https://example.com/?utm_source=test"
    result = subprocess.run(
        [sys.executable, str(script_path), "--text", text],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "utm_source" not in result.stdout
    assert "Visit" in result.stdout

def test_cli_stdin():
    """Test CLI with stdin input."""
    script_path = Path(__file__).parent.parent / "tools" / "cleanshare" / "cleanshare.py"
    url = "https://example.com/page?utm_source=test&param=value"
    result = subprocess.run(
        [sys.executable, str(script_path)],
        input=url,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "utm_source" not in result.stdout
    assert "param=value" in result.stdout

def test_cli_help():
    """Test CLI help message."""
    script_path = Path(__file__).parent.parent / "tools" / "cleanshare" / "cleanshare.py"
    result = subprocess.run(
        [sys.executable, str(script_path), "--help"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "Clean tracking parameters" in result.stdout or "clean" in result.stdout.lower()
