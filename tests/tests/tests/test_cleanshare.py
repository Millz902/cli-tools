"""Tests for cleanshare tool"""
import sys
from pathlib import Path
from io import StringIO
from unittest.mock import patch, MagicMock
import pytest

# Import cleanshare module
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "tools" / "cleanshare"))
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


# Integration tests for main() function and CLI interface

def test_main_with_url_argument(capsys):
    """Test main() with a URL passed as command-line argument"""
    test_url = "https://example.com/page?utm_source=test&param=value"
    with patch('sys.argv', ['cleanshare', test_url]):
        main()
    
    captured = capsys.readouterr()
    output = captured.out.strip()
    assert "example.com/page" in output
    assert "param=value" in output
    assert "utm_source" not in output


def test_main_with_text_flag(capsys):
    """Test main() with --text flag to clean URLs within text"""
    test_text = "Check https://example.com/?utm_source=twitter"
    with patch('sys.argv', ['cleanshare', test_text, '--text']):
        main()
    
    captured = capsys.readouterr()
    output = captured.out
    assert "example.com" in output
    assert "utm_source" not in output


def test_main_with_stdin_input(capsys, monkeypatch):
    """Test main() reading from stdin when no argument provided"""
    test_url = "https://example.com/?fbclid=123456&id=789"
    monkeypatch.setattr('sys.stdin', StringIO(test_url))
    
    with patch('sys.argv', ['cleanshare']):
        main()
    
    captured = capsys.readouterr()
    output = captured.out.strip()
    assert "example.com" in output
    assert "id=789" in output
    assert "fbclid" not in output


def test_main_with_stdin_and_text_flag(capsys, monkeypatch):
    """Test main() reading text from stdin with --text flag"""
    test_text = "Visit https://test.com/?utm_campaign=email&page=home"
    monkeypatch.setattr('sys.stdin', StringIO(test_text))
    
    with patch('sys.argv', ['cleanshare', '--text']):
        main()
    
    captured = capsys.readouterr()
    output = captured.out
    assert "test.com" in output
    assert "page=home" in output
    assert "utm_campaign" not in output


def test_main_clipboard_without_pyperclip(capsys):
    """Test main() with --clipboard when pyperclip is not available"""
    with patch('sys.argv', ['cleanshare', '--clipboard']):
        with patch.dict('sys.modules', {'pyperclip': None}):
            with pytest.raises(SystemExit) as exc_info:
                main()
            
            assert exc_info.value.code == 1
    
    captured = capsys.readouterr()
    assert "pyperclip is not installed" in captured.err


def test_main_clipboard_url_mode(capsys):
    """Test main() with --clipboard flag for URL cleaning"""
    mock_pyperclip = MagicMock()
    test_url = "https://example.com/?utm_source=clipboard&param=keep"
    mock_pyperclip.paste.return_value = test_url
    
    with patch('sys.argv', ['cleanshare', '--clipboard']):
        with patch.dict('sys.modules', {'pyperclip': mock_pyperclip}):
            main()
    
    # Verify paste was called
    mock_pyperclip.paste.assert_called_once()
    # Verify copy was called with cleaned URL
    mock_pyperclip.copy.assert_called_once()
    copied_text = mock_pyperclip.copy.call_args[0][0]
    assert "example.com" in copied_text
    assert "param=keep" in copied_text
    assert "utm_source" not in copied_text
    
    captured = capsys.readouterr()
    assert "Cleaned text copied back to clipboard" in captured.out


def test_main_clipboard_text_mode(capsys):
    """Test main() with --clipboard and --text flags"""
    mock_pyperclip = MagicMock()
    test_text = "Check out https://site.com/?fbclid=abc123 for more info"
    mock_pyperclip.paste.return_value = test_text
    
    with patch('sys.argv', ['cleanshare', '--clipboard', '--text']):
        with patch.dict('sys.modules', {'pyperclip': mock_pyperclip}):
            main()
    
    mock_pyperclip.paste.assert_called_once()
    mock_pyperclip.copy.assert_called_once()
    copied_text = mock_pyperclip.copy.call_args[0][0]
    assert "site.com" in copied_text
    assert "fbclid" not in copied_text
    
    captured = capsys.readouterr()
    assert "Cleaned text copied back to clipboard" in captured.out


def test_main_short_text_flag(capsys):
    """Test main() with -t short flag"""
    test_text = "Visit https://example.com/?utm_medium=social"
    with patch('sys.argv', ['cleanshare', test_text, '-t']):
        main()
    
    captured = capsys.readouterr()
    output = captured.out
    assert "example.com" in output
    assert "utm_medium" not in output


def test_main_short_clipboard_flag(capsys):
    """Test main() with -c short flag"""
    mock_pyperclip = MagicMock()
    test_url = "https://example.com/?gclid=test123"
    mock_pyperclip.paste.return_value = test_url
    
    with patch('sys.argv', ['cleanshare', '-c']):
        with patch.dict('sys.modules', {'pyperclip': mock_pyperclip}):
            main()
    
    mock_pyperclip.copy.assert_called_once()
    copied_text = mock_pyperclip.copy.call_args[0][0]
    assert "gclid" not in copied_text
    
    captured = capsys.readouterr()
    assert "Cleaned text copied back to clipboard" in captured.out


def test_main_combined_flags(capsys):
    """Test main() with multiple flags combined"""
    mock_pyperclip = MagicMock()
    test_text = "Links: https://a.com/?utm_id=1 and https://b.com/?ref=test"
    mock_pyperclip.paste.return_value = test_text
    
    with patch('sys.argv', ['cleanshare', '-c', '-t']):
        with patch.dict('sys.modules', {'pyperclip': mock_pyperclip}):
            main()
    
    copied_text = mock_pyperclip.copy.call_args[0][0]
    assert "utm_id" not in copied_text
    assert "ref" not in copied_text
    assert "a.com" in copied_text
    assert "b.com" in copied_text
