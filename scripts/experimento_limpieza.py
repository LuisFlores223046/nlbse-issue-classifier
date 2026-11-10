"""
experimento_limpieza.py  (responsable: Rogelio)
===============================================
Responde: "¿la limpieza ayuda?"  Compara el baseline (TF-IDF + regresion logistica) con
distintas variantes de limpieza, SOLO en validacion cruzada sobre train (el test no se toca).

Uso (desde la raiz del repo):
    python scripts/experimento_limpieza.py

Salida: una tabla en pantalla y el archivo reports/metrics/experimento_limpieza.json
(NO sobrescribe ningun JSON oficial del baseline).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # para poder importar src.*

import pandas as pd
from sklearn.model_selection import StratifiedKFold, cross_val_predict

from src.config import SEED, TRAIN_RAW
from src.data.clean import clean_dataframe, drop_duplicates_report
from src.metrics import evaluate, save_metrics
from src.models.baseline_tfidf import build_pipeline

# Cada variante apaga UN paso de limpieza para ver cuanto aporta.
VARIANTES = {
    "completa": {},
    "sin_urls": {"reemplazar_urls": False},
    "sin_codigo": {"reemplazar_codigo": False},
    "sin_quitar_html": {"quitar_comentarios_html": False},
}


def limpiar_con(df, **kwargs):
    """Igual que clean_dataframe pero permite apagar pasos (kwargs de clean_text)."""
    from src.data.clean import clean_text
    out = df.copy()
    out["title"] = out["title"].apply(lambda t: clean_text(t, **kwargs))
    out["body"] = out["body"].apply(lambda t: clean_text(t, **kwargs))
    out["text"] = (out["title"] + " . " + out["body"]).str.strip()
    return out


def f1_valid(df):
    """F1 macro promedio de los 5 repos con validacion cruzada de 5 pliegues (solo train)."""
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)
    filas = []
    for repo, g in df.groupby("repo"):
        pred = cross_val_predict(build_pipeline(1.0, None), g["text"], g["label"], cv=cv)
        filas.append(g.assign(pred=pred))
    return evaluate(pd.concat(filas))["f1_promedio_repos"]


def main():
    crudo = pd.read_csv(TRAIN_RAW)
    crudo, _ = drop_duplicates_report(crudo)
    resultados = {}
    for nombre, kw in VARIANTES.items():
        resultados[nombre] = f1_valid(limpiar_con(crudo, **kw))
        print(f"{nombre:18s} F1 promedio (valid) = {resultados[nombre]:.4f}")
    base = resultados["completa"]
    dif = {k: round(v - base, 4) for k, v in resultados.items()}
    ruta = save_metrics("experimento_limpieza", {"f1_valid_por_variante": resultados,
                                                 "diferencia_vs_completa": dif},
                        extra={"seed": SEED, "split": "valid"})
    print("Diferencia vs. completa:", dif)
    print(f"Guardado en {ruta}")


if __name__ == "__main__":
    main()
