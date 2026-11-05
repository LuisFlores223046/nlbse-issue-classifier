# Matriz de trazabilidad

Una fila por requisito. Se llena **mientras** se trabaja, no al final. Dueño: Evelyn (revisa Gabriel).
Estados: ⬜ pendiente · 🟨 en curso · ✅ listo.

| ID | Requisito (fuente) | Issue | Commit/PR | Archivo(s) | Prueba / evidencia | Sección del reporte | Dueño | Estado |
|---|---|---|---|---|---|---|---|---|
| R01 | Planteamiento y justificación del problema (guía oficial) | #1 | | docs/objetivos.md | revisión Gabriel | Cap. 1 | Evelyn | ⬜ |
| R02 | Fuentes de información justificadas | #2 | | docs/referencias.md, data/README.md | SHA256SUMS | Cap. 3 | Rogelio | ⬜ |
| R03 | Recolección y descarga reproducible | #3 | | scripts/download_data.py | hash_data.py OK | Cap. 3 | Rogelio | ⬜ |
| R04 | Limpieza y preparación documentadas | #4 | | src/data/clean.py, docs/decisiones_limpieza.md | tests/test_clean.py | Cap. 3 | Rogelio | ⬜ |
| R05 | Calidad de datos medida | #5 | | reports/data_quality/ | resumen_calidad.json | Cap. 3-4 | Rogelio | ⬜ |
| R06 | Baseline implementado | #6 | | src/models/baseline_tfidf.py | reports/metrics/baseline_*.json | Cap. 3-4 | Sebastián | ⬜ |
| R07 | Modelo(s) comparado(s) | #7 | | src/models/… | reports/metrics/*.json | Cap. 4 | Sebastián | ⬜ |
| R08 | Métricas de evaluación (F1 por repo y promedio) | #8 | | src/metrics.py | tests, metrics JSON | Cap. 4 | Gabriel | ⬜ |
| R09 | Análisis de errores / analítica de software | #9 | | reports/errores/ | tablas y figuras | Cap. 4 | Gabriel | ⬜ |
| R10 | Prototipo (API) | #10 | | src/api/main.py | tests/test_api.py | Cap. 4 | Luis | ⬜ |
| R11 | Pruebas | #11 | | tests/ | pytest -q verde | Cap. 4 | Luis | ⬜ |
| R12 | Control de versiones | #12 | | historial git, tags | git log | Cap. 3 | Luis | ⬜ |
| R13 | Uso de IA documentado | #13 | | ai_log/registro.md | revisión | Cap. 3 / Anexo | todos | ⬜ |
| R14 | Reporte con estructura de 5 capítulos | #14 | | reporte/ | revisión cruzada | todo | Evelyn | ⬜ |
| R15 | Referencias verificables | #15 | | docs/referencias.md | DOI abiertos uno por uno | Refs | Evelyn | ⬜ |
| R16 | Presentación final | #16 | | presentacion/ | ensayo | — | Luis | ⬜ |

> Cada columna "Commit/PR" se llena con el número de PR (ej. `PR #7`).
