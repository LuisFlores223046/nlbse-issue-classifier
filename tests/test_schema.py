"""Valida el esquema de los CSV crudos. Se SALTA si aun no se descargaron."""

import pandas as pd
import pytest

from src.config import COLUMNS, LABELS, REPOS, TEST_RAW, TRAIN_RAW


@pytest.mark.parametrize("ruta", [TRAIN_RAW, TEST_RAW])
def test_esquema_csv(ruta):
    if not ruta.exists():
        pytest.skip("Datos no descargados: python scripts/download_data.py")
    df = pd.read_csv(ruta)
    assert list(df.columns) == COLUMNS
    assert set(df["label"]) <= set(LABELS)
    assert set(df["repo"]) == set(REPOS)
    assert len(df) == 1500  # 5 repos x 3 clases x 100 por mitad (train/test)
