import requests, yaml, os, json
import sys

CONFIG = None
total_general = 0


def cargar():
    global CONFIG
    f = open("config.yml")
    CONFIG = yaml.load(f)
    return CONFIG


def liquidar(medico, turnos, mes, enviar):
    global total_general
    res = []
    total = 0
    for t in turnos:
        if t["estado"] == "atendido":
            if t["tipo"] == "consulta":
                if t["obra_social"] == "OSDE" or t["obra_social"] == "SWISS":
                    if t["urgente"]:
                        monto = t["valor"] * 0.7
                        monto = monto + 500
                        monto = round(monto, 2)
                        res.append({"turno": t["id"], "monto": monto})
                        total = total + monto
                    else:
                        monto = t["valor"] * 0.7
                        monto = round(monto, 2)
                        res.append({"turno": t["id"], "monto": monto})
                        total = total + monto
                else:
                    if t["urgente"]:
                        monto = t["valor"] * 0.6
                        monto = monto + 500
                        monto = round(monto, 2)
                        res.append({"turno": t["id"], "monto": monto})
                        total = total + monto
                    else:
                        monto = t["valor"] * 0.6
                        monto = round(monto, 2)
                        res.append({"turno": t["id"], "monto": monto})
                        total = total + monto
            elif t["tipo"] == "estudio":
                if t["obra_social"] == "OSDE" or t["obra_social"] == "SWISS":
                    if t["urgente"]:
                        monto = t["valor"] * 0.5
                        monto = monto + 500
                        monto = round(monto, 2)
                        res.append({"turno": t["id"], "monto": monto})
                        total = total + monto
                    else:
                        monto = t["valor"] * 0.5
                        monto = round(monto, 2)
                        res.append({"turno": t["id"], "monto": monto})
                        total = total + monto
                else:
                    if t["urgente"]:
                        monto = t["valor"] * 0.4
                        monto = monto + 500
                        monto = round(monto, 2)
                        res.append({"turno": t["id"], "monto": monto})
                        total = total + monto
                    else:
                        monto = t["valor"] * 0.4
                        monto = round(monto, 2)
                        res.append({"turno": t["id"], "monto": monto})
                        total = total + monto
            else:
                print("tipo desconocido")
        elif t["estado"] == "ausente":
            if t["tipo"] == "consulta":
                pass
            else:
                pass
        else:
            pass
    total_general = total_general + total
    if enviar:
        try:
            r = requests.post(
                "http://api.clinica.local/liquidaciones",
                data=json.dumps({"medico": medico, "mes": mes, "items": res, "total": total}),
                verify=False,
            )
            if r.status_code == 200:
                print("ok")
            else:
                print("error")
        except:
            pass
    return total
