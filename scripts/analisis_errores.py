"""
analisis_errores.py  (responsable: Gabriel)
===========================================
Las 7 preguntas de analitica de errores de la guia 04, con codigo reproducible.
Usa SOLO validacion (validacion cruzada en train). El test no se usa para decidir nada.
(Unica excepcion: la pregunta 6 mira las predicciones del test OFICIAL ya generadas, solo para
describir, nunca para ajustar nada.)

Requisitos previos (una vez):
    python -m src.data.make_dataset
    python -m src.models.baseline_tfidf --split valid     # crea pred_baseline_tfidf_valid.csv
    python -m src.models.baseline_tfidf --split test      # (ya lo hizo run_all) para la pregunta 6

Uso:
    python scripts/analisis_errores.py

Crea: reports/errores/*.csv, reports/figures/confusion_*.png, reports/figures/errores_*.png
      y reports/metrics/fuga_sin_plantilla.json  (experimento propio, no pisa nada oficial)
"""

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.model_selection import StratifiedKFold, cross_val_predict

from src.config import (DATA_PROCESSED, ERRORS_DIR, FIGURES_DIR, LABELS, METRICS_DIR, SEED,
                        TEST_RAW, TRAIN_RAW)
from src.metrics import evaluate, save_metrics
from src.models.baseline_tfidf import build_pipeline

RE_ENCABEZADO = re.compile(r"###\s*\w+(\s\w+){0,3}")  # aproximacion a "### Repro steps"


def mostrar(df, titulo):
    print(f"\n== {titulo} ==\n{df.round(3).to_string()}")


def p1_confusion(pred):
    """P1. Matriz de confusion por repo + conteo de errores por par (real -> predicho)."""
    for repo, g in pred.groupby("repo"):
        ConfusionMatrixDisplay.from_predictions(g["label"], g["pred"], labels=LABELS)
        plt.title(f"Matriz de confusión (validación) · {repo}")
        plt.tight_layout()
        plt.savefig(FIGURES_DIR / f"confusion_{repo.replace('/', '__')}.png", dpi=150)
        plt.close()
    err = pred[pred.label != pred.pred].groupby(["repo", "label", "pred"]).size().rename("errores")
    err.to_csv(ERRORS_DIR / "p1_confusiones_por_par.csv")
    mostrar(err.to_frame(), "P1 errores por par real->predicho")


def p2_repo_dificil():
    """P2. F1 macro por repo (del JSON oficial de validacion), ordenado de menor a mayor."""
    datos = json.loads((METRICS_DIR / "baseline_tfidf_valid.json").read_text(encoding="utf-8"))
    t = pd.DataFrame({r: {"f1_macro": m["f1_macro"], "f1_bug": m["f1_bug"],
                          "f1_feature": m["f1_feature"], "f1_question": m["f1_question"]}
                      for r, m in datos["por_repo"].items()}).T.sort_values("f1_macro")
    t.to_csv(ERRORS_DIR / "p2_f1_por_repo.csv")
    mostrar(t, "P2 F1 por repo (menor = mas dificil)")


def p3_palabras(train):
    """P3. Las 10 palabras con mas peso por clase y repo (modelo entrenado solo con train)."""
    filas = []
    for repo, g in train.groupby("repo"):
        m = build_pipeline(1.0, None).fit(g["text"], g["label"])
        vocab = m.named_steps["tfidf"].get_feature_names_out()
        coef = m.named_steps["clf"].coef_
        for i, clase in enumerate(m.named_steps["clf"].classes_):
            for idx in np.argsort(coef[i])[-10:][::-1]:
                filas.append({"repo": repo, "clase": clase, "palabra": vocab[idx],
                              "peso": round(float(coef[i][idx]), 3)})
    t = pd.DataFrame(filas)
    t.to_csv(ERRORS_DIR / "p3_palabras_fuertes.csv", index=False)
    print("\n== P3 palabras con mas peso (primeras filas) ==")
    print(t.head(15).to_string(index=False))


def p4_longitud(pred, train):
    """P4. Acierto por cuartil de longitud del texto limpio."""
    t = train.sort_values("repo", kind="stable").reset_index(drop=True)
    assert (t["label"].values == pred["label"].values).all(), "El orden de pred y train no coincide"
    pred = pred.assign(longitud=t["text"].str.len().values)
    pred["cuartil"] = pd.qcut(pred["longitud"], 4, labels=["Q1 (más corto)", "Q2", "Q3", "Q4 (más largo)"])
    pred["acierto"] = (pred["label"] == pred["pred"]).astype(int)
    res = pred.groupby("cuartil", observed=True).agg(
        issues=("acierto", "size"), acierto=("acierto", "mean"),
        long_min=("longitud", "min"), long_max=("longitud", "max"))
    res.to_csv(ERRORS_DIR / "p4_acierto_por_longitud.csv")
    mostrar(res, "P4 acierto por cuartil de longitud")
    ax = res["acierto"].mul(100).plot(kind="bar", figsize=(6.5, 4))
    ax.set_title("Porcentaje de acierto por cuartil de longitud del texto (validación)")
    ax.set_xlabel("Cuartil de longitud")
    ax.set_ylabel("% de acierto")
    ax.bar_label(ax.containers[0], fmt="%.1f %%", padding=2)  # valor sobre cada barra
    ax.margins(y=0.12)
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "errores_acierto_por_longitud.png", dpi=150)
    plt.close()


