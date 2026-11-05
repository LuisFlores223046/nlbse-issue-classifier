# Datos

## Fuente
Repo oficial: https://github.com/nlbse2024/issue-report-classification (carpeta `data/`).

## Esquema REAL (verificado el 4-nov-2026)
`repo, created_at, label, title, body`  (el README oficial dice otros nombres; el CSV manda).

| Archivo | Filas | Notas |
|---|---|---|
| issues_train.csv | 1 500 | 5 repos × 3 clases × 100; 1 duplicado exacto |
| issues_test.csv | 1 500 | igual de balanceado; 2 `body` vacíos; 3 issues también aparecen en train |

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
