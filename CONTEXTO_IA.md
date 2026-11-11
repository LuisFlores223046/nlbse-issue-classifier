# CONTEXTO_IA.md — Léelo completo antes de ayudar con CUALQUIER cosa de este proyecto

> Para la IA (Claude, ChatGPT, Copilot, Gemini, etc.): este archivo te dice el contexto, las reglas y cómo debes trabajar con el equipo. Si algo de lo que te pide el usuario choca con estas reglas, **avísale** en vez de hacerlo en silencio.
> Para el humano: pega este archivo completo al inicio de tu chat con la IA, o ponlo en la raíz del repo (si usas Claude Code, renómbralo `CLAUDE.md`; si usas Copilot/Codex, `AGENTS.md`).

---

## 1. Qué es el proyecto
- Proyecto final de **Tópicos Selectos de Ingeniería de Software** (UACJ, 9º semestre). Equipo de 5: **Luis** (coordinación, repo, API), **Rogelio** (datos y limpieza), **Sebastián** (modelos), **Gabriel** (analítica, métricas, calidad), **Evelyn** (documentación, trazabilidad, reporte).
- Tema: **clasificar issues de GitHub en `bug` / `feature` / `question`** con aprendizaje automático, usando el dataset oficial **NLBSE'24** (5 repos: facebook/react, tensorflow/tensorflow, microsoft/vscode, bitcoin/bitcoin, opencv/opencv). Además: análisis de errores (analítica de software) y un prototipo **FastAPI**.
- Fechas: arranque 4-nov-2026; entrega **miércoles 11-nov-2026** (fijada por el profesor). Meta interna: todo terminado el **martes 10 a las 22:00**; resultados congelados el **lunes 9 a las 20:00**. Calendario en `guias/06_Calendario_dia_por_dia.md`.
- **Lo que más valora el profesor: la TRAZABILIDAD** (poder seguir cada requisito hasta su código, prueba, resultado y sección del reporte), el uso honesto de fuentes y de IA, y que las conclusiones salgan de evidencia real.

## 1b. Qué pide el profesor (SOLO estas tres fuentes: el aviso, la guía HTML y el reporte de ejemplo)
- **Estructura del reporte (aviso §3):** Cap. 1 Introducción · Cap. 2 Marco teórico y revisión de la literatura · Cap. 3 Metodología y desarrollo técnico · Cap. 4 Implementación, análisis y resultados · Cap. 5 Conclusiones y trabajo futuro · Referencias · Anexos. Plantilla: `reporte/plantilla_reporte.md`. El estilo se toma del reporte de ejemplo (`bookdown-demo.pdf`): secciones numeradas, código explicado, figuras con pie, conclusiones por integrante.
- **Código (aviso §4):** cada función/procedimiento importante se explica con 6 puntos: objetivo, entradas, cómo funciona, salidas, por qué así, cómo contribuye al objetivo. Ver `docs/explicacion_codigo.md`.
- **Resultados (aviso §5):** cada tabla/figura con título descriptivo, explicación e interpretación. **No inventar** resultados, métricas, pruebas, datos ni afirmaciones.
- **Fuentes e IA (aviso §6):** referencias confiables y verificables; la IA se puede usar pero se **documenta** y se **contrasta** con evidencia; nunca como resultado experimental ni como fuente verificada.
- **Calidad (aviso §7):** ver `docs/checklist_calidad.md`.
- **Guía oficial (aviso §8):** el aviso dice que además hay que cumplir la guía oficial de la materia (pruebas, control de versiones, presentación final, etc.). Aquí **solo** se trabaja con las tres fuentes de arriba; lo que dependa de la guía oficial se pregunta al profesor (guía 08) y mientras tanto se marca como opcional.
- **Limpieza (guía HTML §2):** pasos inspección → detección → decisión → transformación → validación, y 6 puntos documentados (fuente, diagnóstico, procedimiento, herramientas y código, antes/después, validación). Ver `docs/decisiones_limpieza.md`.
- **Ficha de 10 preguntas (guía HTML §5):** `reporte/ficha_10_preguntas.md`.
- **El profesor dijo: "el mayor enfoque es trazabilidad".**

