# CleanShare

Clean tracking parameters from URLs or text.

## Examples

Before:
```
https://example.com/article?utm_source=instagram&utm_medium=social&fbclid=XYZ
https://shop.com/product?gclid=123&utm_campaign=sale
```

After:
```
https://example.com/article
https://shop.com/product
```

## Install

```bash
./scripts/install.sh cleanshare
```

## Usage

```bash
# Single URL
cleanshare "https://example.com/?utm_source=x&utm_medium=y"

# Text with multiple URLs
cleanshare --text "Check: https://example.com/?utm_source=twitter and https://another.com/?fbclid=123"

# From stdin
echo "Visit https://example.com/?utm_source=twitter" | cleanshare --text

# Clipboard mode
cleanshare --clipboard
cleanshare --clipboard --text
```

Options:
- `-t, --text` — Treat input as text block (clean all URLs inside)
- `-c, --clipboard` — Read from and write to system clipboard
