# Limpieza y preparación de datos (responsable: Rogelio · revisa: Gabriel)

> Este documento sigue **la guía del profesor** (secciones "2. La limpieza de datos también es fundamental" y "¿Qué debe documentarse sobre la limpieza?"). Alimenta el **Cap. 3.2 a 3.4** del reporte. Los números de abajo se obtuvieron el 5-nov-2026 con el código del repo y se **reprodujeron el 9-nov-2026** en una segunda computadora (Linux CachyOS, Python 3.11): `hash_data.py` confirmó los CSV oficiales, `make_dataset` dio las mismas cifras de `reports/data_quality/resumen_calidad.json` y el experimento de la sección C dio los mismos F1.

## A. Los 6 puntos que pide el profesor

### 1. Fuente original
- Dataset **NLBSE'24 issue report classification**: https://github.com/nlbse2024/issue-report-classification (competencia de investigación; el repositorio oficial tiene el LICENSE vacío, por eso los CSV no se suben a git).
- Cada registro = **un issue de GitHub** de uno de 5 repos (facebook/react, tensorflow/tensorflow, microsoft/vscode, bitcoin/bitcoin, opencv/opencv).
- Columnas reales: `repo, created_at, label, title, body`. La etiqueta (`label`) es `bug`, `feature` o `question`. 1 500 filas en train y 1 500 en test (5 repos × 3 clases × 100).
- Condiciones de uso y verificación: `data/README.md` y `data/SHA256SUMS.txt` (huella SHA-256 de cada CSV).

