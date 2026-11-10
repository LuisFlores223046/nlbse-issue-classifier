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

<!-- Copia el bloque D-00X para cada decisión nueva. -->
