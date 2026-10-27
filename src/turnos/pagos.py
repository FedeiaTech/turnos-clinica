"""Cobro de turnos contra una pasarela de pagos externa.

El servicio no conoce a la pasarela real: recibe cualquier objeto que cumpla
el protocolo PasarelaPagos. Eso permite reemplazarla por dobles en las pruebas.
"""

from dataclasses import dataclass
from typing import Protocol


class ErrorPasarela(Exception):
    """Falla tecnica de la API externa (timeout, 5xx, respuesta invalida)."""


class CobroFallido(Exception):
    """El cobro no pudo completarse y la autorizacion ya fue anulada."""


@dataclass(frozen=True)
class Autorizacion:
    aprobada: bool
    codigo: str = ""
    motivo: str = ""


@dataclass(frozen=True)
class ResultadoCobro:
    aprobado: bool
    comprobante: str = ""
    motivo: str = ""


class PasarelaPagos(Protocol):
    def autorizar(self, monto: float, token_tarjeta: str) -> Autorizacion: ...

    def capturar(self, codigo_autorizacion: str) -> str: ...

    def anular(self, codigo_autorizacion: str) -> None: ...


class ServicioCobro:
    def __init__(self, pasarela: PasarelaPagos):
        self._pasarela = pasarela

    def cobrar(self, monto: float, token_tarjeta: str) -> ResultadoCobro:
        if monto <= 0:
            raise ValueError("El monto a cobrar debe ser positivo")
        if not token_tarjeta:
            raise ValueError("Falta el token de la tarjeta")

        autorizacion = self._pasarela.autorizar(monto, token_tarjeta)
        if not autorizacion.aprobada:
            # un rechazo es una respuesta de negocio: no se captura ni se anula
            return ResultadoCobro(aprobado=False, motivo=autorizacion.motivo)

        try:
            comprobante = self._pasarela.capturar(autorizacion.codigo)
        except ErrorPasarela as error:
            # el dinero quedo retenido: hay que liberar la autorizacion
            self._pasarela.anular(autorizacion.codigo)
            raise CobroFallido(f"No se pudo capturar {autorizacion.codigo}") from error

        return ResultadoCobro(aprobado=True, comprobante=comprobante)