### 2. Diagnóstico inicial (qué problemas se encontraron y cómo se identificaron)
| Problema | Cómo se identificó | Train | Test |
|---|---|---|---|
| Issues con URL en el cuerpo | `body.str.contains("https?://")` | 888 | 893 |
| Issues con bloque de código (```` ``` ````) | `body.str.contains("```")` | 719 | 713 |
| Issues con comentario HTML `<!-- -->` (texto de plantilla) | `body.str.contains("<!--")` | 261 | 277 |
| `body` vacío / nulo | `body.isna()` | 0 | 2 |
| Duplicados exactos (repo+título+cuerpo) | `df.duplicated(...)` | 1 | 0 |
| Título con URL | `title.str.contains("https?://")` | 1 | 2 |
| Cuerpo muy largo (máximo en caracteres) | `body.str.len().max()` | 207 777 | 61 610 |
| Mismo issue en train y en test | `tests/test_leakage.py` | 3 (solapamiento) | |

Columnas con nulos: solo `body` (2 en test). `repo`, `created_at`, `label` y `title` no tienen nulos.

### 3. Procedimiento (qué cambios se hicieron y por qué): tabla de 5 pasos de la guía
| Paso (guía) | Qué hicimos | Función / archivo | Decisión y justificación |
|---|---|---|---|
| 1. Inspección | Revisar columnas, tipos, número de filas y conteo repo×clase | `load_raw`, `quality_summary` (`make_dataset.py`) | Se **valida el esquema** al leer: si las columnas, etiquetas o repos no son los esperados, el programa se detiene. |
| 2. Detección | Contar nulos, duplicados, URL, código, comentarios HTML, longitudes | `quality_summary` (`make_dataset.py`), `scripts/eda.py` | Los conteos de la sección 2 salen de aquí. El EDA guarda tablas en `reports/eda/` y figuras `reports/figures/eda_*.png` (solo con train). |
| 3. Decisión | Una decisión por problema (tabla B) | este documento | Cada decisión tiene alternativa descartada. **No se eliminan filas por tener faltantes**: el `body` vacío se conserva como `""` porque el título aún trae señal. |
| 4. Transformación | Quitar comentarios HTML; bloques de código → `CODEBLOCK`; URLs → `URL`; colapsar espacios; unir título + cuerpo en `text` | `clean_text`, `clean_dataframe` (`clean.py`) | Ver tabla B. |
| 5. Validación | Comparar filas antes/después, nulos, duplicados, residuos de URL/HTML y etiquetas válidas | `validate_clean` (`make_dataset.py`) y `resumen_calidad.json` | Si falla algo crítico el programa lanza error. |

### 4. Herramientas y código
Python 3.11 · pandas (lectura, conteos, duplicados) · `re` (expresiones regulares) · pytest (pruebas en `tests/test_clean.py` y `tests/test_make_dataset.py`) · Git (cada cambio por PR). Funciones explicadas en `docs/explicacion_codigo.md`.
Uso de IA: cualquier apoyo de IA para escribir o revisar este código se registra en `ai_log/registro.md` con la forma en que se verificó (pruebas y comparación contra los conteos de pandas).

### 5. Comparación antes y después (de `reports/data_quality/resumen_calidad.json`)
| Indicador | Train antes | Train después | Test antes | Test después |
|---|---|---|---|---|
| Filas | 1 500 | 1 499 | 1 500 | 1 500 |
| Duplicados exactos (repo+título+cuerpo) | 1 | 0 | 0 | 1 (dos issues que solo diferían en una URL quedan iguales al limpiar; el test no se toca) |
| Mediana de longitud de `body` (caracteres) | 1 091 | 619 | 1 120.5 | 636 |
| Issues con URL en `text` | 888 | 0 | 893 | 0 |
| Issues con `<!--` en `text` | 261 | 0 | 277 | 2 |
| Nulos en `title`/`body`/`text` | 0 | 0 | 2 | 0 |

Tabla verificada contra `resumen_calidad.json` el 9-nov-2026: filas, duplicados, medianas y nulos coinciden.

### 6. Validación (cómo comprobamos que la limpieza no introdujo errores)
1. `validate_clean` comprueba: filas esperadas, sin nulos, etiquetas y repos válidos, sin duplicados (solo train), sin URL ni comentarios HTML residuales. Resultado guardado en `resumen_calidad.json` (`train_validacion`, `test_validacion`).
2. Residuo conocido: **2 issues de test** tienen un comentario HTML **sin cerrar** (`<!--` sin `-->`); la expresión regular solo quita comentarios completos. No se corrigió para no cambiar el procedimiento después de tener resultados, y se declara como limitación (por eso `sin_urls_ni_comentarios_html` sale `False` en test; no es un error del programa).
3. Pruebas automáticas: las 12 pruebas de `tests/test_clean.py`, `tests/test_make_dataset.py`, `tests/test_schema.py` y `tests/test_leakage.py` pasan (9-nov-2026). Cubren texto vacío, solo URL, solo código, emoji/acentos, comentario sin cerrar, texto muy largo, esquema de columnas y fuga entre train y test.
4. Experimento de utilidad: baseline con y sin limpieza en validación (tabla C).

## B. Decisiones una por una
| # | Paso | Función | Por qué | Afectó (train / test) | Alternativa descartada |
|---|---|---|---|---|---|
| 1 | Quitar comentarios HTML `<!-- -->` | `clean_text` | Son texto de plantilla invisible al lector | 261 / 277 issues | dejarlos |
| 2 | Bloques de código → `CODEBLOCK` | `clean_text` | Ruido muy largo; importa que **hay** código | 719 / 713 | quitarlos del todo |
| 3 | URLs → `URL` | `clean_text` | El enlace exacto no generaliza; que haya enlace sí informa | 888 / 893 | dejarlas |
| 4 | Colapsar espacios | `clean_text` | Normalizar | todos | — |
| 5 | Quitar duplicados exactos (solo train) | `drop_duplicates_report` | Evitar sesgo | 1 / 0 | dejarlo |
| 6 | **No** tocar las filas del test | `make_dataset.main` | Protocolo NLBSE | 0 | — |
| 7 | `body` vacío → `""` (no se elimina la fila) | `clean_text` | No perder la fila; el título trae señal | 0 / 2 | eliminar fila |
| 8 | Unir título + cuerpo en `text` (título primero) | `clean_dataframe` | El título suele ser lo más informativo | todos | usar solo el cuerpo |

## C. Experimento: ¿la limpieza ayuda?
Se corre `python scripts/experimento_limpieza.py` (solo validación cruzada sobre train; nunca test; no pisa JSON oficiales). Resultado del 5-nov, reproducido el 9-nov en Linux con valores idénticos (el JSON queda en `reports/metrics/experimento_limpieza.json`):

| Variante | F1 promedio (valid) | Diferencia vs. limpieza completa |
|---|---|---|
| Limpieza completa (oficial) | 0.7294 | — |
| Sin reemplazar URLs | 0.7370 | +0.0075 |
| Sin reemplazar código | 0.7280 | −0.0014 |
| Sin quitar comentarios HTML | 0.7344 | +0.0049 |

**Qué significa:** esperábamos que limpiar el texto ayudara al modelo, pero no fue así. Al dejar las URLs el F1 sube 0.0075, y al dejar los comentarios HTML sube 0.0049; o sea, esos dos pasos le quitan un poco de información al baseline en lugar de aportarle. Cambiar los bloques de código por `CODEBLOCK` casi no cambia nada (−0.0014). Todas las diferencias son menores a 0.01 y cada repo tiene solo 300 issues en train, así que pueden deberse al azar de la validación cruzada y no las tomamos como prueba de que limpiar perjudique.

Decidimos **no cambiar la limpieza oficial** después de ver estos números, porque el baseline ya se había evaluado en test y ajustar el procedimiento después de ver resultados sería adaptar el método a los datos de evaluación (sobreajuste). Por eso lo reportamos como limitación y como trabajo futuro (por ejemplo, conservar el dominio de la URL, como `github.com`, en lugar de borrarla toda). La limpieza la mantenemos porque hace el texto más legible, más corto (la mediana del cuerpo baja de 1 091 a 619 caracteres) y reproducible, no porque mejore el F1.

## D. Limitaciones de los datos (para el Cap. 4.6 y 5)
- Solo 5 repos y 3 clases: no representa a todo GitHub.
- Las plantillas de issues pueden delatar la clase (fuga de señal), ver `perfil_repos.md`.
- Hay 3 issues repetidos entre train y test.
- Etiquetas asignadas por la comunidad: pueden contener errores.
- Idioma: comprobar con una muestra (se asume mayoría en inglés; **no afirmar sin revisar**).
