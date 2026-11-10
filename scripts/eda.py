"""
eda.py  (responsables: Rogelio y Gabriel)
=========================================
Analisis exploratorio (EDA) AUTOMATICO de los datos de ENTRENAMIENTO.
Responde las 5 preguntas de docs/perfil_repos.md con tablas y figuras reproducibles.

Uso (desde la raiz del repo, con el .venv activo):
    python scripts/eda.py

Lee   : data/raw/issues_train.csv  y  data/processed/train_clean.csv
Crea  : reports/eda/*.csv  (tablas agregadas; NO contienen texto de issues)
        reports/figures/eda_*.png  (figuras con titulo y ejes)
Nota  : solo usa TRAIN (el test no se explora para decidir nada).
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # para importar src.*

import matplotlib
matplotlib.use("Agg")  # dibujar sin abrir ventanas (sirve en cualquier PC)
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

from src.config import DATA_PROCESSED, FIGURES_DIR, LABELS, REPORTS, TRAIN_RAW

EDA_DIR = REPORTS / "eda"


def guardar_tabla(df, nombre):
    """Guarda una tabla en reports/eda/<nombre>.csv y la imprime."""
    ruta = EDA_DIR / f"{nombre}.csv"
    df.to_csv(ruta)
    mostrar = df if df.select_dtypes("datetime").shape[1] else df.round(3)  # round no aplica a fechas
    print(f"\n== {nombre} ==\n{mostrar.to_string()}")
    return ruta


def figura_barras(tabla, titulo, ylabel, nombre):
    """Dibuja barras agrupadas (filas = repo, columnas = clase) y guarda el PNG."""
    ax = tabla.plot(kind="bar", figsize=(8, 4.5))
    ax.set_title(titulo)
    ax.set_xlabel("Repositorio")
    ax.set_ylabel(ylabel)
    ax.legend(title="Clase")
    for cont in ax.containers:  # valor numerico sobre cada barra
        ax.bar_label(cont, fmt="%.0f", fontsize=7, padding=2)
    ax.margins(y=0.12)  # espacio arriba para que no se corten las etiquetas
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / f"{nombre}.png", dpi=150)
    plt.close()


def main():
    EDA_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    tr = pd.read_csv(TRAIN_RAW)
    body = tr["body"].fillna("")
    tr["len_title"] = tr["title"].fillna("").str.len()
    tr["len_body"] = body.str.len()
    tr["palabras_body"] = body.str.split().str.len()
    tr["tiene_codigo"] = body.str.contains("```", regex=False)
    tr["tiene_url"] = body.str.contains(r"https?://", regex=True)
    tr["tiene_plantilla"] = body.str.contains("###", regex=False)
    tr["tiene_html"] = body.str.contains("<!--", regex=False)

    # P0. Conteo repo x clase (debe ser 100 por celda; un duplicado puede dejar 99)
    guardar_tabla(tr.groupby(["repo", "label"]).size().unstack(), "conteo_repo_clase")

    # P1. Longitud (mediana de caracteres) por repo y clase
    for col, etiqueta in (("len_body", "cuerpo"), ("len_title", "titulo")):
        t = tr.groupby(["repo", "label"])[col].median().unstack()
        guardar_tabla(t, f"longitud_mediana_{etiqueta}")
        figura_barras(t, f"Mediana de caracteres del {etiqueta} por repositorio y clase",
                      "Caracteres (mediana)", f"eda_longitud_{etiqueta}")

    # P2. % de issues con codigo, URL, plantilla (###) y comentario HTML
    for col, etiqueta in (("tiene_codigo", "bloque de código"), ("tiene_url", "URL"),
                          ("tiene_plantilla", "plantilla (###)"), ("tiene_html", "comentario HTML")):
        t = tr.groupby(["repo", "label"])[col].mean().unstack() * 100
        guardar_tabla(t, f"pct_{col}")
        figura_barras(t, f"% de issues con {etiqueta}, por repositorio y clase",
                      "% de issues", f"eda_pct_{col}")

    # P3. Fechas: rango y numero de issues por anio
    fechas = pd.to_datetime(tr["created_at"], errors="coerce")
    rango = tr.assign(f=fechas).groupby("repo")["f"].agg(["min", "max"])
    guardar_tabla(rango, "rango_fechas_por_repo")
    por_anio = tr.assign(anio=fechas.dt.year).groupby(["anio", "label"]).size().unstack(fill_value=0)
    guardar_tabla(por_anio, "issues_por_anio_clase")
    ax = por_anio.plot(kind="bar", stacked=True, figsize=(8, 4.5))
    ax.set_title("Issues de entrenamiento por año de creación y clase")
    ax.set_xlabel("Año")
    ax.set_ylabel("Número de issues")
    ax.legend(title="Clase")
    for cont in ax.containers:  # valor dentro de cada segmento (solo si hay issues)
        ax.bar_label(cont, labels=[str(int(v)) if v > 0 else "" for v in cont.datavalues],
                     label_type="center", fontsize=7)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "eda_issues_por_anio.png", dpi=150)
    plt.close()

    # P4. Palabras distintivas por clase (sobre el texto ya limpio): las 10 con mayor
    #     proporcion de aparicion en esa clase frente al resto (documentos que la contienen).
    cl = pd.read_csv(DATA_PROCESSED / "train_clean.csv").fillna({"text": ""})
    vec = CountVectorizer(binary=True, min_df=5, stop_words="english")
    X = vec.fit_transform(cl["text"])
    vocab = vec.get_feature_names_out()
    filas = []
    for clase in LABELS:
        mask = (cl["label"] == clase).to_numpy()
        p_in = X[mask].mean(axis=0).A1       # proporcion de docs de la clase con la palabra
        p_out = X[~mask].mean(axis=0).A1     # proporcion en las demas clases
        score = p_in - p_out                 # diferencia: mayor = mas distintiva
        for idx in score.argsort()[-10:][::-1]:
            filas.append({"clase": clase, "palabra": vocab[idx],
                          "pct_en_clase": round(p_in[idx] * 100, 1),
                          "pct_en_otras": round(p_out[idx] * 100, 1)})
    guardar_tabla(pd.DataFrame(filas).set_index("clase"), "palabras_distintivas")

    # P5. Hallazgos para el modelado: titulos con prefijo tipo [Feature Request] / "Bug:" etc.
    prefijo = tr["title"].fillna("").str.contains(r"^\s*\[[^\]]+\]|^\s*\w+\s*:", regex=True)
    guardar_tabla(tr.assign(prefijo_titulo=prefijo).groupby(["repo", "label"])["prefijo_titulo"]
                  .mean().unstack() * 100, "pct_titulo_con_prefijo")
    print(f"\n[OK] Tablas en {EDA_DIR} y figuras eda_*.png en {FIGURES_DIR}")


if __name__ == "__main__":
    main()
