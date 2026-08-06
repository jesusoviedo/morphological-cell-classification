# -*- coding: utf-8 -*-
"""Punto 4: Generación de la imagen D.

Enunciado:
    ¿Cómo, de forma automática, a partir de la imagen C, usando
    SOLAMENTE el proceso de reconstrucción, las operaciones lógicas
    (AND, OR, XOR, NAND, NOR) y la inversión de imagen, generar la
    imagen D de todas las células no agujereadas (sin citoplasma) de
    Tipo 1?

Pasos realizados:
    1. Se cargan las imágenes A y C generadas por los puntos 1 y 3,
       directamente en polaridad operativa.
    2. Se resta (XOR) la imagen C de la imagen A: como C es siempre
       subconjunto de A (toda célula agujereada es también una
       célula), esto equivale a una resta de conjuntos válida.
    3. Se invierte el resultado para volver a la polaridad visual:
       imagen D.

    No se usa reconstrucción morfológica en este punto: el enunciado
    la permite, pero no la exige, y una sola operación lógica alcanza
    para llegar al resultado.
"""

# Importar constantes y funciones auxiliares
from util import NOMBRE_IMAGEN_A
from util import NOMBRE_IMAGEN_C
from util import NOMBRE_IMAGEN_D
from util import OPERACION_XOR
from util import cargar_imagen_resultado
from util import guardar_imagen
from util import invertir_imagen
from util import operacion_logica
from util import graficar_imagenes


def obtener_imagenes_previas():
    """Obtiene las imágenes A y C generadas por los puntos anteriores.

    Carga "imagen_a.png" e "imagen_c.png" directamente en polaridad
    operativa (invertir=True, el valor por defecto), que es la única
    que necesita este punto: ni A ni C se usan en su polaridad visual
    en ningún paso del cómputo.

    Returns:
        tuple: Tupla (imagen_a, imagen_c), ambas numpy.ndarray (0/255),
        en polaridad operativa (células en 255).
    """
    imagen_a = cargar_imagen_resultado(NOMBRE_IMAGEN_A)
    imagen_c = cargar_imagen_resultado(NOMBRE_IMAGEN_C)

    return imagen_a, imagen_c


def generar_imagen_d(imagen_a, imagen_c):
    """Genera la imagen D: células no agujereadas (Tipo 1).

    La imagen C (células agujereadas, Tipo 2, 3 y 4) es siempre
    subconjunto de la imagen A (todas las células), ya que toda
    célula agujereada también es una célula. Por eso, XOR(A, C) se
    comporta como una resta de conjuntos válida (el mismo principio
    aplicado en el punto 1 y el punto 2): deja únicamente los
    píxeles que están en A pero no en C, es decir, las células sin
    agujero — Tipo 1.

    No hace falta ninguna reconstrucción para este punto: el
    enunciado permite usarla, pero no la exige, y una sola operación
    lógica alcanza para llegar al resultado.

    Args:
        imagen_a (numpy.ndarray): Imagen A (0/255), en polaridad
            operativa (células en 255).
        imagen_c (numpy.ndarray): Imagen C (0/255), en polaridad
            operativa (células agujereadas en 255).

    Returns:
        tuple: Tupla (imagen_d, imagen_d_operativa). imagen_d es el
        resultado final (0/255), invertido a polaridad visual (fondo
        blanco, células negras), lista para el informe y para los
        puntos siguientes. imagen_d_operativa es el mismo resultado
        antes de invertir, en polaridad operativa, pensada para
        mostrar el paso intermedio en el informe.
    """
    imagen_d_operativa = operacion_logica(imagen_a, imagen_c, OPERACION_XOR)
    imagen_d = invertir_imagen(imagen_d_operativa)

    return imagen_d, imagen_d_operativa


def main():
    """Función principal del programa."""

    PREFIJO = "punto4"

    # Obtener las imágenes A y C generadas por los puntos anteriores
    imagen_a, imagen_c = obtener_imagenes_previas()

    ruta_imagen_a = guardar_imagen(imagen_a, "imagen_a_operativa.png", prefijo=PREFIJO)
    print(f"Imagen A (operativa) guardada en: {ruta_imagen_a}")

    ruta_imagen_c = guardar_imagen(imagen_c, "imagen_c_operativa.png", prefijo=PREFIJO)
    print(f"Imagen C (operativa) guardada en: {ruta_imagen_c}")

    # Generar la imagen D
    imagen_d, imagen_d_operativa = generar_imagen_d(imagen_a, imagen_c)

    ruta_imagen_d_operativa = guardar_imagen(imagen_d_operativa, "imagen_d_operativa.png", prefijo=PREFIJO)
    print(f"Imagen D (operativa) guardada en: {ruta_imagen_d_operativa}")

    ruta_imagen_d = guardar_imagen(imagen_d, NOMBRE_IMAGEN_D)
    print(f"Imagen D guardada en: {ruta_imagen_d}")

    # Graficar todas las imágenes generadas
    lista_imagenes = [
        imagen_a,
        imagen_c,
        imagen_d_operativa,
        imagen_d,
    ]
    lista_titulos = [
        "Imagen A",
        "Imagen C",
        "XOR final",
        "Imagen D",
    ]

    graficar_imagenes(
        lista_imagenes,
        lista_titulos,
        prefijo=PREFIJO,
        filas=1,
        columnas=4,
        titulo_general="Punto 4: Células no agujereadas (Tipo 1)",
    )


if __name__ == "__main__":
    main()