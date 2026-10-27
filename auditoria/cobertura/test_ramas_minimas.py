"""Experimento del TP2: C1 + C2 alcanzan el 100 % de ramas de calcular_descuento."""

from turnos.facturacion import calcular_descuento


def test_c1_todo_verdadero():
    assert calcular_descuento("OSDE", 70, 5, urgente=False) == 0.25


def test_c2_todo_falso():
    assert calcular_descuento("PUBLICA", 30, 0, urgente=False) == 0.0
