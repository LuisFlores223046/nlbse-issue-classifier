# Decisiones de limpieza (Rogelio)

Cada transformación: qué hace, por qué, cuántas filas/caracteres afectó, y alternativa descartada.

| # | Paso | Función | Por qué | Afectó (llenar con datos reales) | Alternativa descartada |
|---|---|---|---|---|---|
| 1 | Quitar comentarios HTML `<!-- -->` | `clean_text` | Son texto de plantilla, invisible al lector | ___ issues | dejarlos |
| 2 | Bloques de código → `CODEBLOCK` | `clean_text` | Ruido muy largo; importa que HAY código | ___ issues | quitarlos del todo |
| 3 | URLs → `URL` | `clean_text` | El link exacto no generaliza | ___ | dejarlas |
| 4 | Colapsar espacios | `clean_text` | Normalizar | todos | — |
| 5 | Quitar duplicados exactos (solo train) | `drop_duplicates_report` | Evitar sesgo | 1 | dejar |
| 6 | NO tocar el test (filas) | `make_dataset.main` | Protocolo NLBSE | 0 | — |
| 7 | `body` vacío → "" | `clean_text` | No perder la fila | 2 (test) | eliminar fila |

Notas de calidad (rellenar tras el EDA): longitudes extremas (máx. ≈ 207 mil caracteres en un body), idiomas, etc.
