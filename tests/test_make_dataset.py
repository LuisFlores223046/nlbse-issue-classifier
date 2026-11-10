"""Pruebas de la validacion posterior a la limpieza (paso 5 de la guia del profesor)."""

import pandas as pd
import pytest

from src.data.clean import clean_dataframe, drop_duplicates_report
from src.data.make_dataset import quality_summary, validate_clean


def _df():
    # Mini-dataset de juguete: 1 duplicado exacto, 1 body vacio y 1 URL.
    return pd.DataFrame({
        "repo": ["facebook/react"] * 4,
        "created_at": ["2020-01-01"] * 4,
        "label": ["bug", "bug", "feature", "question"],
        "title": ["Falla", "Falla", "Idea", "Duda"],
        "body": ["ver https://x.com/a", "ver https://x.com/a", None, "texto <!-- oculto -->"],
    })


def test_validate_clean_ok_despues_de_limpiar():
    df, quitados = drop_duplicates_report(_df())
    limpio = clean_dataframe(df)
    res = validate_clean(limpio, "train", filas_esperadas=len(_df()) - quitados)
    assert quitados == 1
    assert res["filas_ok"] and res["sin_duplicados_exactos"]
    assert res["sin_urls_ni_comentarios_html"]


def test_validate_clean_detecta_filas_inesperadas():
    limpio = clean_dataframe(_df())
    with pytest.raises(ValueError):
        validate_clean(limpio, "test", filas_esperadas=99)


def test_quality_summary_cuenta_nulos_y_duplicados():
    r = quality_summary(_df(), "demo.csv")
    assert r["filas"] == 4
    assert r["duplicados_exactos"] == 1
    assert r["nulos_por_columna"]["body"] == 1
