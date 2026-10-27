"""Envio de la liquidacion a la API de administracion."""

from dataclasses import asdict

import requests

from turnos.liquidacion import Liquidacion

URL_LIQUIDACIONES = "https://api.clinica.local/liquidaciones"
TIMEOUT_SEGUNDOS = 10


class PublicacionFallida(Exception):
    pass


def publicar(liquidacion: Liquidacion, sesion: requests.Session | None = None) -> None:
    sesion = sesion or requests.Session()
    cuerpo = {**asdict(liquidacion), "total": liquidacion.total}
    try:
        respuesta = sesion.post(URL_LIQUIDACIONES, json=cuerpo, timeout=TIMEOUT_SEGUNDOS)
        respuesta.raise_for_status()
    except requests.RequestException as error:
        raise PublicacionFallida(
            f"No se pudo publicar la liquidacion de {liquidacion.mes}"
        ) from error
