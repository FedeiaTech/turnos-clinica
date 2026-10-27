## Issue relacionado

Closes #<!-- número del issue -->

## Qué cambia

## Cómo se verificó

```text
<!-- pegar la salida del hook pre-commit y de pytest --cov -->
```

## Checklist de la Definition of Done

- [ ] 1. Compila e importa sin errores (`ruff check` sin errores `E9`/`F`).
- [ ] 2. La suite completa pasa (`pytest`).
- [ ] 3. Cobertura de ramas >= 80 %.
- [ ] 4. Revisión aprobada por un par.
- [ ] 5. `black --check` y `ruff check` sin observaciones.
- [ ] 6. Docstrings, `README.md` y `requirements.txt` actualizados si cambió un contrato.