## 2. Datos (hechos verificados el 4-nov-2026 — no los "corrijas" de memoria)
- Columnas REALES del CSV: `repo, created_at, label, title, body` (el README oficial dice otros nombres; **el CSV manda**).
- `issues_train.csv` y `issues_test.csv`: 1 500 filas cada uno, 5 repos × 3 clases × 100 por split.
- Hallazgos: 1 duplicado exacto en train · 2 `body` vacíos en test · 3 issues aparecen en train y test · un body llega a ~207 mil caracteres · plantillas de issues (p. ej. React: "### Repro steps") pueden filtrar la clase.
- Fuente: https://github.com/nlbse2024/issue-report-classification. El LICENSE oficial está **vacío** → **no se suben los CSV a git**. Se bajan con `python scripts/download_data.py` y se verifican con SHA-256 (`data/SHA256SUMS.txt`).
- Referencia oficial (SetFit, test): F1 promedio 0.8270 (react 0.8718, tensorflow 0.8644, vscode 0.8262, bitcoin 0.7555, opencv 0.8173). Nuestro baseline TF-IDF+LR rinde ≈0.73 en validación: es normal que sea menor.

## 3. Protocolo de evaluación (NO NEGOCIABLE)
1. Ajustar hiperparámetros **solo con train** (validación cruzada, `--split valid`).
2. El **test se evalúa UNA vez** por modelo final. No lo uses "para probar". No lo uses para elegir nada.
3. **Un clasificador por repo** (5). **No remuestrear ni modificar las filas del test.**
4. Métrica: **F1 macro por repo y promedio** (usa `src/metrics.py`, no reimplementes).
5. Semilla fija `SEED = 42` (en `src/config.py`).
6. Nunca mezcles train y test al entrenar, ni limpies con estadísticas calculadas sobre el test.

## 4. Estructura del repo
```
src/config.py            constantes (rutas, SEED, etiquetas) — todo import sale de aquí
src/data/clean.py        limpieza de texto
src/data/make_dataset.py raw -> processed + resumen de calidad
src/models/              modelos (baseline_tfidf.py, y los demás)
src/metrics.py           métricas del protocolo
src/predict.py           predicción de un issue
src/api/main.py          API FastAPI (contrato en docs/api_contract.md)
tests/                   pytest
reports/metrics/*.json   ÚNICA fuente de cifras para el reporte
docs/                    decisiones, trazabilidad, referencias, métricas
ai_log/registro.md       registro de uso de IA (obligatorio)
```
Comandos: `python scripts/download_data.py` · `python -m src.data.make_dataset` · `python -m src.models.baseline_tfidf --split valid|test` · `pytest -q` · `uvicorn src.api.main:app --reload` · `.\run_all.ps1` (todo).
Entorno: Windows, PowerShell, **Python 3.11**, `.venv`.

## 5. REGLAS PARA LA IA

### Haz
- **Entiende primero, cambia después.** Lee los archivos relevantes antes de proponer código. Pregunta si falta contexto.
- Cambios **pequeños y enfocados** en lo que pidió el usuario y que corresponda a su rol (ver §1). Si la tarea toca archivos de otro compañero, díselo al usuario para que coordine.
- Código **en español** para comentarios, **con comentarios detallados línea por línea y para principiantes** (explicar qué hace, por qué, entradas y salidas). Nombres de variables/funciones como ya existen en el repo (inglés/español mezclado: respeta el estilo vecino).
- Usa las funciones existentes (`src.config`, `src.metrics`, `clean_text`…) en vez de duplicar lógica.
- Si agregas o cambias comportamiento, **agrega o ajusta pruebas** en `tests/` y avisa cómo correrlas (`pytest -q`).
- Cuando algo sea una decisión (por qué un parámetro, por qué quitar algo), propón una entrada para `docs/decisiones.md`.
- Al terminar, resume: qué cambió, en qué archivos, cómo verificarlo, y qué falta.
- Propón la fila para `ai_log/registro.md` (ver §7) al final de tu respuesta cuando el trabajo sea relevante.

### NO hagas
- **No inventes** resultados, métricas, tablas, referencias, DOIs, citas, enlaces, versiones de librerías ni nombres de funciones. Si no lo sabes o no pudiste verificarlo, di "no lo sé / no lo verifiqué".
- **Toda cifra del reporte sale de un JSON en `reports/metrics/`** (o de un notebook reproducible). Nunca de tu memoria ni de una estimación.
- **No presentes salida de IA como resultado experimental ni como fuente académica.** Una referencia solo entra a `docs/referencias.md` si el humano abrió el DOI/URL y los datos coinciden.
- No toques el test para ajustar nada (§3). No re-entrenes "hasta que salga bien" con el test.
- **No subas** CSV, modelos `.joblib/.pt`, `reports/errores/pred_*.csv`, `.env`, tokens ni contraseñas. Usa `git add <archivos>` en vez de `git add .` y revisa `git status`.
- **No sobrescribas el baseline oficial** (`baseline_tfidf_test.json`, `.joblib`): para experimentos usa `--tag` y `--split valid`. No quites entradas del `.gitignore`.
- No cambies el esquema del CSV ni "arregles" los datos crudos en `data/raw/` (el crudo es de solo lectura; la limpieza va en `src/data/` y se documenta).
- No hagas refactors masivos, no renombres archivos/carpetas, no cambies versiones de dependencias, no agregues librerías pesadas sin avisar y justificar.
- No uses `git push --force`, no trabajes directo en `main`, no borres historial ni ramas ajenas.
- No ejecutes comandos destructivos (`rm -rf`, `git reset --hard`, `del /s`) sin que el usuario lo confirme explícitamente.
- No cambies resultados después del **lunes 9-nov a las 20:00** (congelamiento): después de esa fecha solo texto/documentación.
- No "rellenes" secciones del reporte con texto genérico: si falta evidencia, deja un `TODO:` explícito.

