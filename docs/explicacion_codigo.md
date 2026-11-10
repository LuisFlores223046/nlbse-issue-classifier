# Explicación del código y de los procedimientos (Cap. 4.2 del reporte)

**Regla del profesor (aviso, sección 4):** el código no se presenta sin contexto. Cada función, algoritmo o procedimiento importante se explica con **6 puntos**:
1. **Objetivo** · 2. **Entradas** · 3. **Cómo funciona** (qué operaciones realiza) · 4. **Salidas** · 5. **Por qué se implementó así** · 6. **Cómo contribuye al objetivo general**.

Además, cuando hay varias etapas, se explica **cómo se relacionan** (sección final). Cada integrante redacta **sus** funciones con **sus palabras** (las entradas de abajo son un borrador verificable con el código: léelo y corrige lo que no coincida). Al lado de cada función se anota quién la hizo, como en el ejemplo del profesor ("Realizada por …"). Evelyn une todo en el Cap. 4.2 sin cambiar el sentido.

Estado: ⬜ borrador · 🟨 reescrito por su dueño · ✅ revisado por el revisor.

---
## Datos (Rogelio) — `src/data/`

### `clean_text(texto, quitar_comentarios_html, reemplazar_urls, reemplazar_codigo)` · `clean.py` · ⬜
1. **Objetivo:** limpiar un solo texto (título o cuerpo) de un issue.
2. **Entradas:** un texto (o vacío/nulo) y tres interruptores para activar o apagar pasos.
3. **Cómo funciona:** si es nulo devuelve `""`; quita comentarios HTML; cambia bloques de código por `CODEBLOCK`; cambia URLs por `URL`; colapsa espacios.
4. **Salidas:** texto limpio (siempre `str`).
5. **Por qué así:** cada paso es una expresión regular precompilada y se puede apagar para el experimento de utilidad (`scripts/experimento_limpieza.py`).
6. **Contribución:** deja el texto sin ruido para que TF-IDF aprenda de palabras útiles.

### `clean_dataframe(df)` · `clean.py` · ⬜
1. **Objetivo:** limpiar toda la tabla y crear la columna `text`.
2. **Entradas:** DataFrame con `repo, created_at, label, title, body`.
3. **Cómo funciona:** copia el DataFrame, aplica `clean_text` a título y cuerpo y crea `text = título + " . " + cuerpo`.
4. **Salidas:** copia limpia con columna `text`.
5. **Por qué así:** no modifica el original (el crudo es de solo lectura) y el título va primero porque suele ser lo más informativo.
6. **Contribución:** produce la única entrada que reciben los modelos.

### `drop_duplicates_report(df)` · `clean.py` · ⬜
1. **Objetivo:** quitar duplicados exactos y decir cuántos fueron.
2. **Entradas:** DataFrame.
3. **Cómo funciona:** `drop_duplicates` sobre `repo, title, body`, conserva el primero.
4. **Salidas:** `(df_sin_duplicados, cantidad_quitada)`.
5. **Por qué así:** devolver la cantidad evita ocultar datos y permite citarla en el reporte; solo se usa en train (el test no se modifica).
6. **Contribución:** evita que un issue repetido sesgue el entrenamiento.

### `load_raw(path)` · `make_dataset.py` · ⬜
1. **Objetivo:** leer un CSV crudo y validar su esquema. 2. **Entradas:** ruta del CSV. 3. **Cómo funciona:** comprueba que existe, que las columnas son las esperadas y que etiquetas y repos son válidos. 4. **Salidas:** DataFrame o un error claro. 5. **Por qué así:** es mejor fallar al inicio que entrenar con datos inesperados. 6. **Contribución:** paso 1 (inspección) de la guía del profesor.

### `quality_summary(df, nombre)` · `make_dataset.py` · ⬜
1. **Objetivo:** medir la calidad de una tabla. 2. **Entradas:** DataFrame y nombre. 3. **Cómo funciona:** cuenta filas, nulos, duplicados, conteo repo×clase y longitudes. 4. **Salidas:** diccionario (se guarda en `resumen_calidad.json`). 5. **Por qué así:** se llama **antes y después** para comparar. 6. **Contribución:** pasos 2 y 5 (detección y comparación antes/después).

