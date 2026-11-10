# Matriz de trazabilidad

Una fila por requisito. Se llena **mientras** se trabaja, no al final. Dueño: Evelyn (revisa Gabriel).
Estados: ⬜ pendiente · 🟨 en curso · ✅ listo.

| ID | Requisito (fuente) | Issue | Commit/PR | Archivo(s) | Prueba / evidencia | Sección del reporte | Dueño | Estado |
|---|---|---|---|---|---|---|---|---|
| R01 | Planteamiento y justificación del problema (guía oficial) | #1 | | reporte/objetivos_y_alcance_borrador.md | revisión Gabriel | Cap. 1 | Evelyn | ⬜ |
| R02 | Fuentes de información justificadas | #2 | | docs/referencias.md, data/README.md | SHA256SUMS | Cap. 3 | Rogelio | ⬜ |
| R03 | Recolección y descarga reproducible | #3 | | scripts/download_data.py, data/SHA256SUMS.txt | hash_data.py OK en 2 máquinas | Cap. 3 | Rogelio | ⬜ |
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
| R17 | Análisis bibliométrico (rúbrica criterio 1, Unidad I) | #17 | | docs/bibliometria.md | tabla + gráfica, enlaces abiertos | Cap. 2 | Evelyn | ⬜ |
| R18 | Técnica escalable tipo Big Data (rúbrica criterio 2, temas 2.2/2.4) | #18 | | src/models/scalable_sgd.py | reports/metrics/scalable_sgd_*.json | Cap. 3-4 | Sebastián | ⬜ |
| R19 | Analítica de requerimientos y procesos (rúbrica criterio 3, temas 3.1/3.2/3.4) | #19 | | scripts/proceso_git_stats.py, docs/requisitos.md | reports/proceso/*.csv | Cap. 4 | Gabriel | ⬜ |
| R20 | Optimización y pruebas de rendimiento (3er parcial, punto 3) | #20 | | docs/metricas.md | JSON + latencia medida | Cap. 4 | Sebastián/Luis | ⬜ |

## Mapa rúbrica del profesor → requisitos
| Criterio de la rúbrica | Requisitos que lo cubren |
|---|---|
| 1. Planteamiento y fundamentos (Unidad I, incluye análisis bibliométrico) | R01, R02, R15, R17 |
| 2. Procesamiento y ciencia de datos (Unidad II, Big Data y ML) | R03, R04, R05, R06, R07, R18 |
| 3. Analítica de software y requerimientos (Unidad III) | R08, R09, R19, R20 |
| 4. Código, modelado y prototipado | R10, R11 |
| 5. Gestión, trazabilidad y versiones (Unidad V / cierre) | R12, R13, trazabilidad completa |
| Reporte, presentación y defensa (entrega final) | R14, R16 |

> Cada columna "Commit/PR" se llena con el número de PR (ej. `PR #7`).
