# Matriz de trazabilidad

Una fila por requisito. Se llena **mientras** se trabaja, no al final. Dueño: Evelyn (revisa Gabriel).
Estados: ⬜ pendiente · 🟨 en curso · ✅ listo.

| ID | Requisito (fuente) | Issue | Commit/PR | Archivo(s) | Prueba / evidencia | Sección del reporte | Dueño | Estado |
|---|---|---|---|---|---|---|---|---|
| R01 | Planteamiento y justificación del problema (guía oficial) | #1 | | reporte/objetivos_y_alcance_borrador.md | revisión Gabriel | Cap. 1 | Evelyn | ⬜ |
| R02 | Fuentes de información justificadas | #2 | PR #23 | docs/referencias.md, data/README.md | SHA256SUMS | Cap. 3 | Rogelio | ⬜ |
| R03 | Recolección y descarga reproducible | #3 | PR #22 | scripts/download_data.py, data/SHA256SUMS.txt | hash_data.py OK en 2 máquinas | Cap. 3 | Rogelio | ⬜ |
| R04 | Limpieza y preparación documentadas | #4 | PR #25 | src/data/clean.py, docs/decisiones_limpieza.md | tests/test_clean.py | Cap. 3 | Rogelio | ⬜ |
| R05 | Calidad de datos medida | #5 | PR #25 | reports/data_quality/ | resumen_calidad.json | Cap. 3-4 | Rogelio | ⬜ |
| R06 | Baseline implementado | #6 | PR #24 | src/models/baseline_tfidf.py | reports/metrics/baseline_*.json | Cap. 3-4 | Sebastián | ⬜ |
| R07 | Modelo(s) comparado(s) | #7 | PR #24 | src/models/… | reports/metrics/*.json | Cap. 4 | Sebastián | ⬜ |
| R08 | Métricas de evaluación (F1 por repo y promedio) | #8 | PR #27 | src/metrics.py | tests, metrics JSON | Cap. 4 | Gabriel | ⬜ |
| R09 | Análisis de errores / analítica de software | #9 | PR #27 | reports/errores/ | tablas y figuras | Cap. 4 | Gabriel | ⬜ |
| R10 | Prototipo (API) | #10 | | src/api/main.py | tests/test_api.py | Cap. 4 | Luis | ⬜ |
| R11 | Pruebas | #11 | | tests/ | pytest -q verde | Cap. 4 | Luis | ⬜ |
| R12 | Control de versiones | #12 | | historial git, tags | git log | Cap. 3 | Luis | ⬜ |
| R13 | Uso de IA documentado | #13 | | ai_log/registro.md | revisión | Cap. 3 / Anexo | todos | ⬜ |
| R14 | Reporte con estructura de 5 capítulos | #14 | | reporte/ | revisión cruzada | todo | Evelyn | ⬜ |
| R15 | Referencias verificables | #15 | PR #26 | docs/referencias.md | DOI abiertos uno por uno | Refs | Evelyn | ⬜ |
| R16 | Presentación final | #16 | | presentacion/ | ensayo | — | Luis | ⬜ |
| R17 | Análisis bibliométrico (opcional; solo si el profe lo exige) | #17 | | docs/bibliometria.md | tabla + gráfica, enlaces abiertos | Cap. 2 | Evelyn | ⬜ |
| R18 | Técnica escalable (segundo modelo; se cierra con R07) | #18 | PR #24 | src/models/scalable_sgd.py | reports/metrics/scalable_sgd_*.json | Cap. 3-4 | Sebastián | ⬜ |
| R19 | Analítica del proceso y requerimientos (opcional; apoya trazabilidad) | #19 | | scripts/proceso_git_stats.py, docs/requisitos.md | reports/proceso/*.csv | Cap. 4 | Gabriel | ⬜ |
| R20 | Optimización y latencia (opcional) | #20 | | docs/metricas.md | JSON + latencia medida | Cap. 4 | Sebastián/Luis | ⬜ |
| R21 | Explicación del código con 6 puntos (aviso §4) | #21 | PR #26 | docs/explicacion_codigo.md | revisión Gabriel | Cap. 4.2 | todos / Evelyn | ⬜ |
| R22 | Calidad y presentación del reporte (aviso §7) | #22 | PR #27 | docs/checklist_calidad.md | checklist verificado | todo | Gabriel | ⬜ |

## Mapa aviso del profesor → requisitos
| Pide el aviso / la guía HTML | Requisitos que lo cubren |
|---|---|
| §1-§3 Problema, contexto, justificación, objetivos, alcance (Cap. 1) y marco teórico (Cap. 2) | R01, R02, R15 (R17 opcional) |
| §3 Cap. 3 Metodología: fuentes, datos, limpieza, modelos, herramientas; guía HTML §2 limpieza | R02, R03, R04, R05, R06, R07, R18 |
| §3 Cap. 4 Implementación y resultados; evaluación con pruebas; errores y mejoras | R08, R09, R10, R11 (R19, R20 opcionales) |
| §4 Explicación del código (6 puntos) | R21 |
| §5 Interpretación y nada inventado; §7 calidad | R14, R22 |
| §6 Fuentes confiables y uso de IA documentado | R13, R15 |
| §8 Control de versiones, trazabilidad y presentación final | R12, R16 |
| §3 Cap. 5 Conclusiones, por integrante (ejemplo del profesor) | R14 |

> Cada columna "Commit/PR" se llena con el número de PR (ej. `PR #7`).
