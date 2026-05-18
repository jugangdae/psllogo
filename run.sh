#!/bin/sh

set -e

if [ ! -d ".venv" ]; then
  if ! python3 -m venv .venv >/dev/null 2>&1; then
    echo "failed to create .venv" >&2
    exit 1
  fi
fi

if ! .venv/bin/python -c "import aggdraw, PIL" >/dev/null 2>&1; then
  if ! .venv/bin/python -m pip install --quiet --disable-pip-version-check -r requirements.txt >/dev/null 2>&1; then
    echo "failed to install dependencies" >&2
    exit 1
  fi
fi

printf "Size px: "
read -r size

if [ -z "$size" ]; then
  echo "size is required"
  exit 1
fi

printf "Background hex (default transparent): "
read -r background

if [ -z "$background" ]; then
  .venv/bin/python make_png.py "$size"
else
  .venv/bin/python make_png.py "$size" "$background"
fi
