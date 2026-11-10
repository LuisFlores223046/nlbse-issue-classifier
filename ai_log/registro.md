# Registro de uso de IA (obligatorio — todos)

El profesor pide documentar el uso de IA y **contrastarlo con evidencia**. Una fila por uso relevante.

| Fecha | Quién | Herramienta | Para qué (prompt resumido) | Qué devolvió (resumen) | Cómo se verificó | Qué se aceptó / cambió |
|---|---|---|---|---|---|---|
| 04-nov | Luis | Claude | Planeación, guías y esqueleto del repo | Plan, guías, código base | Se ejecutó el pipeline completo y 13 pruebas pasaron; datos verificados contra el repo oficial | Se adoptó; ajustes del equipo en PRs |
| 05-nov | Rogelio | Claude | Script de pandas para contar hallazgos y redacción de data/README.md| Script de conteo, tabla de hallazgos, párrafo "Por qué este dataset" e interpretación | Números obtenidos corriendo el script en mi PC y con un conteo extra | Se aceptó la tabla; se corrigió "duplicado exacto" a "duplicado por contenido" |
| 09-nov | Gabriel | Claude Code | Subir mi parte (PR feat/analisis-errores): crear la rama, copiar los archivos del kit, traducir los comandos de PowerShell a bash y verificar | Rama con analisis_errores.py, checklist_calidad.md, tablas p1-p6 y figuras de confusión y longitud; explicación de cada archivo | Corrí make_dataset, baseline_tfidf --split valid y analisis_errores.py: 404 errores de 1 499 (igual a p1); p1, p2, p4 y p5 idénticos a Drive; pytest -q: 17 pasan | Se subieron los archivos de Drive (los que cita el reporte); la corrida local solo sirvió para comprobar |

Reglas: nada de IA presentado como resultado experimental · toda cifra sale de un JSON de `reports/metrics` · toda referencia se abre y se comprueba.