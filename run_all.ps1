# run_all.ps1 - Reproduce TODO el pipeline en Windows PowerShell (desde la raiz del repo).
# Uso:  .\run_all.ps1
$ErrorActionPreference = "Stop"          # si un paso falla, se detiene todo

python scripts/download_data.py          # 1) bajar datos + huellas SHA-256
python scripts/hash_data.py              # 2) verificar que son los datos esperados
python -m src.data.make_dataset          # 3) limpiar -> data/processed
python -m src.models.baseline_tfidf --split valid   # 4) validacion (solo train)
python -m src.models.baseline_tfidf --split test    # 5) evaluacion final + guarda modelos
pytest -q                                # 6) pruebas
Write-Host "Pipeline completo. Siguiente: uvicorn src.api.main:app --reload"
