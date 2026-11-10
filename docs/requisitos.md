# Requisitos del prototipo (Gabriel y Luis)

Rúbrica, criterio 3: "analítica de requerimientos y procesos". Aquí se listan los requisitos del sistema
y se evalúa si cada uno se cumplió, con evidencia.

## Funcionales
| ID | Requisito | Prioridad | Evidencia | ¿Cumplido? |
|---|---|---|---|---|
| RF-01 | Recibir título y cuerpo de un issue y devolver bug/feature/question | Alta | tests/test_api.py | |
| RF-02 | Devolver probabilidades por clase | Alta | tests/test_api.py | |
| RF-03 | Elegir el modelo del repo correspondiente | Media | src/predict.py | |
| RF-04 | Rechazar entradas inválidas (título vacío, repo desconocido) con error claro | Media | tests/test_api.py (422) | |
| RF-05 | Informar si el modelo no está entrenado (503) | Baja | tests/test_api.py | |

## No funcionales
| ID | Requisito | Métrica | Meta | Medido |
|---|---|---|---|---|
| RNF-01 | Tiempo de respuesta de /predict | ms promedio de 50 llamadas | < 200 ms | |
| RNF-02 | Reproducibilidad | `run_all` da las mismas métricas en 2 máquinas | idénticas | |
| RNF-03 | Calidad del modelo | F1 promedio en test | ≥ 0.70 | |
| RNF-04 | Mantenibilidad | pruebas automáticas | todas verdes | |
| RNF-05 | Trazabilidad | requisitos con evidencia en la matriz | 100 % | |

## Cómo medir la latencia (Luis)
Con la API corriendo, en PowerShell:
```powershell
$t = Measure-Command { 1..50 | ForEach-Object { Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/predict -ContentType "application/json" -Body '{"title":"App crashes","body":"error","repo":"facebook/react"}' | Out-Null } }
"{0:N1} ms por llamada" -f ($t.TotalMilliseconds / 50)
```
