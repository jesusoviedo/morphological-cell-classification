# -*- coding: utf-8 -*-
"""Módulo de utilidades para el Trabajo Final de PDI.

Contiene funciones auxiliares para descargar la imagen base del trabajo
desde Google Drive y almacenarla localmente en la carpeta 'img'.
"""

import os
import requests

# Constantes para la descarga de la imagen base
ID_IMAGEN_BASE = "1zjP2KHLyJjB0iyuquUZY3tWyorw-ysU3"
NOMBRE_IMAGEN = "5ab3_0Artificial.bmp"

def descargar_imagen(id_archivo=ID_IMAGEN_BASE, nombre_destino=NOMBRE_IMAGEN):
    """Descarga un archivo desde Google Drive dado su ID.

    Construye la URL de descarga directa a partir del ID del archivo
    de Google Drive y descarga su contenido en memoria.

    Args:
        id_archivo (str): ID del archivo en Google Drive, extraído de
            la URL para compartir (parte entre '/d/' y '/view').
        nombre_destino (str): Nombre con el que se guardará el archivo
            descargado (por ejemplo 'celulas.png').

    Returns:
        str: Ruta completa donde se guardó la imagen descargada.

    Raises:
        requests.exceptions.RequestException: Si ocurre un error de red
            al intentar descargar el archivo.
    """
    url_descarga = f"https://drive.google.com/uc?export=download&id={id_archivo}"

    sesion = requests.Session()
    respuesta = sesion.get(url_descarga, stream=True)

    # Google Drive puede devolver una página de confirmación cuando el
    # archivo es grande. Se busca el token de confirmación en las cookies.
    token_confirmacion = None
    for clave, valor in respuesta.cookies.items():
        if clave.startswith("download_warning"):
            token_confirmacion = valor
            break

    if token_confirmacion:
        parametros = {"id": id_archivo, "confirm": token_confirmacion}
        respuesta = sesion.get(
            "https://drive.google.com/uc?export=download",
            params=parametros,
            stream=True,
        )

    respuesta.raise_for_status()

    ruta_destino = guardar_en_carpeta_img(respuesta.content, nombre_destino)
    return ruta_destino


def guardar_en_carpeta_img(contenido, nombre_destino, carpeta="img"):
    """Guarda contenido binario dentro de una carpeta local.

    Si la carpeta indicada no existe, la crea antes de guardar el
    archivo.

    Args:
        contenido (bytes): Contenido binario a escribir en el archivo.
        nombre_destino (str): Nombre con el que se guardará el archivo.
        carpeta (str): Carpeta donde se almacenará el archivo. Por
            defecto es 'img'.

    Returns:
        str: Ruta completa del archivo guardado.
    """
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)

    ruta_destino = os.path.join(carpeta, nombre_destino)

    with open(ruta_destino, "wb") as archivo:
        archivo.write(contenido)

    return ruta_destino


if __name__ == "__main__":

    ruta_guardada = descargar_imagen()
    print(f"Imagen guardada en: {ruta_guardada}")