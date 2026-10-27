"""Experimento del TP2: un unico caso que recorre todas las sentencias de
calcular_descuento pero deja ramas sin evaluar en falso."""

from turnos.facturacion import calcular_descuento


def test_c1_todo_verdadero():
    assert calcular_descuento("OSDE", 70, 5, urgente=False) == 0.25
