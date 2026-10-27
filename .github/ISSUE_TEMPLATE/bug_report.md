---
name: Reporte de defecto
about: Un comportamiento del sistema no coincide con lo especificado
title: "BUG: [resumen breve del fallo]"
labels: ["bug", "status: triage"]
assignees: []
---

## Descripción técnica del problema

<!-- Qué falla, en qué módulo/función y bajo qué condición. Sin opiniones, solo hechos. -->

- **Módulo / función:** `src/turnos/...`
- **Versión o commit:** <!-- git rev-parse --short HEAD -->
- **Entorno:** <!-- SO, versión de Python (python --version) -->
- **Severidad:** <!-- bloqueante | alta | media | baja -->

## Pasos exactos para reproducir

<!-- Lista numerada y determinista: otra persona debe obtener el mismo fallo siguiéndola. -->

1.
2.
3.

**Datos de entrada usados:**

```text

```

## Comportamiento esperado

<!-- Qué debería pasar según la especificación o el criterio de aceptación. Citar la regla. -->

## Comportamiento observado

<!-- Qué pasa realmente: valor devuelto, excepción, mensaje de consola. -->

## Evidencias adjuntas

<!-- Traza completa, log, captura o test que falla. Pegar la salida de consola tal cual. -->

```text

```

## Test que reproduce el defecto (opcional)

```python

```

## Checklist del reporte

- [ ] Busqué issues abiertos y no está reportado.
- [ ] Los pasos reproducen el fallo en la última versión de `main`.
- [ ] Adjunté la salida de consola o el test que falla.
