#!/bin/bash
ls

CONFIG_DIR="$HOME/.config/blind-typing"
mkdir -p "$CONFIG_DIR"

if [ ! -f "$CONFIG_DIR/test.txt" ]; then
  cp /app/config/test.txt "$CONFIG_DIR/test.txt"
fi

exec python3 /app/main.py "$@"
