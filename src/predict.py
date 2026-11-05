"""
predict.py  (responsable: Luis)
===============================
Carga los modelos guardados y predice la clase de UN issue.
La API (src/api/main.py) usa esta funcion.
"""

import joblib

from src.config import LABELS, MODELS_DIR
from src.data.clean import clean_text

_cache = {}  # guardamos los modelos ya cargados para no leer el disco en cada peticion


def _cargar(repo):
    """Carga (y cachea) el modelo de un repo. Lanza FileNotFoundError si no existe."""
    if repo not in _cache:
        ruta = MODELS_DIR / f"{repo.replace('/', '__')}.joblib"
        _cache[repo] = joblib.load(ruta)
    return _cache[repo]


def predict_issue(title, body, repo="facebook/react"):
    """Devuelve (etiqueta, probabilidades) para un issue.

    Entrada : titulo, cuerpo y (opcional) el repo cuyo modelo se usara.
    Salida  : ("bug", {"bug": 0.8, "feature": 0.1, "question": 0.1})
    """
    modelo = _cargar(repo)
    texto = clean_text(title) + " . " + clean_text(body)  # MISMA limpieza que en entrenamiento
    probas = modelo.predict_proba([texto])[0]             # una probabilidad por clase
    clases = list(modelo.classes_)                        # orden en que el modelo guarda las clases
    dic = {c: float(p) for c, p in zip(clases, probas)}
    etiqueta = max(dic, key=dic.get)                      # la de mayor probabilidad
    return etiqueta, {l: dic.get(l, 0.0) for l in LABELS}
