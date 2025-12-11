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
