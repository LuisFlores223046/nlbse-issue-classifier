"""
metrics.py  (responsable: Gabriel)
==================================
Metricas segun el protocolo NLBSE'24: F1 por clase, F1 por repo y F1 promedio global.
Todos los modelos (baseline, SetFit, RoBERTa...) usan ESTAS funciones para que la
comparacion sea justa y reproducible.
"""

import json

import pandas as pd
from sklearn.metrics import f1_score, precision_recall_fscore_support

from src.config import LABELS, METRICS_DIR


def evaluate(df, col_real="label", col_pred="pred"):
    """Calcula metricas a partir de un DataFrame con columnas repo, label (real) y pred.

    Salida: diccionario con
      - por_repo[repo] = {f1_macro, f1_bug, f1_feature, f1_question}
      - f1_promedio_repos = promedio simple de los F1 macro de los 5 repos
    Por que macro: las clases estan balanceadas por repo, macro las trata igual.
    """
    por_repo = {}
    for repo, g in df.groupby("repo"):  # un clasificador/evaluacion por repo, como pide NLBSE
        p, r, f, _ = precision_recall_fscore_support(
            g[col_real], g[col_pred], labels=LABELS, zero_division=0)
        por_repo[repo] = {
            "f1_macro": float(f1_score(g[col_real], g[col_pred], labels=LABELS,
                                       average="macro", zero_division=0)),
            **{f"f1_{lab}": float(f[i]) for i, lab in enumerate(LABELS)},
            **{f"precision_{lab}": float(p[i]) for i, lab in enumerate(LABELS)},
            **{f"recall_{lab}": float(r[i]) for i, lab in enumerate(LABELS)},
        }
    promedio = float(pd.Series([v["f1_macro"] for v in por_repo.values()]).mean())
    return {"por_repo": por_repo, "f1_promedio_repos": promedio, "n": int(len(df))}


def save_metrics(nombre_modelo, resultados, extra=None):
    """Guarda las metricas en reports/metrics/<nombre_modelo>.json.

    `extra` sirve para anotar parametros, version del dato, fecha, commit, etc.
    (esto es lo que enlaza resultado <-> codigo <-> dato en la matriz de trazabilidad).
    """
    METRICS_DIR.mkdir(parents=True, exist_ok=True)
    salida = {"modelo": nombre_modelo, **resultados, **(extra or {})}
    ruta = METRICS_DIR / f"{nombre_modelo}.json"
    ruta.write_text(json.dumps(salida, indent=2, ensure_ascii=False), encoding="utf-8")
    return ruta
