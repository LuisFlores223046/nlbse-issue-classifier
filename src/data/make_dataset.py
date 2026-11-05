"""
make_dataset.py  (responsable: Rogelio)
=======================================
Pipeline de datos:  data/raw  ->  validar  ->  limpiar  ->  data/processed

Se corre asi (desde la raiz del repo):
    python -m src.data.make_dataset

Genera:
  data/processed/train_clean.csv
  data/processed/test_clean.csv
  reports/data_quality/resumen_calidad.json   (conteos, nulos, duplicados)
"""

import json  # para guardar el resumen de calidad

import pandas as pd

from src.config import (COLUMNS, DATA_PROCESSED, LABELS, QUALITY_DIR, REPOS,
                        TEST_RAW, TRAIN_RAW)
from src.data.clean import clean_dataframe, drop_duplicates_report


def load_raw(path):
    """Lee un CSV crudo y VALIDA que tenga el esquema esperado.

    Si algo no cuadra, lanza un error claro (mejor fallar aqui que entrenar con basura).
    """
    if not path.exists():
        raise FileNotFoundError(
            f"No existe {path}. Corre primero:  python scripts/download_data.py")
    df = pd.read_csv(path)  # el CSV usa comillas para cuerpos con saltos de linea; pandas lo maneja
    if list(df.columns) != COLUMNS:
        raise ValueError(f"Columnas inesperadas: {list(df.columns)} (esperaba {COLUMNS})")
    etiquetas_raras = set(df["label"]) - set(LABELS)
    if etiquetas_raras:
        raise ValueError(f"Etiquetas no esperadas: {etiquetas_raras}")
    repos_raros = set(df["repo"]) - set(REPOS)
    if repos_raros:
        raise ValueError(f"Repos no esperados: {repos_raros}")
    return df


def quality_summary(df, nombre):
    """Devuelve un diccionario con metricas de calidad de un DataFrame."""
    return {
        "archivo": nombre,
        "filas": int(len(df)),
        "nulos_por_columna": {c: int(v) for c, v in df.isna().sum().items()},
        "duplicados_exactos": int(df.duplicated(subset=["repo", "title", "body"]).sum()),
        "conteo_repo_label": {f"{r}|{l}": int(n)
                              for (r, l), n in df.groupby(["repo", "label"]).size().items()},
        "longitud_body_mediana": float(df["body"].fillna("").str.len().median()),
        "longitud_body_max": int(df["body"].fillna("").str.len().max()),
    }


def main():
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    QUALITY_DIR.mkdir(parents=True, exist_ok=True)

    resumen = {}
    for nombre, ruta in (("train", TRAIN_RAW), ("test", TEST_RAW)):
        df = load_raw(ruta)                                   # 1) leer + validar
        resumen[f"{nombre}_antes"] = quality_summary(df, ruta.name)  # 2) medir ANTES
        df, quitados = drop_duplicates_report(df) if nombre == "train" else (df, 0)
        # OJO: al test NO le quitamos filas (protocolo NLBSE: no remuestrear el test).
        df = clean_dataframe(df)                              # 3) limpiar texto
        resumen[f"{nombre}_duplicados_quitados"] = quitados
        salida = DATA_PROCESSED / f"{nombre}_clean.csv"
        df.to_csv(salida, index=False)                        # 4) guardar
        print(f"[OK] {salida.name}: {len(df)} filas ({quitados} duplicados quitados)")

    ruta_json = QUALITY_DIR / "resumen_calidad.json"
    ruta_json.write_text(json.dumps(resumen, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[OK] {ruta_json}")


if __name__ == "__main__":  # solo corre main() si ejecutas este archivo directamente
    main()
