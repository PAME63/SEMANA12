"""
ArchivoServicio.

Funciones utilitarias para leer y escribir archivos JSON.
No contiene logica de negocio ni de indices: solo persistencia en disco.
"""

import json
import os


def cargar_json(ruta):
    """Carga una lista de diccionarios desde un archivo JSON.

    Si el archivo no existe o esta vacio/corrupto, devuelve una lista vacia
    para permitir que el sistema arranque igualmente en un entorno nuevo.
    """
    if not os.path.exists(ruta):
        return []
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            contenido = archivo.read().strip()
            if not contenido:
                return []
            return json.loads(contenido)
    except (json.JSONDecodeError, OSError):
        return []


def guardar_json(ruta, datos):
    """Guarda una lista de diccionarios en un archivo JSON con formato legible."""
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)
