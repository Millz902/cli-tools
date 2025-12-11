#!/bin/bash
set -e

TOOLS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../tools" && pwd)"

install_tool() {
  local tool="$1"
  local path="$TOOLS_DIR/$tool"

  if [ ! -d "$path" ]; then
    echo "❌ Tool '$tool' not found"
    echo "Available tools:"
    ls -1 "$TOOLS_DIR" | grep -v "__template__"
    exit 1
  fi

  echo "📦 Installing $tool..."

  if [ -f "$path/requirements.txt" ]; then
    echo "  Installing Python dependencies..."
    
    # Check if we're in a virtual environment
    if [ -n "$VIRTUAL_ENV" ] || [ -n "$CONDA_DEFAULT_ENV" ]; then
      echo "  ✓ Virtual environment detected, installing normally..."
      pip install --quiet -r "$path/requirements.txt"
    else
      echo "  ⚠ Not in a virtual environment, installing to user site-packages..."
      pip install --quiet --user -r "$path/requirements.txt"
    fi
  fi

  chmod +x "$path/${tool}.py" 2>/dev/null || true

  if [ -w "/usr/local/bin" ]; then
    ln -sf "$path/${tool}.py" "/usr/local/bin/$tool"
    echo "✅ Installed to /usr/local/bin/$tool"
  else
    sudo ln -sf "$path/${tool}.py" "/usr/local/bin/$tool"
    echo "✅ Installed to /usr/local/bin/$tool (sudo used)"
  fi
}

if [ "$1" = "--all" ]; then
  echo "Installing all tools..."
  for d in "$TOOLS_DIR"/*; do
    [ -d "$d" ] && tool="$(basename "$d")" && [ "$tool" != "__template__" ] && install_tool "$tool"
  done
  echo "🎉 All tools installed!"
elif [ -n "$1" ]; then
  install_tool "$1"
else
  echo "Usage: $0 <tool-name> | --all"
  exit 1
fi