### `validate_clean(df, nombre, filas_esperadas)` · `make_dataset.py` · ⬜
1. **Objetivo:** validar la limpieza. 2. **Entradas:** tabla limpia, nombre y filas esperadas. 3. **Cómo funciona:** verifica filas, nulos, etiquetas, repos, residuos de URL/HTML y duplicados (train). 4. **Salidas:** diccionario de comprobaciones; lanza error si algo crítico falla. 5. **Por qué así:** la guía pide demostrar que la limpieza no introdujo errores. 6. **Contribución:** paso 5 (validación).

### `main()` de `make_dataset.py` · ⬜ — orquesta: leer → medir antes → deduplicar (solo train) → limpiar → medir después → validar → guardar CSV y JSON.

---
## Modelos (Sebastián) — `src/models/`

### `build_pipeline(C, class_weight)` · `baseline_tfidf.py` · ⬜
1. **Objetivo:** construir el clasificador base. 2. **Entradas:** `C` (regularización) y `class_weight`. 3. **Cómo funciona:** `TfidfVectorizer` (palabras y pares, `min_df=2`, `sublinear_tf`, 50 000 términos) seguido de `LogisticRegression`. 4. **Salidas:** un `Pipeline` sin entrenar. 5. **Por qué así:** es rápido, interpretable y suficiente como línea base; un clasificador por repo, como pide el protocolo NLBSE. 6. **Contribución:** es el modelo oficial contra el que se compara todo.

### `main()` de `baseline_tfidf.py` · ⬜ — con `--split valid` hace validación cruzada de 5 pliegues solo en train; con `--split test` entrena con train y evalúa en test **una vez**; guarda JSON, predicciones y modelos.

### `entrenar_por_lotes(textos, etiquetas, class_weight, epocas)` · `scalable_sgd.py` · ⬜
1. **Objetivo:** entrenar sin cargar todo el texto a la vez. 2. **Entradas:** textos, etiquetas, peso de clases y épocas. 3. **Cómo funciona:** `HashingVectorizer` (no guarda vocabulario) + `SGDClassifier.partial_fit` por lotes. 4. **Salidas:** `(modelo, vectorizador)`. 5. **Por qué así:** memoria constante aunque crezcan los datos. 6. **Contribución:** segundo modelo y comparación F1 contra tiempo.

---
## Métricas y análisis (Gabriel)

### `evaluate(df)` · `src/metrics.py` · ⬜
1. **Objetivo:** calcular las métricas del protocolo. 2. **Entradas:** DataFrame con `repo`, `label`, `pred`. 3. **Cómo funciona:** por cada repo calcula precisión, recall y F1 por clase y F1 macro; promedia los 5 F1 macro. 4. **Salidas:** diccionario con `por_repo` y `f1_promedio_repos`. 5. **Por qué así:** es la métrica oficial de NLBSE'24; macro trata igual a las 3 clases. 6. **Contribución:** única fuente de cifras del reporte.

### `save_metrics(nombre_modelo, resultados, extra)` · `src/metrics.py` · ⬜
Guarda el JSON en `reports/metrics/` con parámetros extra (semilla, versión): enlaza **resultado ↔ código ↔ datos** (trazabilidad).

---
## Prototipo (Luis)

### `predict_issue(title, body, repo)` · `src/predict.py` · ⬜
Carga (una sola vez) el modelo del repo, limpia el texto con `clean_text` y devuelve `(etiqueta, probabilidades)`; la API añade la versión del modelo. Contribución: es lo que usa la API.

### `GET /health` y `POST /predict` · `src/api/main.py` · ⬜
Entradas, salidas y códigos de error (422 entrada inválida, 503 sin modelo) en `docs/api_contract.md`. Se validan con `tests/test_api.py`.

---
## Cómo se relacionan las etapas (Cap. 3.1 y 4.2) — borrador
`download_data.py` (CSV + SHA-256) → `make_dataset.py` (`load_raw` → `clean_*` → `validate_clean` → `train_clean.csv`/`test_clean.csv`) → `baseline_tfidf.py`/`scalable_sgd.py` (entrenan con train, evalúan con `evaluate`, escriben JSON y predicciones) → análisis de errores (lee `reports/errores/pred_*.csv`) → `predict.py` (carga los modelos `.joblib`) → API → pruebas (`pytest`). Cada flecha = un archivo producido que la etapa siguiente lee.

> Si agregas una función importante nueva, agrega aquí su ficha de 6 puntos en el mismo PR.
