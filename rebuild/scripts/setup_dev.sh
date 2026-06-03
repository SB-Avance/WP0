#!/usr/bin/env bash
set -euo pipefail
echo "Creating virtual environment .venv..."
python -m venv .venv
echo "Activating virtual environment..."
source .venv/bin/activate
echo "Upgrading pip and installing dependencies..."
python -m pip install --upgrade pip
pip install -r rebuild/requirements.txt

if command -v pre-commit >/dev/null 2>&1; then
  echo "Installing pre-commit hooks..."
  pre-commit install
else
  echo "pre-commit not found. Install it with 'pip install pre-commit'"
fi

echo "Done. Copy rebuild/.env.example to .env and fill the values."