def p5_fuga_plantilla(train):
    """P5. ¿Depende el modelo de la plantilla? Mismo CV con y sin encabezados '### ...'."""
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)
    res = {}
    for nombre, f in (("con_plantilla", lambda s: s),
                      ("sin_encabezados", lambda s: RE_ENCABEZADO.sub(" ", s))):
        filas = []
        for repo, g in train.groupby("repo"):
            textos = g["text"].map(f)
            pred = cross_val_predict(build_pipeline(1.0, None), textos, g["label"], cv=cv)
            filas.append(g.assign(pred=pred))
        res[nombre] = evaluate(pd.concat(filas))
    tabla = pd.DataFrame({k: {**{r: v["por_repo"][r]["f1_macro"] for r in v["por_repo"]},
                              "PROMEDIO": v["f1_promedio_repos"]} for k, v in res.items()})
    tabla["diferencia"] = tabla["sin_encabezados"] - tabla["con_plantilla"]
    tabla.to_csv(ERRORS_DIR / "p5_fuga_plantilla.csv")
    mostrar(tabla, "P5 F1 con y sin encabezados de plantilla (validacion)")
    save_metrics("fuga_sin_plantilla", {"f1_promedio_con_plantilla": res["con_plantilla"]["f1_promedio_repos"],
                                        "f1_promedio_sin_encabezados": res["sin_encabezados"]["f1_promedio_repos"]},
                 extra={"seed": SEED, "split": "valid", "nota": "experimento propio; no es el modelo oficial"})


def p6_solapamiento():
    """P6. Issues identicos en train y test, y si el baseline oficial los acierta en test."""
    tr, te = pd.read_csv(TRAIN_RAW), pd.read_csv(TEST_RAW)
    llaves = ["repo", "title", "body"]
    # drop_duplicates evita contar doble un issue que esta repetido DENTRO de train
    comunes = te.merge(tr[llaves + ["label"]].drop_duplicates(subset=llaves), on=llaves,
                       suffixes=("_test", "_train"))
    print(f"\n== P6 issues identicos en train y test: {len(comunes)} ==")
    out = {"repetidos_train_test": int(len(comunes)),
           "misma_etiqueta_en_train_y_test": int((comunes["label_test"] == comunes["label_train"]).sum())}
    ruta = ERRORS_DIR / "pred_baseline_tfidf_test.csv"
    if len(comunes) and ruta.exists():
        # pred_*_test.csv conserva el orden del test agrupado por repo: alineamos por posicion
        te_ord = te.sort_values("repo", kind="stable").reset_index(drop=True)
        pt = pd.read_csv(ruta)
        assert (te_ord["label"].values == pt["label"].values).all(), "El orden de pred y test no coincide"
        claves_comunes = set(zip(comunes["repo"], comunes["title"], comunes["body"]))
        mask = [(r, t, b) in claves_comunes for r, t, b in zip(te_ord["repo"], te_ord["title"], te_ord["body"])]
        sel = pt[mask]
        out["filas_de_test_repetidas_en_train"] = int(len(sel))
        out["acertadas_por_el_baseline_oficial"] = int((sel["label"] == sel["pred"]).sum())
    (ERRORS_DIR / "p6_solapamiento.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(out)


def p7_errores_concretos(pred, train):
    """P7. 10 errores al azar por repo (semilla 42) para explicarlos a mano."""
    t = train.sort_values("repo", kind="stable").reset_index(drop=True)
    pred = pred.assign(largo_texto=t["text"].str.len().values)
    mal = pred[pred.label != pred.pred]
    partes = [g.sample(min(10, len(g)), random_state=SEED) for _, g in mal.groupby("repo")]
    muestra = pd.concat(partes).assign(explicacion_tuya="")  # concat conserva la columna repo
    # Se llama pred_* para que .gitignore lo excluya (contiene titulos del dataset).
    muestra.to_csv(ERRORS_DIR / "pred_errores_concretos.csv", index=False)
    print(f"\n== P7 {len(muestra)} errores guardados en reports/errores/pred_errores_concretos.csv "
          "(llena la columna explicacion_tuya a mano) ==")


def main():
    ERRORS_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    ruta = ERRORS_DIR / "pred_baseline_tfidf_valid.csv"
    if not ruta.exists():
        raise SystemExit("Falta pred_baseline_tfidf_valid.csv. Corre: python -m src.models.baseline_tfidf --split valid")
    pred = pd.read_csv(ruta)
    train = pd.read_csv(DATA_PROCESSED / "train_clean.csv").fillna({"text": ""})
    p1_confusion(pred)
    p2_repo_dificil()
    p3_palabras(train)
    p4_longitud(pred, train)
    p5_fuga_plantilla(train)
    p6_solapamiento()
    p7_errores_concretos(pred, train)
    print("\n[OK] Tablas en reports/errores/, figuras en reports/figures/")


if __name__ == "__main__":
    main()
