# turnos-clinica

Módulo de facturación, cobro y liquidación de honorarios de turnos médicos. Se usa como
sistema de laboratorio para los trabajos prácticos de la Unidad 3 (Verificación y
Validación) de Metodología en Sistemas II.

## Estructura

```text
src/turnos/
  facturacion.py   calcular_total / calcular_descuento (reglas de descuento)
  pagos.py         ServicioCobro contra una PasarelaPagos externa
  liquidacion.py   liquidación mensual de honorarios
  publicacion.py   envío de la liquidación a la API de administración
tests/             suites pytest (patrón AAA, stubs y mocks)
auditoria/         código heredado y reportes de análisis estático
.githooks/         hook pre-commit (black -> ruff -> pytest)
.github/           plantillas de issue y PR, etiquetas
```

## Puesta en marcha

```sh
python -m pip install -r requirements-dev.txt
git config core.hooksPath .githooks
python -m pytest --cov
```

## Contrato con la API de administración

`POST /liquidaciones` con cuerpo JSON:

```json
{"medico": "str", "mes": "AAAA-MM", "items": [{"turno": 1, "monto": 7000.0}], "total": 7000.0}
```

La regla de calidad del repositorio está en [DEFINITION_OF_DONE.md](DEFINITION_OF_DONE.md).
