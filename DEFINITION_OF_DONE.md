# Definition of Done — turnos-clinica

Una tarea (issue) se considera **Terminada** solo cuando su Pull Request cumple los seis
criterios. Si falla uno, el PR no se integra a `main`. La DoD es la misma para todas las
tareas; los criterios de aceptación funcionales se escriben en cada issue.

| # | Criterio | Condición verificable | Herramienta / evidencia |
|---|----------|-----------------------|-------------------------|
| 1 | Integridad de compilación | `python -m compileall -q src tests` termina con código 0 y los imports resuelven sin errores ni `SyntaxWarning`. | Hook pre-commit (`ruff check` reporta errores `E9`/`F`). |
| 2 | Pruebas automatizadas | El 100 % de la suite de `tests/` pasa. Un solo test en rojo veta la integración. Cada bug corregido agrega un test que lo reproduce. | `pytest`, ejecutado por el hook y adjunto en el PR. |
| 3 | Cobertura mínima | Cobertura total de **ramas** ≥ 80 % y ningún archivo nuevo o modificado por debajo de 80 %. | `pytest --cov` con `fail_under = 80` y `branch = true` en `pyproject.toml`. |
| 4 | Revisión por pares | Al menos **1 aprobación** de un integrante distinto del autor. Los comentarios bloqueantes quedan resueltos antes del merge. | Revisión del PR en GitHub. Rama `main` protegida. |
| 5 | Gobernanza de estilo | `black --check` sin cambios pendientes y `ruff check` sin advertencias. Complejidad ciclomática ≤ 8 por función (`C901`). | Hook pre-commit. |
| 6 | Documentación técnica | Las funciones públicas nuevas tienen docstring. Un cambio de contrato (firma pública, formato JSON enviado a la API, dependencias) actualiza `README.md` y `requirements.txt`. | Checklist del PR, revisada por el par. |

## Fuera de la DoD

- **Criterios de aceptación**: son propios de cada issue (por ejemplo, "el descuento
  acumulado no supera el 25 %"). Se validan con los tests de ese issue.
- **Excepciones**: un criterio solo se omite si el PR lleva la etiqueta `dod-exception`
  y el revisor deja escrita la justificación. La deuda queda registrada como issue
  `technical-debt`.
