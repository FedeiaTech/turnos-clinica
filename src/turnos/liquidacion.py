"""Liquidacion mensual de honorarios medicos.

Reemplaza a auditoria/legacy/liquidacion_legacy.py. Las ocho ramas duplicadas
del original se reducen a una tabla de porcentajes y una sola funcion de calculo.
"""

from dataclasses import dataclass

OBRAS_SOCIALES_PREMIUM = frozenset({"OSDE", "SWISS"})
RECARGO_URGENCIA = 500

# porcentaje del valor del turno que cobra el medico: (tipo, es_premium) -> porcentaje
PORCENTAJE_HONORARIO = {
    ("consulta", True): 0.7,
    ("consulta", False): 0.6,
    ("estudio", True): 0.5,
    ("estudio", False): 0.4,
}


@dataclass(frozen=True)
class Turno:
    id: int
    tipo: str
    estado: str
    obra_social: str
    valor: float
    urgente: bool = False


@dataclass(frozen=True)
class ItemLiquidacion:
    turno: int
    monto: float


@dataclass(frozen=True)
class Liquidacion:
    medico: str
    mes: str
    items: tuple[ItemLiquidacion, ...]

    @property
    def total(self) -> float:
        return round(sum(item.monto for item in self.items), 2)


def calcular_honorario(turno: Turno) -> float:
    clave = (turno.tipo, turno.obra_social in OBRAS_SOCIALES_PREMIUM)
    if clave not in PORCENTAJE_HONORARIO:
        raise ValueError(f"Tipo de turno desconocido: {turno.tipo!r}")
    monto = turno.valor * PORCENTAJE_HONORARIO[clave]
    if turno.urgente:
        monto += RECARGO_URGENCIA
    return round(monto, 2)


def liquidar(medico: str, mes: str, turnos: list[Turno]) -> Liquidacion:
    """Solo se liquidan los turnos atendidos; ausentes y cancelados no generan honorario."""
    items = tuple(
        ItemLiquidacion(turno.id, calcular_honorario(turno))
        for turno in turnos
        if turno.estado == "atendido"
    )
    return Liquidacion(medico, mes, items)
