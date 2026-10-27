"""Compara la liquidacion vieja contra la nueva con los mismos turnos.

Uso: python auditoria/comparar_legacy.py
Se stubea el modulo yaml para poder importar el legacy sin instalar PyYAML 5.3.1.
"""

import itertools
import sys
import types
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path[:0] = [str(RAIZ / "src"), str(RAIZ / "auditoria" / "legacy")]
sys.modules.setdefault("yaml", types.ModuleType("yaml"))

import liquidacion_legacy  # noqa: E402

from turnos.liquidacion import Turno, liquidar  # noqa: E402

turnos = [
    Turno(i, tipo, estado, os_, 10_000 + i * 1_000, urg)
    for i, (tipo, estado, os_, urg) in enumerate(
        itertools.product(
            ["consulta", "estudio"], ["atendido", "ausente"], ["OSDE", "SWISS", "PUBLICA"], [True, False]
        )
    )
]
viejo = liquidacion_legacy.liquidar("Dra. Paz", [t.__dict__ for t in turnos], "2026-10", False)
nuevo = liquidar("Dra. Paz", "2026-10", turnos).total
print(f"turnos evaluados: {len(turnos)}")
print(f"total legacy:     {viejo:,.2f}")
print(f"total refactor:   {nuevo:,.2f}")
print("RESULTADO:", "IGUALES" if round(viejo, 2) == nuevo else "DISTINTOS")
sys.exit(0 if round(viejo, 2) == nuevo else 1)