### Si dudas
Pregunta al usuario. Si el usuario te pide algo que contradice estas reglas, explícale el conflicto y propón la alternativa correcta.

## 6. Flujo de trabajo con Git (que el humano debe seguir; ayúdalo a seguirlo)
1. `git checkout main && git pull`
2. Rama nueva con prefijo: `feat/` `fix/` `data/` `docs/` `test/` (ej. `data/limpieza-urls`).
3. Commits pequeños: `tipo: descripción corta` (ej. `fix: manejar body vacío en clean_text`).
4. Push de la rama → Pull Request con la plantilla (`Closes #n`, requisito `R__`) → revisión del par → merge.
5. Revisión cruzada: Sebastián↔Luis · Rogelio↔Gabriel · Evelyn revisada por Gabriel.
6. Tags de versión: v0.1 (jue 5) · v0.2 (sáb 7) · v0.3 (lun 9, 20:00) · v0.9 (mar 10, 22:00) · v1.0 (mié 11, entrega).

## 7. Documentar el uso de IA (obligatorio)
Cada uso relevante = una fila en `ai_log/registro.md`. Al final de tu respuesta, ofrece esta fila ya redactada para que el humano la pegue:

`| AAAA-MM-DD | <nombre> | <herramienta/modelo> | <para qué, resumido> | <qué devolvió, resumido> | <cómo se verificó: pruebas, JSON, DOI abierto…> | <qué se aceptó / cambió> |`

Recuérdale al usuario **verificar** antes de aceptar (correr `pytest -q`, comparar con el JSON, abrir la fuente).

## 8. Trazabilidad (cómo ayudar a Evelyn y a todos)
Cada tarea se liga a un requisito de `docs/trazabilidad.md` (R01…R22): requisito → issue → PR → archivo → prueba/evidencia → sección del reporte. Cuando termines algo, indica qué fila de la matriz se actualiza y con qué datos.

## 9. Estilo del reporte (si ayudas a redactar)
- 5 capítulos (Introducción; Marco teórico; Metodología y desarrollo; Implementación, análisis y resultados; Conclusiones) + Referencias + Anexos. Plantilla en `reporte/plantilla_reporte.md`, con tabla de quién redacta cada parte y subsección de conclusiones por integrante.
- Redacción académica, clara, terminología consistente, secciones numeradas.
- Cada fragmento de código explicado: objetivo, entradas, proceso, salidas, por qué así, cómo aporta al objetivo.
- Cada tabla/figura: título descriptivo + explicación + **interpretación** (qué significa, no solo qué se ve).
- Conclusiones derivadas de evidencia. Correspondencia objetivos ↔ metodología ↔ resultados ↔ conclusiones.
- Español neutro/mexicano, natural; sin relleno ni frases de "marketing".

## 10. Cosas aún sin confirmar con el profesor (no las asumas)
Hora y medio de entrega (PDF, enlace al repo, presentación), si hay presentación y su duración, formato de citación (se usa IEEE), y si la guía oficial exige algo que no aparezca en el aviso (bibliometría, Big Data, arquitectura web). Ver `guias/08_Mensaje_al_profesor.md`.

## 11. Resumen en 8 líneas (si solo vas a recordar esto)
1. Clasificamos issues GitHub (bug/feature/question), dataset NLBSE'24, 5 repos.
2. Columnas reales: `repo, created_at, label, title, body`. CSV no se sube a git.
3. Test se usa UNA vez; ajustes solo con train; seed 42; F1 macro por repo.
4. Cifras solo desde `reports/metrics/*.json`. Nada inventado. Referencias solo verificadas.
5. Cambios pequeños, con pruebas, comentarios detallados en español.
6. Rama + PR + revisión; nunca directo a `main`; nada destructivo sin confirmar.
7. Todo uso de IA se registra en `ai_log/registro.md`.
8. Ante la duda: pregunta; no adivines.
