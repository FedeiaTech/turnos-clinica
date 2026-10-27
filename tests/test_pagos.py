"""Pruebas de ServicioCobro aisladas de la API de pagos mediante dobles de prueba.

- Stub: devuelve respuestas fijas para probar como reacciona el servicio (estado).
- Mock: registra las llamadas para verificar el protocolo con la pasarela (comportamiento).
"""

from unittest.mock import Mock, call

import pytest

from turnos.pagos import (
    Autorizacion,
    CobroFallido,
    ErrorPasarela,
    PasarelaPagos,
    ResultadoCobro,
    ServicioCobro,
)


class StubPasarela:
    """Stub escrito a mano: respuestas enlatadas, sin logica ni registro de llamadas."""

    def __init__(self, autorizacion: Autorizacion, comprobante: str = "CMP-001"):
        self._autorizacion = autorizacion
        self._comprobante = comprobante

    def autorizar(self, monto, token_tarjeta):
        return self._autorizacion

    def capturar(self, codigo_autorizacion):
        return self._comprobante

    def anular(self, codigo_autorizacion):
        return None


# --------------------------------------------------------------------------- stubs (estado)


def test_cobro_aprobado_devuelve_comprobante():
    # Arrange
    pasarela = StubPasarela(Autorizacion(aprobada=True, codigo="AUT-77"), comprobante="CMP-900")
    servicio = ServicioCobro(pasarela)

    # Act
    resultado = servicio.cobrar(9_000, "tok_visa")

    # Assert
    assert resultado == ResultadoCobro(aprobado=True, comprobante="CMP-900")


def test_cobro_rechazado_informa_el_motivo_de_la_pasarela():
    # Arrange
    pasarela = StubPasarela(Autorizacion(aprobada=False, motivo="fondos insuficientes"))
    servicio = ServicioCobro(pasarela)

    # Act
    resultado = servicio.cobrar(9_000, "tok_visa")

    # Assert
    assert resultado.aprobado is False
    assert resultado.motivo == "fondos insuficientes"
    assert resultado.comprobante == ""


@pytest.mark.parametrize(("monto", "token"), [(0, "tok"), (-5, "tok"), (100, "")])
def test_datos_invalidos_no_llegan_a_la_pasarela(monto, token):
    # Arrange
    pasarela = Mock(spec=PasarelaPagos)
    servicio = ServicioCobro(pasarela)

    # Act / Assert
    with pytest.raises(ValueError):
        servicio.cobrar(monto, token)
    pasarela.autorizar.assert_not_called()


# --------------------------------------------------------------------------- mocks (comportamiento)


def test_cobro_aprobado_autoriza_y_captura_una_sola_vez_en_orden():
    # Arrange
    pasarela = Mock(spec=PasarelaPagos)
    pasarela.autorizar.return_value = Autorizacion(aprobada=True, codigo="AUT-1")
    pasarela.capturar.return_value = "CMP-1"
    servicio = ServicioCobro(pasarela)

    # Act
    servicio.cobrar(5_000, "tok_master")

    # Assert: se interroga al mock, no al resultado
    assert pasarela.mock_calls == [call.autorizar(5_000, "tok_master"), call.capturar("AUT-1")]
    pasarela.anular.assert_not_called()


def test_cobro_rechazado_nunca_intenta_capturar():
    # Arrange
    pasarela = Mock(spec=PasarelaPagos)
    pasarela.autorizar.return_value = Autorizacion(aprobada=False, motivo="tarjeta vencida")
    servicio = ServicioCobro(pasarela)

    # Act
    servicio.cobrar(5_000, "tok_master")

    # Assert
    pasarela.autorizar.assert_called_once_with(5_000, "tok_master")
    pasarela.capturar.assert_not_called()
    pasarela.anular.assert_not_called()


def test_falla_en_la_captura_anula_la_autorizacion():
    # Arrange
    pasarela = Mock(spec=PasarelaPagos)
    pasarela.autorizar.return_value = Autorizacion(aprobada=True, codigo="AUT-9")
    pasarela.capturar.side_effect = ErrorPasarela("timeout")
    servicio = ServicioCobro(pasarela)

    # Act
    with pytest.raises(CobroFallido):
        servicio.cobrar(5_000, "tok_master")

    # Assert
    pasarela.anular.assert_called_once_with("AUT-9")
