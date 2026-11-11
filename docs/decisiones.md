# Registro de decisiones (ADR corto)

Formato: una entrada por decisión importante. Responde: ¿qué se decidió, por qué, qué alternativas había?

## D-001 · Tema y dataset (04-nov-2026)
- **Decisión:** clasificar issues de GitHub (bug/feature/question) con NLBSE'24.
- **Por qué:** dataset público, etiquetado, balanceado, con baselines y protocolo oficiales; riesgo bajo con poco tiempo.
- **Alternativas:** PROMISE NFR (625 requisitos, muy chico), GitBugs (menos estandarizado).
- **Autor:** equipo.

## D-002 · Datos fuera de git
- **Decisión:** no subir CSV; script de descarga + SHA-256.
- **Por qué:** LICENSE oficial vacío; además mantiene el repo liviano.

## D-003 · Protocolo de evaluación
- **Decisión:** ajustar solo con train (validación cruzada); test se evalúa **una vez** por modelo final; un clasificador por repo; métrica = F1 macro por repo y promedio.
- **Por qué:** es el protocolo NLBSE'24; evita fuga de información.

## D-004 · Hallazgos de datos que obligan a decidir (rellenar)
- Duplicado exacto en train (1) → se elimina (ver decisiones_limpieza.md).
- 3 issues aparecen en train y test → se reportan; el test NO se modifica.
- 2 `body` vacíos en test → se tratan como texto vacío (solo título).
- Plantillas de issues (React: "### Repro steps"…) → posible fuga; Gabriel mide el efecto.

## D-005 · Baseline oficial (Sebastián completa)
- **Decisión:** el baseline oficial es la corrida de `run_all` con `C=1` (valid 0.7294, test 0.7402, 5-nov-2026).
- **Por qué:** el test ya se evaluó una vez con esa configuración; cualquier otro ajuste se reporta como modelo aparte (`--tag`).
- **Pendiente de Sebastián:** explicar qué hace TF-IDF, qué es `C` y por qué un clasificador por repo.

## D-006 · Predicciones fuera de git
- **Decisión:** `reports/errores/pred_*.csv` no se versionan.
- **Por qué:** contienen títulos del dataset y la licencia original está vacía.

## D-007 · Ajuste de C por validación (5-nov-2026)
- **Decisión:** probar C = 0.1, 0.3, 1, 3, 10 con y sin `class_weight="balanced"` solo en validación (`--split valid --tag`). El mejor F1 de validación fue C=10 sin balanceo (0.7443). Se evaluó **una sola vez** en test como modelo aparte (`--split test --C 10 --tag C10`): 0.7634.
- **Por qué:** protocolo NLBSE (ajustar con train, test una vez por modelo final). El baseline oficial sigue siendo C=1 (0.7402).
- **Límite:** C=10 es el extremo de la rejilla; no se probaron valores mayores.

## D-008 · Segundo modelo escalable (5-nov-2026)
- **Decisión:** `scalable_sgd.py` (HashingVectorizer + SGDClassifier por lotes). Valid 0.6919, test 0.7159, 1.0 s de entrenamiento (test).
- **Por qué:** muestra una técnica que no guarda vocabulario y usa memoria constante; se compara contra el baseline en F1 y tiempo.
- **Límite:** no se exploró `class_weight` ni otros hiperparámetros en este modelo; con 1 500 issues el tiempo no es un factor decisivo.

## D-009 · La limpieza no se cambia tras el experimento (5-nov-2026)
- **Decisión:** se mantiene la limpieza completa aunque en validación quitar el reemplazo de URLs dio +0.0075 de F1 (ver `decisiones_limpieza.md`, sección C).
- **Por qué:** el baseline oficial ya se había evaluado en test; cambiar el procedimiento después de ver resultados sería ajustar con información posterior. Queda como trabajo futuro.

## D-010 · Fuga por plantilla (5-nov-2026)
- **Hallazgo:** quitar los encabezados "### ..." baja el F1 de validación de tensorflow de 0.808 a 0.741; en los demás repos el cambio es ≤ 0.007 en valor absoluto. Promedio 0.729 → 0.717.
- **Decisión:** no se quitan encabezados del modelo oficial; se reporta como riesgo de fuga en el Cap. 4.6.

<!-- Copia el bloque D-00X para cada decisión nueva. -->
