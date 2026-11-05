#!/usr/bin/env bash
# run_all.sh - Igual que run_all.ps1 pero para Linux/macOS/Git Bash.
set -e   # detener al primer error
python scripts/download_data.py
python scripts/hash_data.py
python -m src.data.make_dataset
python -m src.models.baseline_tfidf --split valid
python -m src.models.baseline_tfidf --split test
pytest -q
echo "Pipeline completo. Siguiente: uvicorn src.api.main:app --reload"
