"""
make_dataset.py  (responsable: Rogelio)
=======================================
Pipeline de datos:  data/raw  ->  validar  ->  limpiar  ->  data/processed

Se corre asi (desde la raiz del repo):
    python -m src.data.make_dataset

Genera:
  data/processed/train_clean.csv
  data/processed/test_clean.csv
  reports/data_quality/resumen_calidad.json   (conteos, nulos, duplicados ANTES y DESPUES + validacion)

Sigue los 5 pasos de la guia del profesor: 1 inspeccion, 2 deteccion, 3 decision,
4 transformacion, 5 validacion (ver docs/decisiones_limpieza.md).
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


def validate_clean(df, nombre, filas_esperadas):
    """PASO 5 (validacion): comprueba el DataFrame DESPUES de limpiar.

    Entrada : df limpio (con columna `text`), nombre ("train"/"test") y filas esperadas.
    Salida  : diccionario con cada comprobacion (True/False) y datos de apoyo.
    Por que : la guia pide verificar que la limpieza no introdujo errores:
              comparar filas antes/despues y revisar nulos y duplicados que queden.
    Si falla algo critico (nulos, etiquetas raras, filas inesperadas) lanza ValueError.
    """
    comprobaciones = {
        "filas_ok": bool(len(df) == filas_esperadas),
        "sin_nulos_en_title_body_text": bool(df[["title", "body", "text"]].isna().sum().sum() == 0),
        "etiquetas_validas": bool(set(df["label"]) <= set(LABELS)),
        "repos_validos": bool(set(df["repo"]) <= set(REPOS)),
        "sin_urls_ni_comentarios_html": bool(
            not df["text"].str.contains(r"https?://|<!--", regex=True).any()),
        "issues_con_texto_vacio": int((df["text"].str.replace(".", "", regex=False).str.strip() == "").sum()),
    }
    if nombre == "train":  # solo train se deduplica (protocolo: el test no se toca)
        comprobaciones["sin_duplicados_exactos"] = bool(
            not df.duplicated(subset=["repo", "title", "body"]).any())
    criticas = ["filas_ok", "sin_nulos_en_title_body_text", "etiquetas_validas", "repos_validos"]
    malas = [c for c in criticas if not comprobaciones[c]]
    if malas:
        raise ValueError(f"Validacion fallida en {nombre}: {malas}")
    return comprobaciones


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
        resumen[f"{nombre}_despues"] = quality_summary(df, f"{nombre}_clean.csv")  # 5) medir DESPUES
        filas_antes = resumen[f"{nombre}_antes"]["filas"]
        resumen[f"{nombre}_validacion"] = validate_clean(df, nombre, filas_antes - quitados)
        salida = DATA_PROCESSED / f"{nombre}_clean.csv"
        df.to_csv(salida, index=False)                        # 4) guardar
        print(f"[OK] {salida.name}: {len(df)} filas ({quitados} duplicados quitados)")

    ruta_json = QUALITY_DIR / "resumen_calidad.json"
    ruta_json.write_text(json.dumps(resumen, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[OK] {ruta_json}")


if __name__ == "__main__":  # solo corre main() si ejecutas este archivo directamente
    main()
