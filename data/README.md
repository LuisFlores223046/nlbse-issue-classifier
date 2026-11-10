# Datos

## Fuente
Repo oficial: https://github.com/nlbse2024/issue-report-classification (carpeta `data/`).

## Por qué este dataset
Usamos el dataset oficial de la competencia de clasificación de issues del workshop NLBSE'24.
Es una fuente pública preparada para una competencia de investigación, lo que permite comparar
nuestros resultados con la referencia oficial (SetFit). Además, ya viene etiquetado en tres
clases (`bug`, `feature`, `question`) y está balanceado: 100 issues por clase y por repositorio
en cada partición, para 5 repositorios (react, tensorflow, vscode, bitcoin, opencv).

## Esquema REAL (verificado el 4-nov-2026)
`repo, created_at, label, title, body`  (el README oficial dice otros nombres; el CSV manda).

| Archivo | Filas | Notas |
|---|---|---|
| issues_train.csv | 1 500 | 5 repos × 3 clases × 100; 1 duplicado por contenido (repo+title+body) |
| issues_test.csv | 1 500 | igual de balanceado; 2 `body` vacíos; 3 issues también aparecen en train |

## Hallazgos (calculados el 5-nov-2026)
Conteos obtenidos con pandas sobre los CSV de `data/raw/` (sin modificarlos).

| Indicador | train | test |
|---|---|---|
| Filas | 1 500 | 1 500 |
| Issues por repo × clase | 100 en cada celda | 100 en cada celda |
| Nulos en `repo`, `created_at`, `label`, `title` | 0 | 0 |
| Nulos en `body` | 0 | 2 |
| `body` vacío (nulo o solo espacios) | 0 | 2 |
| Duplicados exactos (todas las columnas) | 0 | 0 |
| Duplicados por contenido (`repo`+`title`+`body`, criterio de `clean.py`) | 1 | 0 |
| Longitud `title` (caracteres): mín / mediana / media / máx | 1 / 52 / 55.9 / 293 | 1 / 52 / 56.5 / 284 |
| Longitud `body` (caracteres): mín / mediana / media / máx | 1 / 1 091 / 2 335.7 / 207 777 | 0 / 1 120.5 / 2 179.1 / 61 610 |

Issues presentes en train y test (mismo repo, título y cuerpo): **3**
(1 de tensorflow/tensorflow y 2 de bitcoin/bitcoin, estos últimos con títulos de 1-2 caracteres).

**Interpretación:**
- El dataset está perfectamente balanceado (100 issues por repo y clase), por lo que no se
  remuestrea y el F1 macro es una métrica adecuada.
- Train no tiene nulos; test tiene 2 `body` nulos. La limpieza debe tolerar cuerpos vacíos
  (por ejemplo, clasificar solo con el título). Esas filas de test no se eliminan, porque el
  protocolo prohíbe modificar el test.
- La longitud del `body` está muy sesgada: la mediana ronda los 1 100 caracteres, pero el
  máximo en train llega a 207 777. Conviene evaluar un recorte de longitud.
- Train tiene 1 duplicado por contenido: el issue de bitcoin "#F" aparece dos veces con
  6 minutos de diferencia en `created_at`. El pipeline lo elimina (`drop_duplicates_report`
  en `src/data/clean.py`), por eso `train_clean.csv` queda con 1 499 filas. Ese mismo
  issue es uno de los 3 que también aparecen en test.
- Hay títulos de 1 carácter: existen issues con muy poca información textual.
- 3 issues aparecen en train y en test, lo que es una fuga de información. Si se corrige,
  se quitan solo de train.
- Las decisiones derivadas de estos hallazgos se documentan en `docs/decisiones.md`.

## Cómo obtenerlos
```powershell
python scripts/download_data.py   # baja a data/raw y escribe data/SHA256SUMS.txt
python scripts/hash_data.py       # comprueba que tu copia es idéntica
```
SHA-256 de referencia (04-nov-2026):
- issues_train.csv `18dc42a30aa33dccadb723ad3baeb164d38bff521496f985ca2791c26b8939f5`
- issues_test.csv  `4f7d8619d4e5adbea126e548fd8c214449288f3a93bb3bc130c54cd307af7e85`

## Por qué no se suben los CSV
El archivo LICENSE del repo oficial está vacío (0 bytes): no hay permiso explícito de redistribución.
Se cita la fuente y se sube solo el script + las huellas.

## Capas
- `raw/` original, intocable. - `interim/` pasos intermedios. - `processed/` listo para modelar.