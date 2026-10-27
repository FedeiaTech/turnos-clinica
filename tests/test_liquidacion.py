"""Pruebas de la liquidacion refactorizada. Los valores esperados son los mismos
que devuelve liquidacion_legacy.liquidar para los mismos turnos (ver
auditoria/comparar_legacy.py), de modo que el refactor no cambia el comportamiento."""

from unittest.mock import Mock

import pytest
import requests

from turnos.liquidacion import Turno, calcular_honorario, liquidar
from turnos.publicacion import PublicacionFallida, publicar


@pytest.mark.parametrize(
    ("tipo", "obra_social", "urgente", "esperado"),
    [
        ("consulta", "OSDE", False, 7_000),
        ("consulta", "OSDE", True, 7_500),
        ("consulta", "PUBLICA", False, 6_000),
        ("consulta", "PUBLICA", True, 6_500),
        ("estudio", "SWISS", False, 5_000),
        ("estudio", "SWISS", True, 5_500),
        ("estudio", "PUBLICA", False, 4_000),
        ("estudio", "PUBLICA", True, 4_500),
    ],
)
def test_honorario_por_tipo_obra_social_y_urgencia(tipo, obra_social, urgente, esperado):
    # Arrange
    turno = Turno(1, tipo, "atendido", obra_social, 10_000, urgente)

    # Act
    honorario = calcular_honorario(turno)

    # Assert
    assert honorario == esperado


def test_tipo_desconocido_lanza_error():
    # Arrange
    turno = Turno(1, "cirugia", "atendido", "OSDE", 10_000)

    # Act / Assert
    with pytest.raises(ValueError, match="cirugia"):
        calcular_honorario(turno)


def test_liquidar_ignora_ausentes_y_suma_atendidos():
    # Arrange
    turnos = [
        Turno(1, "consulta", "atendido", "OSDE", 10_000),
        Turno(2, "estudio", "ausente", "OSDE", 10_000),
        Turno(3, "estudio", "atendido", "PUBLICA", 20_000, urgente=True),
    ]

    # Act
    liquidacion = liquidar("Dra. Paz", "2026-10", turnos)

    # Assert
    assert [item.turno for item in liquidacion.items] == [1, 3]
    assert liquidacion.total == 15_500


def test_publicar_envia_json_con_timeout():
    # Arrange
    sesion = Mock(spec=requests.Session)
    liquidacion = liquidar("Dra. Paz", "2026-10", [Turno(1, "consulta", "atendido", "OSDE", 1_000)])

    # Act
    publicar(liquidacion, sesion)

    # Assert
    args, kwargs = sesion.post.call_args
    assert kwargs["json"]["total"] == 700
    assert kwargs["timeout"] == 10
    sesion.post.return_value.raise_for_status.assert_called_once()


def test_publicar_traduce_errores_de_red():
    # Arrange
    sesion = Mock(spec=requests.Session)
    sesion.post.side_effect = requests.ConnectionError("sin red")
    liquidacion = liquidar("Dra. Paz", "2026-10", [])

    # Act / Assert
    with pytest.raises(PublicacionFallida):
        publicar(liquidacion, sesion)
