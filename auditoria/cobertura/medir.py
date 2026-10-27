"""Corre un archivo de pruebas con cobertura de sentencias y de ramas y reporta
solo la funcion calcular_descuento (usa la seccion "functions" del JSON de coverage).

Uso: python auditoria/cobertura/medir.py auditoria/cobertura/test_caso_unico.py
"""

import json
import subprocess
import sys

prueba = sys.argv[1]
for modo in ("sentencias", "ramas"):
    rc = f"auditoria/cobertura/{modo}.coveragerc"
    subprocess.run(
        [sys.executable, "-m", "coverage", "run", f"--rcfile={rc}", "-m", "pytest", "-q",
         "-p", "no:cacheprovider", prueba],
        check=True, capture_output=True,
    )
    subprocess.run([sys.executable, "-m", "coverage", "json", f"--rcfile={rc}", "-q", "-o", "cov.json"],
                   check=True)
    datos = json.load(open("cov.json", encoding="utf-8"))
    archivo = next(v for k, v in datos["files"].items() if k.endswith("facturacion.py"))
    f = archivo["functions"]["calcular_descuento"]["summary"]
    linea = f"[{modo:10}] sentencias {f['covered_lines']}/{f['num_statements']}"
    if modo == "ramas":
        linea += f" | ramas {f['covered_branches']}/{f['num_branches']}"
        faltan = archivo["functions"]["calcular_descuento"].get("missing_branches", [])
        linea += f" | sin recorrer {faltan}"
    print(linea + f" | cobertura {f['percent_covered_display']} %")
