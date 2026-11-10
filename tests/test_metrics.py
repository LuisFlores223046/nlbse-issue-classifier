"""Pruebas de src/metrics.py (Gabriel las amplia). Correr: pytest -q"""

import json

import pandas as pd
import pytest

from src.metrics import evaluate, save_metrics


def _df(real, pred, repo="x"):
    return pd.DataFrame({"repo": repo, "label": real, "pred": pred})


def test_prediccion_perfecta_da_f1_uno():
    d = _df(["bug", "feature", "question"], ["bug", "feature", "question"])
    r = evaluate(d)
    assert r["f1_promedio_repos"] == pytest.approx(1.0)


def test_todo_mal_da_f1_cero():
    d = _df(["bug", "feature", "question"], ["feature", "question", "bug"])
    assert evaluate(d)["f1_promedio_repos"] == pytest.approx(0.0)


def test_promedio_es_promedio_simple_de_repos():
    perfecto = _df(["bug", "feature", "question"], ["bug", "feature", "question"], "a")
    malo = _df(["bug", "feature", "question"], ["feature", "question", "bug"], "b")
    r = evaluate(pd.concat([perfecto, malo]))
    assert r["f1_promedio_repos"] == pytest.approx(0.5)  # (1.0 + 0.0) / 2


def test_save_metrics_escribe_json(tmp_path, monkeypatch):
    import src.metrics as m
    monkeypatch.setattr(m, "METRICS_DIR", tmp_path)  # escribir en carpeta temporal
    ruta = save_metrics("demo", {"f1_promedio_repos": 0.5}, extra={"seed": 42})
    datos = json.loads(ruta.read_text(encoding="utf-8"))
    assert datos["modelo"] == "demo" and datos["seed"] == 42
