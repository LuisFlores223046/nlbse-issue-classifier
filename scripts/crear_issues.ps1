# crear_issues.ps1 - Crea los 22 issues con GitHub CLI.
# OJO: si ya creaste #1-#20 a mano, NO corras todo el script (duplicaria issues): copia solo los bloques de R21 y R22.
# Requisitos: instalar gh (https://cli.github.com) y correr `gh auth login` una vez.
# Uso (dentro de la carpeta del repo clonado):  .\crear_issues.ps1
$ErrorActionPreference = 'Stop'
foreach ($l in 'datos','modelos','analitica','docs','api','git') { gh label create $l --force | Out-Null }
gh issue create --title 'R01 Objetivos, alcance y justificación' --label 'docs' --body @'
**Requisito:** R01 (ver docs/trazabilidad.md)

**Responsable:** Evelyn  **Revisor:** Gabriel  **Fecha límite:** jue 5-nov

**Qué hay que hacer**
- Redactar objetivo general, objetivos específicos, alcance y limitaciones
- Contestar la ficha de 10 preguntas (reporte/ficha_10_preguntas.md)

**Criterio de terminado (verificable)**
- [ ] Documento revisado por Gabriel y unido a main

**Evidencia esperada** (archivo, prueba o métrica): reporte/objetivos_y_alcance_borrador.md, reporte/ficha_10_preguntas.md
'@
gh issue create --title 'R02 Fuentes de información justificadas' --label 'datos' --body @'
**Requisito:** R02 (ver docs/trazabilidad.md)

**Responsable:** Rogelio  **Revisor:** Gabriel  **Fecha límite:** jue 5-nov

**Qué hay que hacer**
- Completar data/README.md: fuente, esquema real, hallazgos, licencia
- Justificar por qué NLBSE'24

**Criterio de terminado (verificable)**
- [ ] data/README.md completo y revisado

**Evidencia esperada** (archivo, prueba o métrica): data/README.md
'@
gh issue create --title 'R03 Descarga reproducible de datos' --label 'datos' --body @'
**Requisito:** R03 (ver docs/trazabilidad.md)

**Responsable:** Rogelio  **Revisor:** Gabriel  **Fecha límite:** jue 5-nov

**Qué hay que hacer**
- Correr scripts/download_data.py y scripts/hash_data.py (debe dar [OK] en los dos CSV)
- Comparar tu huella con las de data/README.md
- Abrir el PR de la rama data/descarga con data/SHA256SUMS.txt (sin CSV)
- Si no coincide, avisar a Luis (no cambiar el archivo)

**Criterio de terminado (verificable)**
- [ ] hash_data.py da OK en 2 máquinas distintas

**Evidencia esperada** (archivo, prueba o métrica): data/SHA256SUMS.txt (PR de Rogelio) y salida de hash_data.py pegada como comentario en el issue
'@
gh issue create --title 'R04 Limpieza con pruebas' --label 'datos' --body @'
**Requisito:** R04 (ver docs/trazabilidad.md)

**Responsable:** Rogelio  **Revisor:** Gabriel  **Fecha límite:** sáb 7-nov

**Qué hay que hacer**
- Ampliar src/data/clean.py si hace falta
- Agregar al menos 10 pruebas en tests/test_clean.py
- Verificar docs/decisiones_limpieza.md (6 puntos de la guía del profesor) con números reales
- Correr scripts/experimento_limpieza.py y escribir la lectura con tus palabras

**Criterio de terminado (verificable)**
- [ ] 10 o más pruebas verdes y decisiones documentadas

**Evidencia esperada** (archivo, prueba o métrica): src/data/clean.py, tests/test_clean.py, docs/decisiones_limpieza.md
'@
gh issue create --title 'R05 Calidad de datos y EDA' --label 'datos' --body @'
**Requisito:** R05 (ver docs/trazabilidad.md)

**Responsable:** Rogelio y Gabriel  **Revisor:** Luis  **Fecha límite:** sáb 7-nov

**Qué hay que hacer**
- Crear notebooks/01_eda.ipynb
- Llenar docs/perfil_repos.md con tablas
- Guardar figuras con título y ejes en reports/figures/

