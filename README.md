# Clasificación de issues de GitHub (bug / feature / question)

Proyecto final · Tópicos Selectos de Ingeniería de Software · UACJ · 2026
Equipo: Luis Flores, Rogelio, Sebastián, Gabriel, Evelyn.

## Problema
Los repositorios grandes reciben cientos de issues; etiquetarlos a mano toma tiempo.
Entrenamos clasificadores de texto que predicen si un issue es **bug**, **feature** o **question**,
analizamos dónde fallan y exponemos el mejor modelo en una API (FastAPI).

## Datos
Dataset oficial **NLBSE'24 Issue Report Classification** (3 000 issues, 5 repos).
Los CSV **no** se guardan en este repo (la licencia del original está vacía): se descargan con un script.
Ver `data/README.md`.

## Cómo reproducir (Windows, PowerShell, Python 3.11)
```powershell
git clone <URL-DEL-REPO>
cd <carpeta>
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
.\run_all.ps1            # descarga, limpia, entrena baseline, evalúa y corre pruebas
uvicorn src.api.main:app --reload   # API en http://127.0.0.1:8000/docs
```

## Estructura
| Carpeta | Contenido |
|---|---|
| `data/` | `raw` (original), `interim`, `processed` (no se suben a git) |
| `src/` | código: `data/` limpieza, `models/`, `metrics.py`, `api/`, `web/` |
| `tests/` | pruebas con pytest |
| `reports/` | métricas (JSON), calidad de datos, errores, figuras |
| `docs/` | decisiones, trazabilidad, contrato de la API, referencias |
| `ai_log/` | registro de uso de IA (obligatorio) |
| `notebooks/` | exploración (EDA) |

## Trazabilidad
Cada requisito → issue → commit/PR → archivo → prueba → resultado, en `docs/trazabilidad.md`.

## Licencia y créditos
Dataset: Kallis et al., *NLBSE'24 Tool Competition on Issue Report Classification* (ver `docs/referencias.md`).
