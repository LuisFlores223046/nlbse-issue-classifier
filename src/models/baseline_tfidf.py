"""
baseline_tfidf.py  (responsable: Sebastian)
===========================================
Modelo BASE: TF-IDF + Regresion Logistica, un clasificador por repo.
Es rapido (segundos, sin GPU) y deja el proyecto con resultados reales desde el dia 1.
Los modelos "bonitos" (SetFit, RoBERTa) se comparan CONTRA este.

Uso (desde la raiz del repo):
    python -m src.models.baseline_tfidf --split valid     # validacion cruzada SOLO con train
    python -m src.models.baseline_tfidf --split test      # evaluacion final en test (UNA vez!)

REGLA DE ORO: el test se usa UNA sola vez por modelo final. Para ajustar
hiperparametros usa --split valid.
"""

import argparse

import joblib  # guardar/cargar modelos entrenados
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_predict, StratifiedKFold
from sklearn.pipeline import Pipeline

from src.config import DATA_PROCESSED, ERRORS_DIR, MODELS_DIR, MODEL_VERSION, SEED
from src.metrics import evaluate, save_metrics


def build_pipeline(C=1.0, class_weight=None):
    """Crea el pipeline: texto -> TF-IDF -> regresion logistica.

    TF-IDF convierte texto en numeros (que palabras importan en cada issue).
    ngram_range=(1,2): usa palabras sueltas y pares de palabras.
    C: fuerza de regularizacion (mas chico = modelo mas simple).
    class_weight: None (todas las clases pesan igual) o "balanced" (da mas peso a las clases
                  menos frecuentes; el dataset ya esta balanceado, pero se prueba y se documenta).
    """
    return Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True,
                                  max_features=50_000)),
        ("clf", LogisticRegression(C=C, max_iter=1000, random_state=SEED,
                                   class_weight=class_weight)),
    ])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", choices=["valid", "test"], default="valid")
    ap.add_argument("--C", type=float, default=1.0)
    ap.add_argument("--balanced", action="store_true", help="usar class_weight='balanced'")
    ap.add_argument("--tag", default="", help="sufijo para NO sobrescribir el baseline oficial (ej. C3)")
    args = ap.parse_args()
    cw = "balanced" if args.balanced else None  # None = comportamiento por defecto

    train = pd.read_csv(DATA_PROCESSED / "train_clean.csv").fillna({"text": ""})
    resultados_filas = []   # aqui juntamos las predicciones de los 5 repos

    if args.split == "valid":
        # Validacion cruzada 5 pliegues DENTRO del train (el test ni se toca).
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)
        for repo, g in train.groupby("repo"):
            pred = cross_val_predict(build_pipeline(args.C, cw), g["text"], g["label"], cv=cv)
            resultados_filas.append(g.assign(pred=pred))
        nombre = "baseline_tfidf_valid" + (f"_{args.tag}" if args.tag else "")
    else:
        test = pd.read_csv(DATA_PROCESSED / "test_clean.csv").fillna({"text": ""})
        MODELS_DIR.mkdir(parents=True, exist_ok=True)
        for repo, g_tr in train.groupby("repo"):
            modelo = build_pipeline(args.C, cw).fit(g_tr["text"], g_tr["label"])  # entrena SOLO con train del repo
            g_te = test[test["repo"] == repo]
            resultados_filas.append(g_te.assign(pred=modelo.predict(g_te["text"])))
            nombre_archivo = repo.replace("/", "__")  # "facebook/react" -> "facebook__react"
            joblib.dump(modelo, MODELS_DIR / (f"{nombre_archivo}.joblib" if not args.tag else f"{nombre_archivo}__{args.tag}.joblib"))
        nombre = "baseline_tfidf_test" + (f"_{args.tag}" if args.tag else "")

    df = pd.concat(resultados_filas)
    # Guardamos TODAS las predicciones fila por fila: Gabriel las usa para el analisis de errores.
    ERRORS_DIR.mkdir(parents=True, exist_ok=True)
    df[["repo", "label", "pred", "title"]].to_csv(ERRORS_DIR / f"pred_{nombre}.csv", index=False)
    res = evaluate(df)
    ruta = save_metrics(nombre, res, extra={"C": args.C, "class_weight": cw, "seed": SEED,
                                            "split": args.split, "model_version": MODEL_VERSION})
    print(f"F1 promedio ({args.split}): {res['f1_promedio_repos']:.4f}")
    for repo, m in res["por_repo"].items():
        print(f"  {repo:24s} F1 macro = {m['f1_macro']:.4f}")
    print(f"Metricas guardadas en {ruta}")


if __name__ == "__main__":
    main()