**Criterio de terminado (verificable)**
- [ ] Perfil de repos completo con figuras interpretadas

**Evidencia esperada** (archivo, prueba o métrica): notebooks/01_eda.ipynb, docs/perfil_repos.md, reports/data_quality/
'@
gh issue create --title 'R06 Baseline TF-IDF + regresión logística' --label 'modelos' --body @'
**Requisito:** R06 (ver docs/trazabilidad.md)

**Responsable:** Sebastián  **Revisor:** Luis  **Fecha límite:** sáb 7-nov

**Qué hay que hacer**
- Probar valores de C y class_weight con --split valid (usar --tag para no pisar archivos)
- Declarar como baseline oficial la corrida de run_all (C=1) en docs/decisiones.md
- Si eliges otro C, correr el test UNA vez con --tag y reportarlo como modelo aparte

**Criterio de terminado (verificable)**
- [ ] JSON de valid y de test en reports/metrics y PR aprobado

**Evidencia esperada** (archivo, prueba o métrica): src/models/baseline_tfidf.py, reports/metrics/baseline_tfidf_*.json
'@
gh issue create --title 'R07 Segundo modelo y comparación' --label 'modelos' --body @'
**Requisito:** R07 (ver docs/trazabilidad.md)

**Responsable:** Sebastián  **Revisor:** Luis  **Fecha límite:** lun 9-nov

**Qué hay que hacer**
- Evaluar src/models/scalable_sgd.py (HashingVectorizer + SGD por lotes): valid y luego test una vez
- Opcional: SetFit en Colab
- Comparar con el baseline en docs/metricas.md (F1 y segundos de entrenamiento)

**Criterio de terminado (verificable)**
- [ ] Tabla comparativa completa y justificación escrita

