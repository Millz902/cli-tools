#!/usr/bin/env python3
import argparse
import re
import sys
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse

# Common tracking parameters to strip from URLs
TRACKING_PARAMS = {
    "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content", "utm_id",
    "gclid", "fbclid", "mc_cid", "mc_eid", "igshid",
    "ref", "ref_src", "vero_conv", "vero_id",
}

URL_REGEX = re.compile(r"(https?://[^\s)>\]]+)", re.IGNORECASE)

def clean_url(url: str) -> str:
    """Remove tracking parameters from a single URL."""
    try:
        parsed = urlparse(url)
    except ValueError as e:
        print(f"Warning: Failed to parse URL '{url}': {e}", file=sys.stderr)
        return url
    params = parse_qsl(parsed.query, keep_blank_values=True)
    kept = [(k, v) for (k, v) in params if k.lower() not in TRACKING_PARAMS]
    query = urlencode(kept, doseq=True)
    return urlunparse(parsed._replace(query=query))

def clean_text(text: str) -> str:
    """Find all URLs in a text block and clean them."""
    return URL_REGEX.sub(lambda m: clean_url(m.group(1)), text)

def main():
    parser = argparse.ArgumentParser(
        description="Clean tracking parameters from URLs or from text containing URLs."
    )
    parser.add_argument("input", nargs="?", help="A URL or text to clean. If omitted, reads from stdin.")
    parser.add_argument("-t", "--text", action="store_true", help="Treat input as text (clean all URLs inside).")
    parser.add_argument("-c", "--clipboard", action="store_true", help="Use clipboard as input/output.")
    args = parser.parse_args()

    if args.clipboard:
        try:
            import pyperclip  # type: ignore
        except ImportError:
            print("[!] pyperclip is not installed. Run: pip install pyperclip", file=sys.stderr)
            sys.exit(1)
        original = pyperclip.paste()
        # Only strip whitespace for single-URL mode, preserve it for text mode
        if args.text:
            cleaned = clean_text(original)
        else:
            cleaned = clean_url(original.strip())
        pyperclip.copy(cleaned)
        print("✅ Cleaned text copied back to clipboard.")
        return

    data = args.input if args.input else sys.stdin.read()
    print(clean_text(data) if args.text else clean_url(data.strip()))

if __name__ == "__main__":
    main()
