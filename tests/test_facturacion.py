"""Suite de calcular_total / calcular_descuento con el patron Arrange-Act-Assert."""

import pytest

from turnos.facturacion import TOPE_DESCUENTO, calcular_descuento, calcular_total

# --------------------------------------------------------------------------- caso base


def test_paciente_sin_beneficios_paga_el_monto_completo():
    # Arrange
    monto, obra_social, edad, turnos_previos, urgente = 10_000, "PUBLICA", 30, 0, False

    # Act
    total = calcular_total(monto, obra_social, edad, turnos_previos, urgente)

    # Assert
    assert total == 10_000


def test_obra_social_premium_sin_urgencia_descuenta_10_por_ciento():
    # Arrange
    monto = 10_000

    # Act
    total = calcular_total(monto, "OSDE", edad=30, turnos_previos=0, urgente=False)

    # Assert
    assert total == 9_000


def test_descuentos_acumulados_se_limitan_al_tope():
    # Arrange: premium (10) + jubilado (15) + fidelidad (5) = 30 %
    obra_social, edad, turnos_previos = "SWISS", 70, 5

    # Act
    descuento = calcular_descuento(obra_social, edad, turnos_previos, urgente=False)
    total = calcular_total(8_000, obra_social, edad, turnos_previos, urgente=False)

    # Assert
    assert descuento == TOPE_DESCUENTO
    assert total == 6_000


# --------------------------------------------------------------------------- casos de borde


@pytest.mark.parametrize(
    ("edad", "esperado"),
    [(11, 8_500), (12, 10_000), (64, 10_000), (65, 8_500)],
    ids=["11-pediatrico", "12-fuera", "64-fuera", "65-jubilado"],
)
def test_limites_de_edad(edad, esperado):
    # Arrange
    monto = 10_000

    # Act
    total = calcular_total(monto, "PUBLICA", edad, turnos_previos=0, urgente=False)

    # Assert
    assert total == esperado


@pytest.mark.parametrize(("turnos_previos", "esperado"), [(3, 10_000), (4, 9_500)])
def test_limite_de_fidelidad(turnos_previos, esperado):
    # Arrange
    monto = 10_000

    # Act
    total = calcular_total(monto, "PUBLICA", 30, turnos_previos, urgente=False)

    # Assert
    assert total == esperado


def test_redondeo_a_centavos():
    # Arrange
    monto = 3_333.33

    # Act
    total = calcular_total(monto, "OSDE", 30, 0, urgente=False)

    # Assert
    assert total == 3_000.0


# --------------------------------------------------------------------------- inyeccion de errores


@pytest.mark.parametrize("monto", [0, -1, -10_000])
def test_monto_no_positivo_lanza_error_controlado(monto):
    # Arrange: el monto invalido llega por parametro

    # Act / Assert
    with pytest.raises(ValueError, match="positivo"):
        calcular_total(monto, "OSDE", 30, 0, urgente=False)


@pytest.mark.parametrize(("edad", "turnos_previos"), [(-1, 0), (30, -2)])
def test_edad_o_turnos_negativos_lanzan_error(edad, turnos_previos):
    # Act / Assert
    with pytest.raises(ValueError, match="negativos"):
        calcular_total(1_000, "OSDE", edad, turnos_previos, urgente=False)


# --------------------------------------------------------------------------- cobertura de ramas
# Cada fila fuerza una combinacion distinta de verdadero/falso en los cuatro if
# de calcular_descuento. Ver el analisis de cobertura en el informe del TP2.


@pytest.mark.parametrize(
    ("caso", "obra_social", "edad", "turnos", "urgente", "esperado"),
    [
        ("C1", "OSDE", 70, 5, False, 0.25),  # if1 V, if2 V (>=65), if3 V, tope V
        ("C2", "PUBLICA", 30, 0, False, 0.00),  # if1 F, if2 F, if3 F, tope F
        ("C3", "OSDE", 30, 0, True, 0.00),  # if1 F por urgencia
        ("C4", "PUBLICA", 8, 0, False, 0.15),  # if2 V por edad < 12
    ],
)
def test_ramas_de_calcular_descuento(caso, obra_social, edad, turnos, urgente, esperado):
    # Act
    descuento = calcular_descuento(obra_social, edad, turnos, urgente)

    # Assert
    assert descuento == pytest.approx(esperado), caso
