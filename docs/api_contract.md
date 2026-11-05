# Contrato de la API (v0.1.0)

Base: `http://127.0.0.1:8000` · docs interactivas: `/docs`

## GET /health
200 → `{"status": "ok"}`

## POST /predict
Entrada (JSON):
```json
{"title": "App crashes on start", "body": "Stack trace ...", "repo": "facebook/react"}
```
- `title` obligatorio (≥ 1 carácter). `body` opcional. `repo` opcional (por defecto facebook/react) y debe ser uno de los 5.

Salida 200:
```json
{"label": "bug", "probabilities": {"bug": 0.81, "feature": 0.12, "question": 0.07}, "model_version": "0.1.0"}
```
Errores: **422** datos inválidos (título vacío, repo desconocido) · **503** modelo aún no entrenado.

## Prueba rápida (PowerShell)
```powershell
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/predict -ContentType "application/json" `
  -Body '{"title":"App crashes on start","body":"TypeError at line 3","repo":"facebook/react"}'
```
