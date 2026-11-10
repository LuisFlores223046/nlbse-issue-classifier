# Checklist de calidad del reporte (aviso del profesor, sección 7)

Se llena el **martes 10** (borrador completo) y de nuevo el **miércoles 11** antes de entregar. Lo revisa Gabriel (Evelyn llena, Gabriel verifica). Cada casilla debe poder comprobarse abriendo el reporte.

## Criterios del profesor
- [ ] Redacción académica, clara y coherente (sin frases de relleno, sin primera persona informal).
- [ ] Capítulos y subsecciones **numeradas** (1, 1.1, 1.2…).
- [ ] Terminología técnica consistente (p. ej. siempre "F1 macro", siempre "issue", siempre "baseline").
- [ ] Explicación suficiente para que **otro estudiante** repita el procedimiento (probar: que alguien ajeno al equipo lea 1 página).
- [ ] Código legible y bien presentado (bloques de código con explicación, ver `docs/explicacion_codigo.md`).
- [ ] **Cada tabla y figura**: número, título descriptivo, explicación de lo que representa e interpretación.
- [ ] Referencias verificables (cada una abierta por una persona distinta a quien la escribió) y con formato uniforme.
- [ ] Correspondencia **objetivos ↔ metodología ↔ resultados ↔ conclusiones** (tabla en el Cap. 5).
- [ ] Sin repeticiones innecesarias ni contenido que no aporte.

## Honestidad (aviso, secciones 5 y 6)
- [ ] Ninguna cifra sin JSON o notebook que la respalde (anotar el archivo junto a cada tabla).
- [ ] Ninguna referencia sin abrir; ninguna respuesta de IA presentada como resultado o como fuente.
- [ ] Uso de IA documentado por actividad (`ai_log/registro.md`) y contrastado con evidencia.
- [ ] Las conclusiones no afirman más de lo que muestran los datos (se declaran limitaciones).

## Contenido que pide el aviso (secciones 2, 3 y 8) — ¿está?
- [ ] Problema, relevancia, contexto, objetivos, alcance y limitaciones (Cap. 1).
- [ ] Conceptos, antecedentes, métodos y fundamentación (Cap. 2).
- [ ] Etapas, fuentes, datos, limpieza, algoritmos, herramientas, decisiones y problemas (Cap. 3).
- [ ] Funcionamiento, código explicado, tablas/gráficas/métricas, interpretación, **pruebas**, errores y mejoras (Cap. 4).
- [ ] Síntesis, cumplimiento de objetivos, respuesta al problema, dificultades, trabajo futuro (Cap. 5).
- [ ] Referencias y anexos.
- [ ] Control de versiones y trazabilidad (Cap. 3.8 + Anexo A).
- [ ] Presentación final (si el profesor la pide; pendiente de confirmar).

## Pruebas de que el entregable funciona
- [ ] Alguien ajeno al módulo clonó el repo en carpeta vacía y siguió el `README.md`: `pytest -q` verde y `run_all` sin errores.
- [ ] Tags v0.1 … v1.0 existen y el historial muestra PR con revisión.
