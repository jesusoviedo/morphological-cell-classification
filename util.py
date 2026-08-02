# -*- coding: utf-8 -*-
"""Módulo de utilidades para el Trabajo Final de PDI.

Contiene funciones auxiliares para descargar la imagen base del trabajo
desde Google Drive y almacenarla localmente en la carpeta 'img'.
"""

import os
import requests
import cv2

# Constantes para la descarga de la imagen base
ID_IMAGEN_BASE = "1zjP2KHLyJjB0iyuquUZY3tWyorw-ysU3"
NOMBRE_IMAGEN = "5ab3_0Artificial.bmp"
CARPETA_IMG = "img"

def descargar_imagen(id_archivo=ID_IMAGEN_BASE, nombre_destino=NOMBRE_IMAGEN):
    """Descarga un archivo desde Google Drive dado su ID.

    Construye la URL de descarga directa a partir del ID del archivo
    de Google Drive y descarga su contenido en memoria.

    Args:
        id_archivo (str, optional): ID del archivo en Google Drive,
            extraído de la URL para compartir (parte entre '/d/' y
            '/view'). Por defecto es ID_IMAGEN_BASE.
        nombre_destino (str, optional): Nombre con el que se guardará
            el archivo descargado. Por defecto es NOMBRE_IMAGEN.

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


def guardar_en_carpeta_img(contenido, nombre_destino, carpeta=CARPETA_IMG):
    """Guarda contenido binario dentro de una carpeta local.

    Si la carpeta indicada no existe, la crea antes de guardar el
    archivo.

    Args:
        contenido (bytes): Contenido binario a escribir en el archivo.
        nombre_destino (str): Nombre con el que se guardará el archivo.
        carpeta (str, optional): Carpeta donde se almacenará el
            archivo. Por defecto es 'img'.

    Returns:
        str: Ruta completa del archivo guardado.
    """
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)

    ruta_destino = os.path.join(carpeta, nombre_destino)

    with open(ruta_destino, "wb") as archivo:
        archivo.write(contenido)

    return ruta_destino


def binarizar_imagen(imagen, umbral=127, valor_maximo=255):
    """Convierte una imagen en escala de grises a una imagen binaria.

    Por defecto utiliza un umbral fijo de 127. Si se pasa umbral=None, el
    umbral se calcula automáticamente mediante el método de Otsu.

    Args:
        imagen (numpy.ndarray): Imagen en escala de grises a binarizar.
        umbral (int, optional): Valor de umbral fijo a utilizar. Si es
            None, el umbral se calcula automáticamente con el método
            de Otsu. Por defecto es 127.
        valor_maximo (int, optional): Valor asignado a los píxeles que
            superan el umbral. Por defecto es 255.

    Returns:
        numpy.ndarray: Imagen binaria resultante.
    """
    if umbral is None:
        _, imagen_binaria = cv2.threshold(imagen, 
                                          0, 
                                          valor_maximo, 
                                          cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    else:
        _, imagen_binaria = cv2.threshold(imagen, 
                                          umbral, 
                                          valor_maximo, 
                                          cv2.THRESH_BINARY)    

    return imagen_binaria


def cargar_imagen_binaria(ruta_imagen, umbral=127, valor_maximo=255):
    """Carga una imagen desde disco y la convierte a binaria.

    Lee la imagen en escala de grises desde la ruta indicada y aplica
    la binarización correspondiente, siguiendo el criterio de umbral
    fijo empleado en el material de cátedra.

    Args:
        ruta_imagen (str): Ruta del archivo de imagen a cargar.
        umbral (int, optional): Valor de umbral fijo a utilizar. Si es
            None, el umbral se calcula automáticamente con el método
            de Otsu. Por defecto es 127.
        valor_maximo (int, optional): Valor asignado a los píxeles que
            superan el umbral. Por defecto es 255.

    Returns:
        numpy.ndarray: Imagen binaria resultante.

    Raises:
        FileNotFoundError: Si no se pudo leer la imagen desde la ruta
            indicada.
    """
    imagen_gris = cv2.imread(ruta_imagen, cv2.IMREAD_GRAYSCALE)

    if imagen_gris is None:
        raise FileNotFoundError(f"No se pudo leer la imagen: {ruta_imagen}")

    return binarizar_imagen(imagen_gris, umbral, valor_maximo)


def guardar_imagen(imagen, nombre_destino, carpeta=CARPETA_IMG):
    """Guarda una imagen en disco dentro de una carpeta local.

    Si la carpeta indicada no existe, la crea antes de guardar la
    imagen. Pensada para almacenar los resultados intermedios de cada
    punto (imagen A, B, C, etc.) en la misma carpeta donde se guardó
    la imagen base.

    Args:
        imagen (numpy.ndarray): Imagen a guardar.
        nombre_destino (str): Nombre del archivo de salida, incluyendo
            extensión (por ejemplo 'imagen_a.png').
        carpeta (str, optional): Carpeta donde se guardará la imagen.
            Por defecto es 'img'.

    Returns:
        str: Ruta completa donde se guardó la imagen.

    Raises:
        IOError: Si OpenCV no pudo escribir la imagen en la ruta
            indicada (por ejemplo, por una extensión no soportada).
    """
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)

    ruta_destino = os.path.join(carpeta, nombre_destino)

    if not cv2.imwrite(ruta_destino, imagen):
        raise IOError(f"No se pudo guardar la imagen en: {ruta_destino}")

    return ruta_destino


def cargar_imagen_resultado(nombre_archivo, carpeta=CARPETA_IMG):
    """Carga una imagen resultado previamente guardada en disco.

    Pensada para que un punto lea el resultado guardado por un punto
    anterior (por ejemplo, que el Punto 2 cargue la imagen A generada
    por el Punto 1) sin necesidad de binarizarla nuevamente.

    Args:
        nombre_archivo (str): Nombre del archivo a cargar, incluyendo
            extensión (por ejemplo 'imagen_a.png').
        carpeta (str, optional): Carpeta donde buscar el archivo. Por
            defecto es 'img'.

    Returns:
        numpy.ndarray: Imagen cargada en escala de grises.

    Raises:
        FileNotFoundError: Si no se pudo leer la imagen desde la ruta
            indicada.
    """
    ruta_origen = os.path.join(carpeta, nombre_archivo)
    imagen = cv2.imread(ruta_origen, cv2.IMREAD_GRAYSCALE)

    if imagen is None:
        raise FileNotFoundError(f"No se pudo leer la imagen: {ruta_origen}")

    return imagen