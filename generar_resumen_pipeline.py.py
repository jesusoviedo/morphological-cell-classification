# -*- coding: utf-8 -*-
"""Genera un panel resumen con la imagen base y los resultados de los 8 puntos.

No es uno de los 8 puntos del enunciado -- es una utilidad aparte,
pensada para el cierre del informe: arma un único panel con la imagen
base y cada resultado canónico (A a G, más Tipo 2 y Tipo 3), para
mostrar de un vistazo la evolución completa del pipeline.
"""

import os
import cv2
# Importar constantes y funciones auxiliares
from util import CARPETA_IMG
from util import NOMBRE_IMAGEN
from util import NOMBRE_IMAGEN_A
from util import NOMBRE_IMAGEN_B
from util import NOMBRE_IMAGEN_C
from util import NOMBRE_IMAGEN_D
from util import NOMBRE_IMAGEN_E
from util import NOMBRE_IMAGEN_F
from util import NOMBRE_IMAGEN_G
from util import NOMBRE_IMAGEN_TIPO_2
from util import NOMBRE_IMAGEN_TIPO_3
from util import graficar_imagenes


def cargar_para_mostrar(nombre_archivo):
    """Carga una imagen tal como está guardada, sin invertir.

    A diferencia de cargar_imagen_resultado, esta función no invierte
    la imagen -- se usa solo para mostrarla en el panel resumen, en la
    misma polaridad visual en la que ya está guardada en disco.

    Args:
        nombre_archivo (str): Nombre del archivo a cargar, dentro de
            la carpeta de imágenes del proyecto.

    Returns:
        numpy.ndarray: Imagen cargada en escala de grises.

    Raises:
        FileNotFoundError: Si no se pudo leer la imagen desde la ruta
            indicada.
    """
    ruta = os.path.join(CARPETA_IMG, nombre_archivo)
    imagen = cv2.imread(ruta, cv2.IMREAD_GRAYSCALE)

    if imagen is None:
        raise FileNotFoundError(f"No se pudo leer la imagen: {ruta}")

    return imagen


def main():
    """Función principal del programa."""
    nombres = [
        NOMBRE_IMAGEN,
        NOMBRE_IMAGEN_A,
        NOMBRE_IMAGEN_B,
        NOMBRE_IMAGEN_C,
        NOMBRE_IMAGEN_D,
        NOMBRE_IMAGEN_E,
        NOMBRE_IMAGEN_F,
        NOMBRE_IMAGEN_G,
        NOMBRE_IMAGEN_TIPO_2,
        NOMBRE_IMAGEN_TIPO_3,
    ]
    titulos = [
        "Base",
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "Tipo 2",
        "Tipo 3",
    ]

    imagenes = [cargar_para_mostrar(nombre) for nombre in nombres]

    ruta = graficar_imagenes(
        imagenes,
        titulos,
        prefijo="resumen",
        filas=2,
        columnas=5,
        titulo_general="Síntesis del pipeline completo",
    )
    print(f"Panel resumen guardado en: {ruta}")


if __name__ == "__main__":
    main()