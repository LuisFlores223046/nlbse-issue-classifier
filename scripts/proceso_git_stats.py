"""
proceso_git_stats.py  (responsable: Gabriel)
============================================
ANALITICA DE NUESTRO PROPIO PROCESO (rubrica, criterio 3: "analitica de requerimientos y
procesos" y trazabilidad). Lee el historial de git y calcula metricas del equipo:
  - commits por persona y por dia
  - archivos tocados por persona
Genera CSV en reports/proceso/ que se interpretan en el reporte (Cap. 4).

Uso (desde la raiz del repo, con el repo ya clonado):
    python scripts/proceso_git_stats.py

No necesita internet: solo el comando `git log`.
"""

import subprocess  # para ejecutar el comando git desde Python
import sys
from io import StringIO
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.config import REPORTS  # noqa: E402

SALIDA = REPORTS / "proceso"


def leer_log():
    """Devuelve un DataFrame con un renglon por commit: hash, autor, fecha, mensaje, n_archivos."""
    # --numstat lista los archivos tocados; el separador "|" nos deja partir los campos.
    fmt = "--pretty=format:@@%H|%an|%ad|%s"
    out = subprocess.run(["git", "log", fmt, "--date=short", "--numstat"],
                         capture_output=True, text=True, encoding="utf-8", check=True).stdout
    filas, actual = [], None
    for linea in out.splitlines():
        if linea.startswith("@@"):                 # encabezado de un commit
            h, autor, fecha, msg = linea[2:].split("|", 3)
            actual = {"hash": h[:7], "autor": autor, "fecha": fecha, "mensaje": msg, "archivos": 0}
            filas.append(actual)
        elif linea.strip() and actual is not None:  # linea de archivo tocado
            actual["archivos"] += 1
    return pd.DataFrame(filas)


def main():
    df = leer_log()
    if df.empty:
        print("No hay commits todavia.")
        return
    SALIDA.mkdir(parents=True, exist_ok=True)
    por_persona = df.groupby("autor").agg(commits=("hash", "count"),
                                          archivos_tocados=("archivos", "sum")).reset_index()
    por_dia = df.groupby(["fecha", "autor"]).size().unstack(fill_value=0)
    por_persona.to_csv(SALIDA / "commits_por_persona.csv", index=False)
    por_dia.to_csv(SALIDA / "commits_por_dia.csv")
    df.to_csv(SALIDA / "historial_commits.csv", index=False)
    print(por_persona.to_string(index=False))
    print(f"\nGuardado en {SALIDA}")


if __name__ == "__main__":
    main()
