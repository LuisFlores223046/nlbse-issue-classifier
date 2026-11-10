"""
tabla_metricas.py  (responsables: Sebastian y Gabriel)
=====================================================
Lee TODOS los JSON de reports/metrics/ y arma la tabla comparativa en Markdown + una figura.
Asi ninguna cifra del reporte se escribe a mano: sale de los JSON.

Uso:  python scripts/tabla_metricas.py
Crea: docs/metricas_generada.md  y  reports/figures/f1_por_repo_modelos.png
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from src.config import FIGURES_DIR, METRICS_DIR, REPOS, ROOT


def main():
    filas = []
    for ruta in sorted(METRICS_DIR.glob("*.json")):
        d = json.loads(ruta.read_text(encoding="utf-8"))
        if "por_repo" not in d:   # JSON de otro tipo (p. ej. experimento_limpieza): se omite aqui
            continue
        fila = {"archivo": ruta.name, "split": d.get("split") or ("test" if "_test" in ruta.stem else "valid"), "F1 promedio": d["f1_promedio_repos"],
                "segundos": d.get("segundos_entrenamiento", "")}
        fila.update({r.split("/")[1]: d["por_repo"][r]["f1_macro"] for r in REPOS if r in d["por_repo"]})
        filas.append(fila)
    t = pd.DataFrame(filas)
    md = "# Tabla de métricas (generada por scripts/tabla_metricas.py; no editar a mano)\n\n"
    try:
        md += t.to_markdown(index=False, floatfmt=".4f")   # necesita el paquete tabulate
    except ImportError:
        md += t.round(4).to_string(index=False)            # sin tabulate: texto plano
    (ROOT / "docs" / "metricas_generada.md").write_text(md + "\n", encoding="utf-8")
    print(t.round(4).to_string(index=False))

    test = t[t["split"] == "test"].set_index("archivo")[[r.split("/")[1] for r in REPOS]]
    if len(test):
        test.index = [i.replace("baseline_tfidf_test", "baseline TF-IDF").replace("scalable_sgd_test", "SGD por lotes")
                      .replace(".json", "").replace("_C10", " (C=10)") for i in test.index]
        ax = test.T.plot(kind="bar", figsize=(8, 5))
        ax.set_title("F1 macro en test por repositorio y modelo")
        ax.set_xlabel("Repositorio")
        ax.set_ylabel("F1 macro")
        for cont in ax.containers:  # valor de F1 sobre cada barra
            ax.bar_label(cont, fmt="%.3f", fontsize=6, padding=2, rotation=90)
        ax.margins(y=0.15)
        ax.legend(title="Modelo", fontsize=8, loc="upper center", bbox_to_anchor=(0.5, -0.22), ncol=3)
        plt.xticks(rotation=20, ha="right")
        plt.tight_layout()
        plt.savefig(FIGURES_DIR / "f1_por_repo_modelos.png", dpi=150)
        plt.close()


if __name__ == "__main__":
    main()
