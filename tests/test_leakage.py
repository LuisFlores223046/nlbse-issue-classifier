"""Fuga de datos: ningun issue de TEST debe estar tambien en TRAIN (misma fuente de verdad)."""

import pandas as pd
import pytest

from src.config import TEST_RAW, TRAIN_RAW

# Hallazgo real (04-nov-2026): el dataset oficial trae unos pocos issues repetidos entre
# train y test. Fijamos el MAXIMO tolerado; si sube, algo se rompio. Documentar en docs/decisiones.md.
MAX_SOLAPAMIENTO_TOLERADO = 5


def _clave(df):
    return df["repo"] + "||" + df["title"].fillna("") + "||" + df["body"].fillna("")


def test_solapamiento_train_test_es_minimo():
    if not (TRAIN_RAW.exists() and TEST_RAW.exists()):
        pytest.skip("Datos no descargados")
    solapados = set(_clave(pd.read_csv(TRAIN_RAW))) & set(_clave(pd.read_csv(TEST_RAW)))
    assert len(solapados) <= MAX_SOLAPAMIENTO_TOLERADO, f"{len(solapados)} issues en ambos"
