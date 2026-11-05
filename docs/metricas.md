# Métricas y resultados (Gabriel)

Todas las cifras salen de `reports/metrics/*.json`. **No se escribe un número aquí que no esté en un JSON.**

| Modelo | Split | F1 promedio | react | tensorflow | vscode | bitcoin | opencv | JSON | Commit |
|---|---|---|---|---|---|---|---|---|---|
| Baseline TF-IDF + LR | valid (CV train) | | | | | | | baseline_tfidf_valid.json | |
| Baseline TF-IDF + LR | test | | | | | | | baseline_tfidf_test.json | |
| (SetFit / otro) | | | | | | | | | |
| Referencia oficial SetFit NLBSE'24 | test | 0.8270 | 0.8718 | 0.8644 | 0.8262 | 0.7555 | 0.8173 | README oficial | — |

Reglas: el test se usa una vez por modelo final · misma semilla (42) · mismos datos (SHA-256).
