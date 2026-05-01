import json
from pathlib import Path


def cargar_datos(nombre_archivo="utils/arboles/amor_tree.json"):
    ruta = Path(nombre_archivo)

    if not ruta.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {nombre_archivo}")

    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)


def listar_arboles(directorio="utils/arboles"):
    """Escanea el directorio y retorna metadata de todos los árboles disponibles."""
    ruta_dir = Path(directorio)
    arboles = []

    for archivo in sorted(ruta_dir.glob("*.json")):
        try:
            with open(archivo, "r", encoding="utf-8") as f:
                datos = json.load(f)
            arboles.append({
                "archivo": str(archivo),
                "valor": datos.get("valor", archivo.stem),
                "descripcion": datos.get("descripcion", ""),
                "icon": datos.get("icon", "🎵"),
            })
        except Exception:
            pass  # Ignorar archivos mal formados

    return arboles