**Evidencia esperada** (archivo, prueba o métrica): src/models/, reports/metrics/*.json, docs/metricas.md
'@
gh issue create --title 'R08 Métricas del protocolo NLBSE' --label 'analitica' --body @'
**Requisito:** R08 (ver docs/trazabilidad.md)

**Responsable:** Gabriel  **Revisor:** Sebastián  **Fecha límite:** sáb 7-nov

**Qué hay que hacer**
- Revisar src/metrics.py (F1 por repo y promedio)
- Agregar pruebas de metrics.py

**Criterio de terminado (verificable)**
- [ ] metrics.py probado y usado por todos los modelos

**Evidencia esperada** (archivo, prueba o métrica): src/metrics.py, tests/
'@
gh issue create --title 'R09 Análisis de errores (7 preguntas de analítica)' --label 'analitica' --body @'
**Requisito:** R09 (ver docs/trazabilidad.md)

**Responsable:** Gabriel  **Revisor:** Rogelio  **Fecha límite:** lun 9-nov

**Qué hay que hacer**
- Crear notebooks/02_analisis_errores.ipynb
- Responder las 7 preguntas de la guía 04 con tabla o figura y un párrafo

**Criterio de terminado (verificable)**
- [ ] 7 preguntas respondidas con evidencia reproducible

**Evidencia esperada** (archivo, prueba o métrica): notebooks/02_analisis_errores.ipynb, reports/errores/, reports/figures/
'@
gh issue create --title 'R10 API FastAPI' --label 'api' --body @'
**Requisito:** R10 (ver docs/trazabilidad.md)

**Responsable:** Luis  **Revisor:** Sebastián  **Fecha límite:** sáb 7-nov

**Qué hay que hacer**
- Verificar /health y /predict según docs/api_contract.md
- Probar con modelos entrenados

**Criterio de terminado (verificable)**
- [ ] La API responde 200 con la estructura del contrato

**Evidencia esperada** (archivo, prueba o métrica): src/api/main.py, docs/api_contract.md
'@
gh issue create --title 'R11 Pruebas completas' --label 'api' --body @'
**Requisito:** R11 (ver docs/trazabilidad.md)

**Responsable:** Luis  **Revisor:** Gabriel  **Fecha límite:** lun 9-nov

**Qué hay que hacer**
- Ampliar tests/test_api.py (body vacío, texto largo)
- Confirmar que pytest -q pasa desde cero

**Criterio de terminado (verificable)**
- [ ] pytest -q verde en la máquina de otra persona

**Evidencia esperada** (archivo, prueba o métrica): tests/
'@
gh issue create --title 'R12 Control de versiones y tags' --label 'git' --body @'
**Requisito:** R12 (ver docs/trazabilidad.md)

**Responsable:** Luis  **Revisor:** Evelyn  **Fecha límite:** mié 11-nov

**Qué hay que hacer**
- Crear tags v0.1 (jue 5), v0.2 (sáb 7), v0.3 (lun 9 20:00), v0.9 (mar 10 22:00) y v1.0 (mié 11) en sus fechas
- Verificar que todos los PR tienen revisión y Closes #n

**Criterio de terminado (verificable)**
- [ ] Tags publicados y historial de PR completo

**Evidencia esperada** (archivo, prueba o métrica): historial de git
'@
gh issue create --title 'R13 Registro de uso de IA' --label 'docs' --body @'
**Requisito:** R13 (ver docs/trazabilidad.md)

**Responsable:** Todos  **Revisor:** Evelyn  **Fecha límite:** lun 9-nov

**Qué hay que hacer**
- Anotar cada uso relevante de IA en ai_log/registro.md
- Verificar y contrastar lo que devolvió la IA
- Evelyn redacta el Cap. 3.8: uso de IA por actividad (qué se pidió, qué devolvió, cómo se contrastó con evidencia)

**Criterio de terminado (verificable)**
- [ ] Registro completo, una fila por uso relevante

**Evidencia esperada** (archivo, prueba o métrica): ai_log/registro.md
'@
gh issue create --title 'R14 Reporte con los 5 capítulos' --label 'docs' --body @'
**Requisito:** R14 (ver docs/trazabilidad.md)

**Responsable:** Evelyn  **Revisor:** Gabriel  **Fecha límite:** mar 10-nov 22:00

**Qué hay que hacer**
- Redactar y unir los capítulos 1 a 5, referencias y anexos desde reporte/plantilla_reporte.md (cada quien redacta su parte; ver tabla en la plantilla)
- Agregar 5.6 conclusiones por integrante
- Cifras solo desde reports/metrics

**Criterio de terminado (verificable)**
- [ ] Borrador completo revisado por Gabriel

**Evidencia esperada** (archivo, prueba o métrica): reporte/
'@
gh issue create --title 'R15 Referencias verificables' --label 'docs' --body @'
**Requisito:** R15 (ver docs/trazabilidad.md)

**Responsable:** Evelyn  **Revisor:** Gabriel  **Fecha límite:** mar 10-nov

**Qué hay que hacer**
- Abrir cada DOI o URL de docs/referencias.md y comprobar datos
- Unificar el formato de citación

**Criterio de terminado (verificable)**
- [ ] Todas las referencias abiertas y comprobadas

**Evidencia esperada** (archivo, prueba o métrica): docs/referencias.md
'@
gh issue create --title 'R16 Presentación y demo' --label 'docs' --body @'
**Requisito:** R16 (ver docs/trazabilidad.md)

**Responsable:** Luis y Evelyn  **Revisor:** Sebastián  **Fecha límite:** mar 10-nov

**Qué hay que hacer**
- Armar 8 a 10 diapositivas
- Ensayar la demo de la API (5 min)

**Criterio de terminado (verificable)**
- [ ] Ensayo completo realizado

**Evidencia esperada** (archivo, prueba o métrica): presentacion/
'@
gh issue create --title 'R17 Análisis bibliométrico (rúbrica criterio 1)' --label 'docs' --body @'
**Requisito:** R17 (ver docs/trazabilidad.md)

**Responsable:** Evelyn  **Revisor:** Gabriel  **Fecha límite:** mar 10-nov (opcional)

**Qué hay que hacer**
- Reunir 12 a 20 trabajos sobre clasificación de issues/reportes (Google Scholar, OpenAlex o Semantic Scholar)
- Armar tabla: autor, año, medio, método, dataset, métrica reportada
- Gráfica de trabajos por año y 1 párrafo de interpretación

**Criterio de terminado (verificable)**
- [ ] Tabla y gráfica en el Cap. 2 con cada trabajo verificado (abierto el enlace)

**Evidencia esperada** (archivo, prueba o métrica): docs/bibliometria.md, reports/figures/bibliometria_por_anio.png
'@
gh issue create --title 'R18 Técnica escalable tipo Big Data (rúbrica criterio 2)' --label 'modelos' --body @'
**Requisito:** R18 (ver docs/trazabilidad.md)

**Responsable:** Sebastián  **Revisor:** Luis  **Fecha límite:** lun 9-nov

**Qué hay que hacer**
- Correr src/models/scalable_sgd.py en valid y, una vez, en test
- Medir tiempo y memoria frente al baseline
- Escribir 1 párrafo: por qué esta técnica escala y cuándo conviene

**Criterio de terminado (verificable)**
- [ ] JSON con segundos de entrenamiento y comparación escrita

**Evidencia esperada** (archivo, prueba o métrica): src/models/scalable_sgd.py, reports/metrics/scalable_sgd_*.json, docs/metricas.md
'@
gh issue create --title 'R19 Analítica de requerimientos y de nuestro proceso (rúbrica criterio 3)' --label 'analitica' --body @'
**Requisito:** R19 (ver docs/trazabilidad.md)

**Responsable:** Gabriel  **Revisor:** Evelyn  **Fecha límite:** mar 10-nov (opcional)

**Qué hay que hacer**
- Correr scripts/proceso_git_stats.py y analizar commits por persona y por día
- Completar docs/requisitos.md (requisitos funcionales y no funcionales del prototipo)
- Convertir los hallazgos en 3 métricas de desempeño con interpretación

**Criterio de terminado (verificable)**
- [ ] Tablas y párrafos del Cap. 4 con datos de reports/proceso/

**Evidencia esperada** (archivo, prueba o métrica): scripts/proceso_git_stats.py, reports/proceso/, docs/requisitos.md
'@
gh issue create --title 'R20 Optimización y pruebas de rendimiento (Tercer parcial, punto 3)' --label 'modelos' --body @'
**Requisito:** R20 (ver docs/trazabilidad.md)

**Responsable:** Sebastián y Luis  **Revisor:** Gabriel  **Fecha límite:** lun 9-nov (opcional)

**Qué hay que hacer**
- Sebastián: comparar class_weight None vs balanced y validación cruzada de 5 pliegues, documentar
- Luis: medir latencia de /predict (promedio de 50 llamadas) y anotarla
- Registrar los ajustes y su efecto en docs/metricas.md

**Criterio de terminado (verificable)**
- [ ] Tabla de ajustes con su efecto y latencia medida

**Evidencia esperada** (archivo, prueba o métrica): docs/metricas.md, reports/metrics/*.json
'@
gh issue create --title 'R21 Explicación del código (6 puntos por función)' --label 'docs' --body @'
**Requisito:** R21 (ver docs/trazabilidad.md)

**Responsable:** Todos (Evelyn une)  **Revisor:** Gabriel  **Fecha límite:** lun 9-nov

**Qué hay que hacer**
- Cada quien reescribe con sus palabras las fichas de sus funciones en docs/explicacion_codigo.md: objetivo, entradas, cómo funciona, salidas, por qué, aporte
- Poner 'Realizada por <nombre>' en cada ficha
- Evelyn une todo en el Cap. 4.2

**Criterio de terminado (verificable)**
- [ ] Todas las funciones listadas con las 6 respuestas y revisadas

**Evidencia esperada** (archivo, prueba o métrica): docs/explicacion_codigo.md, reporte/
'@
gh issue create --title 'R22 Checklist de calidad y revisión final' --label 'docs' --body @'
**Requisito:** R22 (ver docs/trazabilidad.md)

**Responsable:** Gabriel  **Revisor:** Evelyn  **Fecha límite:** mar 10-nov

**Qué hay que hacer**
- Evelyn llena docs/checklist_calidad.md contra el reporte completo
- Gabriel verifica cada casilla (abre referencias, revisa figuras, comprueba que las cifras coinciden con los JSON)
- Revisar el PDF final el miércoles 11

**Criterio de terminado (verificable)**
- [ ] Checklist completo y firmado por Gabriel

**Evidencia esperada** (archivo, prueba o métrica): docs/checklist_calidad.md
'@
