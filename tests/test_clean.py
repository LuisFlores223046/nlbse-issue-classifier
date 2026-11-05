"""Pruebas de la limpieza de texto (Rogelio las amplia). Correr: pytest -q"""

import pandas as pd

from src.data.clean import clean_dataframe, clean_text, drop_duplicates_report


def test_texto_vacio_devuelve_cadena_vacia():
    # NaN y None no deben romper nada
    assert clean_text(None) == ""
    assert clean_text(float("nan")) == ""


def test_quita_comentarios_html_y_urls():
    t = "Hola <!-- oculto --> mira https://example.com/x ya"
    out = clean_text(t)
    assert "oculto" not in out
    assert "https" not in out
    assert "URL" in out


def test_bloque_codigo_se_reemplaza():
    assert "CODEBLOCK" in clean_text("antes ```print(1)``` despues")


def test_colapsa_espacios():
    assert clean_text("a   b\n\n c") == "a b c"


def test_clean_dataframe_crea_text_y_no_toca_original():
    df = pd.DataFrame({"repo": ["x"], "created_at": ["2020"], "label": ["bug"],
                       "title": ["Titulo"], "body": [None]})
    out = clean_dataframe(df)
    assert out.loc[0, "text"].startswith("Titulo")
    assert pd.isna(df.loc[0, "body"])  # el original sigue intacto


def test_duplicados_se_reportan():
    df = pd.DataFrame({"repo": ["x", "x"], "title": ["a", "a"], "body": ["b", "b"]})
    limpio, n = drop_duplicates_report(df)
    assert len(limpio) == 1 and n == 1
