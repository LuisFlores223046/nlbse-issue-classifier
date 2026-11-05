"""Pruebas de la API (Luis). No necesitan modelo entrenado: probamos tambien los errores."""

import pytest

fastapi = pytest.importorskip("fastapi")  # si no esta instalado, se salta
from fastapi.testclient import TestClient  # noqa: E402

from src.api.main import app  # noqa: E402

client = TestClient(app)  # cliente falso que llama a la API sin levantar servidor


def test_health():
    r = client.get("/health")
    assert r.status_code == 200 and r.json() == {"status": "ok"}


def test_repo_invalido_da_422():
    r = client.post("/predict", json={"title": "x", "body": "y", "repo": "no/existe"})
    assert r.status_code == 422


def test_titulo_vacio_da_422():
    r = client.post("/predict", json={"title": "", "body": "y"})
    assert r.status_code == 422


def test_predict_sin_modelo_da_503_o_200():
    # Sin .joblib -> 503; con modelos entrenados -> 200 y estructura correcta.
    r = client.post("/predict", json={"title": "App crashes on start", "body": "stack trace"})
    assert r.status_code in (200, 503)
    if r.status_code == 200:
        j = r.json()
        assert j["label"] in ("bug", "feature", "question")
        assert abs(sum(j["probabilities"].values()) - 1.0) < 1e-6
