import json
from pathlib import Path

def cargar_datos(nombre_archivo="utils/arboles/amor_tree.json"):
    ruta = Path(nombre_archivo)

    if not ruta.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {nombre_archivo}")

    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)