# -*- coding: utf-8 -*-
"""Punto 1: Generación de la imagen A.

Enunciado:
    ¿Cómo, de forma automática, usando SOLAMENTE el proceso de
    reconstrucción, las operaciones lógicas (AND, OR, XOR, NAND, NOR) y
    la inversión de imagen, generar la imagen A sin pedazos ni células
    truncadas en los bordes de la imagen?
"""

import numpy as np

from util import descargar_imagen
from util import cargar_imagen_binaria
from util import operacion_and
from util import operacion_xor
from util import guardar_imagen
from util import invertir_imagen
from util import NOMBRE_IMAGEN
from util import reconstruccion_morfologica

def main():
    """Función principal del programa."""

    print(f"Descargando imagen {NOMBRE_IMAGEN}...")

    ruta_imagen = descargar_imagen()
    print(f"Imagen {NOMBRE_IMAGEN} descargada en: {ruta_imagen}")

    imagen_binaria = cargar_imagen_binaria(ruta_imagen)

    print(imagen_binaria)

    imagen_marco = np.zeros_like(imagen_binaria)

    imagen_marco[0, :] = 255
    imagen_marco[-1, :] = 255
    imagen_marco[:, 0] = 255
    imagen_marco[:, -1] = 255

    print(imagen_marco)

    imagen_operacion_and = operacion_and(imagen_binaria, imagen_marco)

    print(imagen_operacion_and)

    imagen_con_borde = reconstruccion_morfologica(imagen_operacion_and, imagen_binaria)

    imagen_a = operacion_xor(imagen_binaria, imagen_con_borde)

    imagen_a = invertir_imagen(imagen_a)

    guardar_imagen(imagen_a, "imagen_a.png")



if __name__ == "__main__":
    main()