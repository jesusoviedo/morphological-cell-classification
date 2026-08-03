# -*- coding: utf-8 -*-
"""Punto 1: Generación de la imagen A.

Enunciado:
    ¿Cómo, de forma automática, usando SOLAMENTE el proceso de
    reconstrucción, las operaciones lógicas (AND, OR, XOR, NAND, NOR) y
    la inversión de imagen, generar la imagen A sin pedazos ni células
    truncadas en los bordes de la imagen?
"""

import numpy as np
# Importar funciones auxiliares
from util import NOMBRE_IMAGEN
from util import descargar_imagen
from util import cargar_imagen_binaria
from util import operacion_and
from util import operacion_xor
from util import guardar_imagen
from util import invertir_imagen
from util import reconstruccion_morfologica
from util import graficar_imagenes


def obtener_imagen_base():
    """Obtiene la imagen base del trabajo, ya binarizada.
 
    Descarga la imagen base si todavía no existe localmente (la
    verificación la hace internamente descargar_imagen), y luego la
    carga en escala de grises y la binariza con el criterio por
    defecto del proyecto (umbral fijo en 127).
 
    Returns:
        numpy.ndarray: Imagen base binarizada (0/255).
    """
    print(f"Descargando imagen {NOMBRE_IMAGEN}...")
    ruta_imagen = descargar_imagen()

    imagen_original = cargar_imagen_binaria(ruta_imagen, invertir_automatico=False)
    imagen_mascara = cargar_imagen_binaria(ruta_imagen)
    
    print(f"Imagen {NOMBRE_IMAGEN} descargada en: {ruta_imagen}")

    return imagen_original, imagen_mascara


def crear_marcador_borde(imagen_binaria):
    """Construye el marcador para eliminar objetos que tocan el borde.
 
    Genera una máscara con 255 únicamente en el marco exterior (fila
    superior, fila inferior, columna izquierda y columna derecha) de
    la imagen, y la combina con AND contra la imagen binaria. El
    resultado conserva solo los píxeles de la imagen original que
    caen justo sobre el borde, quedando en 0 en todo lo demás.
 
    Args:
        imagen_binaria (numpy.ndarray): Imagen binaria (0/255) sobre
            la que se construye el marcador.
 
    Returns:
        numpy.ndarray: Marcador (0/255), subconjunto de
        imagen_binaria, con los píxeles del borde encendidos.
    """
    marco = np.zeros_like(imagen_binaria)
    marco[0, :] = 255
    marco[-1, :] = 255
    marco[:, 0] = 255
    marco[:, -1] = 255
 
    return operacion_and(imagen_binaria, marco)


def generar_imagen_a(imagen_mascara, imagen_marcador):
    """Genera la imagen A: células sin truncar en los bordes.
 
    Construye el marcador de borde, reconstruye a partir de él los
    objetos que tocan el borde de la imagen, y elimina esos objetos de
    la imagen original mediante XOR (válido porque la reconstrucción
    es siempre un subconjunto de la imagen original).
 
    Args:
        imagen_mascara (numpy.ndarray): Imagen mascarada (0/255) de
            entrada, con todas las células.
        imagen_marcador (numpy.ndarray): Marcador de borde (0/255).
 
    Returns:
        numpy.ndarray: Imagen A (0/255), sin las células que tocan el
        borde.
    """

    image_con_objeto_borde = reconstruccion_morfologica(imagen_marcador, imagen_mascara)
    nueva_imagen = operacion_xor(imagen_mascara, image_con_objeto_borde)
    return invertir_imagen(nueva_imagen), image_con_objeto_borde


def main():
    """Función principal del programa."""

    PREFIJO = "punto1"

    imagen_original, imagen_mascara = obtener_imagen_base()
    guardar_imagen(imagen_original, f"{PREFIJO}_imagen_original.png")
    guardar_imagen(imagen_mascara, f"{PREFIJO}_imagen_mascara.png")

    imagen_marcador = crear_marcador_borde(imagen_mascara)
    guardar_imagen(imagen_marcador, f"{PREFIJO}_imagen_marcador.png")

    imagen_a, image_con_objeto_borde = generar_imagen_a(imagen_mascara, imagen_marcador)
    guardar_imagen(image_con_objeto_borde, f"{PREFIJO}_image_con_objeto_borde.png")
    guardar_imagen(imagen_a, "imagen_a.png")

    lista_imagenes = [imagen_original, imagen_mascara, imagen_marcador, image_con_objeto_borde,imagen_a]
    lista_titulos = ["Imagen Original", "Imagen Mascara", "Imagen Marcador", "Imagen con Objetos de Borde", "Imagen A"]
    graficar_imagenes(lista_imagenes, 
                      lista_titulos, 
                      prefijo=PREFIJO, 
                      filas=2, 
                      columnas=3, 
                      titulo_general="Punto 1: Células sin sin pedazos ni células truncadas en los bordes")


if __name__ == "__main__":
    main()