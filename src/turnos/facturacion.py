"""Calculo del importe final de un turno.

Reglas de negocio (criterios de aceptacion de la historia "Facturar turno"):
- Obra social premium (OSDE, SWISS) sin urgencia: 10 % de descuento.
- Paciente menor de 12 anios o de 65 anios en adelante: 15 % de descuento.
- Paciente con mas de 3 turnos previos (fidelidad): 5 % de descuento.
- Los descuentos se suman, pero el total nunca supera el tope del 25 %.
"""

OBRAS_SOCIALES_PREMIUM = frozenset({"OSDE", "SWISS"})

DESCUENTO_PREMIUM = 0.10
DESCUENTO_EDAD = 0.15
DESCUENTO_FIDELIDAD = 0.05
TOPE_DESCUENTO = 0.25

EDAD_MINIMA_PEDIATRICA = 12
EDAD_MINIMA_JUBILADO = 65
UMBRAL_TURNOS_FIDELIDAD = 3


def calcular_descuento(obra_social: str, edad: int, turnos_previos: int, urgente: bool) -> float:
    """Devuelve el porcentaje de descuento acumulado, ya limitado por el tope."""
    descuento = 0.0
    if obra_social in OBRAS_SOCIALES_PREMIUM and not urgente:
        descuento += DESCUENTO_PREMIUM
    if edad < EDAD_MINIMA_PEDIATRICA or edad >= EDAD_MINIMA_JUBILADO:
        descuento += DESCUENTO_EDAD
    if turnos_previos > UMBRAL_TURNOS_FIDELIDAD:
        descuento += DESCUENTO_FIDELIDAD
    if descuento > TOPE_DESCUENTO:
        descuento = TOPE_DESCUENTO
    return descuento


def calcular_total(
    monto: float, obra_social: str, edad: int, turnos_previos: int, urgente: bool
) -> float:
    """Aplica el descuento al monto base y redondea a centavos."""
    if monto <= 0:
        raise ValueError(f"El monto debe ser positivo, se recibio {monto}")
    if edad < 0 or turnos_previos < 0:
        raise ValueError("La edad y los turnos previos no pueden ser negativos")
    descuento = calcular_descuento(obra_social, edad, turnos_previos, urgente)
    return round(monto * (1 - descuento), 2)
