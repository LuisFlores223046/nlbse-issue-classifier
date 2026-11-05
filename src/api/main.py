"""
main.py  (API, responsable: Luis)
=================================
Prototipo FastAPI.  Arrancar con:
    uvicorn src.api.main:app --reload
y abrir http://127.0.0.1:8000/docs  (documentacion interactiva automatica)

Contrato (tambien en docs/api_contract.md):
  GET  /health   -> {"status": "ok"}
  POST /predict  {title, body, repo?} -> {label, probabilities, model_version}
"""

from fastapi import FastAPI, HTTPException  # FastAPI = el framework; HTTPException = errores HTTP
from pydantic import BaseModel, Field        # BaseModel valida automaticamente el JSON de entrada

from src.config import MODEL_VERSION, REPOS
from src.predict import predict_issue

app = FastAPI(title="Clasificador de issues de GitHub", version=MODEL_VERSION)


class IssueIn(BaseModel):
    """Lo que ENVIA el usuario."""
    title: str = Field(..., min_length=1, description="Titulo del issue")
    body: str = Field("", description="Cuerpo del issue (puede ir vacio)")
    repo: str = Field("facebook/react", description="Modelo de que repo usar")


class PredictionOut(BaseModel):
    """Lo que DEVUELVE la API."""
    label: str
    probabilities: dict
    model_version: str


@app.get("/health")
def health():
    """Para comprobar que la API esta viva."""
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionOut)
def predict(issue: IssueIn):
    """Clasifica un issue como bug / feature / question."""
    if issue.repo not in REPOS:
        # 422 = "tu peticion esta bien formada pero el valor no es valido"
        raise HTTPException(status_code=422, detail=f"repo debe ser uno de {REPOS}")
    try:
        label, probs = predict_issue(issue.title, issue.body, issue.repo)
    except FileNotFoundError:
        # 503 = "servicio no disponible todavia": faltan los .joblib (no se ha entrenado)
        raise HTTPException(status_code=503, detail="Modelo no entrenado. Corre el baseline con --split test.")
    return PredictionOut(label=label, probabilities=probs, model_version=MODEL_VERSION)
