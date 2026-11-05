"""
config.py
=========
Un SOLO lugar con las constantes del proyecto (rutas, semilla, etiquetas).
Todos los demas archivos hacen `from src.config import ...` en vez de escribir
rutas "a mano". Asi, si algo cambia, se cambia aqui y listo.
"""

from pathlib import Path  # Path nos deja manejar rutas sin importar si es Windows o Linux

# Carpeta raiz del repo: este archivo esta en <raiz>/src/config.py,
# asi que subimos DOS niveles (parent = src, parent.parent = raiz).
ROOT = Path(__file__).resolve().parent.parent

# --- Carpetas de datos ---------------------------------------------------
DATA_RAW = ROOT / "data" / "raw"              # CSV originales. NUNCA se editan a mano.
DATA_INTERIM = ROOT / "data" / "interim"      # pasos intermedios (ej. ya sin duplicados)
DATA_PROCESSED = ROOT / "data" / "processed"  # datos finales listos para entrenar

# --- Carpetas de salidas -------------------------------------------------
REPORTS = ROOT / "reports"
METRICS_DIR = REPORTS / "metrics"             # un JSON por modelo con sus metricas
QUALITY_DIR = REPORTS / "data_quality"        # tablas/graficas de calidad de datos
ERRORS_DIR = REPORTS / "errores"              # analisis de errores del modelo
FIGURES_DIR = REPORTS / "figures"             # graficas para el reporte
MODELS_DIR = ROOT / "models"                  # modelos entrenados (.joblib) - NO van a git

# --- Archivos del dataset oficial NLBSE'24 -------------------------------
TRAIN_RAW = DATA_RAW / "issues_train.csv"
TEST_RAW = DATA_RAW / "issues_test.csv"

# URLs oficiales (repo nlbse2024/issue-report-classification, rama main)
BASE_URL = "https://raw.githubusercontent.com/nlbse2024/issue-report-classification/main/data"
TRAIN_URL = f"{BASE_URL}/issues_train.csv"
TEST_URL = f"{BASE_URL}/issues_test.csv"

# --- Esquema REAL del CSV (verificado, ojo: el README oficial dice otra cosa) ---
COLUMNS = ["repo", "created_at", "label", "title", "body"]
LABELS = ["bug", "feature", "question"]
REPOS = [
    "facebook/react",
    "tensorflow/tensorflow",
    "microsoft/vscode",
    "bitcoin/bitcoin",
    "opencv/opencv",
]

# --- Reproducibilidad ----------------------------------------------------
# Con la misma semilla, el modelo da los mismos resultados cada vez que se corre.
SEED = 42

# Version del modelo que devuelve la API (subirla cuando se reentrene).
MODEL_VERSION = "0.1.0"
