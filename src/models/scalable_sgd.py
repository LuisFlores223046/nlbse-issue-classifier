"""
scalable_sgd.py  (responsable: Sebastian)
=========================================
Segundo modelo: tecnica ESCALABLE (estilo "Big Data") con scikit-learn.

Idea: con millones de issues, el texto no cabe en memoria ni se puede ajustar un
TF-IDF global. Esta variante usa:
  * HashingVectorizer: convierte texto en numeros SIN guardar vocabulario (memoria constante).
  * SGDClassifier + partial_fit: aprende por LOTES (chunks), viendo pocos datos a la vez.
Con 1 500 issues no hace falta, pero demostramos la tecnica y medimos su costo/beneficio
contra el baseline (tecnica escalable tipo Big Data: memoria constante por lotes).

Uso (desde la raiz del repo):
    python -m src.models.scalable_sgd --split valid
    python -m src.models.scalable_sgd --split test      # UNA vez, solo con el modelo final
"""

import argparse
import time  # para medir cuanto tarda entrenar (analisis de rendimiento)

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import StratifiedKFold

from src.config import DATA_PROCESSED, ERRORS_DIR, LABELS, MODEL_VERSION, SEED
from src.metrics import evaluate, save_metrics

# 2**18 columnas: suficientes para evitar muchas colisiones sin gastar memoria.
N_FEATURES = 2 ** 18
CHUNK = 200  # cuantos issues se procesan por lote


def _vectorizador():
    """HashingVectorizer sin estado: no necesita 'fit', por eso sirve para flujos de datos."""
    return HashingVectorizer(n_features=N_FEATURES, ngram_range=(1, 2),
                             alternate_sign=False)  # alternate_sign=False -> valores >= 0


def entrenar_por_lotes(textos, etiquetas, class_weight=None, epocas=5):
    """Entrena un SGDClassifier viendo los datos de CHUNK en CHUNK.

    Entrada : lista de textos y lista de etiquetas.
    Salida  : (modelo, vectorizador).
    Por que : partial_fit permite aprender sin cargar todo el dataset a la vez.
    """
    vec = _vectorizador()
    # loss="log_loss" da probabilidades (necesarias para la API y para F1 por clase).
    clf = SGDClassifier(loss="log_loss", alpha=1e-5, class_weight=class_weight,
                        random_state=SEED)
    rng = np.random.RandomState(SEED)
    textos = np.asarray(textos, dtype=object)
    etiquetas = np.asarray(etiquetas, dtype=object)
    for _ in range(epocas):                      # varias pasadas por los datos
        orden = rng.permutation(len(textos))     # barajar en cada epoca
        for i in range(0, len(orden), CHUNK):
            idx = orden[i:i + CHUNK]
            X = vec.transform(textos[idx])       # texto -> matriz dispersa
            clf.partial_fit(X, etiquetas[idx], classes=LABELS)  # aprende este lote
    return clf, vec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", choices=["valid", "test"], default="valid")
    ap.add_argument("--balanced", action="store_true", help="usar class_weight='balanced'")
    args = ap.parse_args()
    cw = "balanced" if args.balanced else None

    train = pd.read_csv(DATA_PROCESSED / "train_clean.csv").fillna({"text": ""})
    filas = []
    t0 = time.perf_counter()  # cronometro: entrenamiento total
    if args.split == "valid":
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)
        for repo, g in train.groupby("repo"):
            g = g.reset_index(drop=True)
            pred = np.empty(len(g), dtype=object)
            for tr_i, va_i in cv.split(g["text"], g["label"]):
                clf, vec = entrenar_por_lotes(g.loc[tr_i, "text"], g.loc[tr_i, "label"], cw)
                pred[va_i] = clf.predict(vec.transform(g.loc[va_i, "text"]))
            filas.append(g.assign(pred=pred))
        nombre = "scalable_sgd_valid"
    else:
        test = pd.read_csv(DATA_PROCESSED / "test_clean.csv").fillna({"text": ""})
        for repo, g_tr in train.groupby("repo"):
            clf, vec = entrenar_por_lotes(g_tr["text"], g_tr["label"], cw)
            g_te = test[test["repo"] == repo]
            filas.append(g_te.assign(pred=clf.predict(vec.transform(g_te["text"]))))
        nombre = "scalable_sgd_test"
    segundos = time.perf_counter() - t0

    df = pd.concat(filas)
    ERRORS_DIR.mkdir(parents=True, exist_ok=True)
    df[["repo", "label", "pred", "title"]].to_csv(ERRORS_DIR / f"pred_{nombre}.csv", index=False)
    res = evaluate(df)
    save_metrics(nombre, res, extra={"class_weight": cw, "seed": SEED, "n_features": N_FEATURES,
                                     "chunk": CHUNK, "segundos_entrenamiento": round(segundos, 2),
                                     "model_version": MODEL_VERSION})
    print(f"F1 promedio ({args.split}): {res['f1_promedio_repos']:.4f}  ({segundos:.1f} s)")
    for repo, m in res["por_repo"].items():
        print(f"  {repo:24s} F1 macro = {m['f1_macro']:.4f}")


if __name__ == "__main__":
    main()
