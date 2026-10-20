#!/usr/bin/env bash
# One-command setup and launch. Usage: ./run.sh
set -e
cd "$(dirname "$0")"
if [ ! -d .venv ]; then
  python3 -m venv .venv || { echo "Run: sudo apt install python3-venv"; exit 1; }
fi
.venv/bin/pip install -q pytest pyyaml
.venv/bin/python demo.py
