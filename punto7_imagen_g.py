# -*- coding: utf-8 -*-
"""Punto 7: Generación de la imagen G.

Enunciado:
    ¿Cómo, de forma automática, a partir de las imágenes A, D y F,
    usando las operaciones lógicas (AND, OR, XOR, NAND, NOR), generar
    la imagen G de todas las células de Tipo 2 y Tipo 3?

Pasos realizados:
    1. Se cargan las imágenes A, D y F, directamente en polaridad
       operativa.
    2. Se resta (XOR) la imagen D de la imagen A: como D (Tipo 1) es
       siempre subconjunto de A, el XOR se comporta como una resta de
       conjuntos, dejando todas las células agujereadas (Tipo 2, 3 y
       4) — el mismo resultado que la imagen C, sin necesidad de
       cargarla.
    3. Se resta (XOR) la imagen F de ese resultado: como F (Tipo 4
       completa) es siempre subconjunto de las células agujereadas,
       el XOR vuelve a comportarse como una resta de conjuntos,
       dejando únicamente las células Tipo 2 y Tipo 3.
    4. Se invierte el resultado para volver a la polaridad visual,
       usando NAND(X, X) en vez de una inversión directa: como
       AND(X, X) es siempre X, NAND(X, X) = NOT(AND(X, X)) = NOT(X).
       Con esto, todo el punto queda resuelto exclusivamente con
       operaciones lógicas (XOR y NAND), tal como lo exige el
       enunciado, sin necesitar la inversión de imagen, que no
       aparece en la lista de herramientas permitidas para este punto
       en particular (a diferencia de los demás puntos).
"""

# Importar constantes y funciones auxiliares
from util import NOMBRE_IMAGEN_A
from util import NOMBRE_IMAGEN_D
from util import NOMBRE_IMAGEN_F
from util import NOMBRE_IMAGEN_G
from util import OPERACION_NAND
from util import OPERACION_XOR
from util import cargar_imagen_resultado
from util import guardar_imagen
from util import operacion_logica
from util import graficar_imagenes


def generar_imagen_g(imagen_a, imagen_d, imagen_f):
    """Genera la imagen G: células Tipo 2 y Tipo 3.

    D es siempre subconjunto de A (toda célula Tipo 1 es una célula),
    así que XOR(A, D) se comporta como una resta de conjuntos y da
    exactamente la imagen C (células Tipo 2, 3 y 4), sin necesidad de
    cargarla aparte. F es a su vez siempre subconjunto de ese
    resultado (toda célula Tipo 4 completa es una célula agujereada),
    así que el segundo XOR también resta, dejando únicamente Tipo 2 y
    Tipo 3.

    Para volver a la polaridad visual, se usa NAND(X, X): como AND(X, X)
    es siempre X, NAND(X, X) = NOT(X) da el mismo resultado que invertir,
    pero usando exclusivamente una de las operaciones lógicas permitidas.

    Args:
        imagen_a (numpy.ndarray): Imagen A (0/255), en polaridad
            operativa (células en 255).
        imagen_d (numpy.ndarray): Imagen D (0/255), en polaridad
            operativa (células Tipo 1 en 255).
        imagen_f (numpy.ndarray): Imagen F (0/255), en polaridad
            operativa (células Tipo 4 completas en 255).

    Returns:
        tuple: Tupla (imagen_g, imagen_g_operativa, celulas_agujereadas).
        imagen_g es el resultado final (0/255), en polaridad visual
        (fondo blanco, células negras), lista para el informe.
        imagen_g_operativa es el mismo resultado antes de invertir.
        celulas_agujereadas es el paso intermedio (equivalente a la
        imagen C), pensado para mostrar en el informe.
    """
    celulas_agujereadas = operacion_logica(imagen_a, imagen_d, OPERACION_XOR)
    imagen_g_operativa = operacion_logica(celulas_agujereadas, imagen_f, OPERACION_XOR)
    imagen_g = operacion_logica(imagen_g_operativa, imagen_g_operativa, OPERACION_NAND)

    return imagen_g, imagen_g_operativa, celulas_agujereadas


def main():
    """Función principal del programa."""

    PREFIJO = "punto7"

    # Obtener las imágenes A, D y F generadas por los puntos anteriores
    imagen_a = cargar_imagen_resultado(NOMBRE_IMAGEN_A)
    imagen_d = cargar_imagen_resultado(NOMBRE_IMAGEN_D)
    imagen_f = cargar_imagen_resultado(NOMBRE_IMAGEN_F)

    ruta_imagen_a = guardar_imagen(imagen_a, "imagen_a_operativa.png", prefijo=PREFIJO)
    print(f"Imagen A (operativa) guardada en: {ruta_imagen_a}")

    ruta_imagen_d = guardar_imagen(imagen_d, "imagen_d_operativa.png", prefijo=PREFIJO)
    print(f"Imagen D (operativa) guardada en: {ruta_imagen_d}")

    ruta_imagen_f = guardar_imagen(imagen_f, "imagen_f_operativa.png", prefijo=PREFIJO)
    print(f"Imagen F (operativa) guardada en: {ruta_imagen_f}")

    # Generar la imagen G y los pasos intermedios
    imagen_g, imagen_g_operativa, celulas_agujereadas = generar_imagen_g(
        imagen_a, imagen_d, imagen_f
    )

    ruta_celulas_agujereadas = guardar_imagen(celulas_agujereadas, "celulas_agujereadas.png", prefijo=PREFIJO)
    print(f"Células agujereadas (= imagen C) guardadas en: {ruta_celulas_agujereadas}")

    ruta_imagen_g_operativa = guardar_imagen(imagen_g_operativa, "imagen_g_operativa.png", prefijo=PREFIJO)
    print(f"Imagen G (operativa) guardada en: {ruta_imagen_g_operativa}")

    ruta_imagen_g = guardar_imagen(imagen_g, NOMBRE_IMAGEN_G)
    print(f"Imagen G guardada en: {ruta_imagen_g}")

    # Graficar todas las imágenes generadas
    lista_imagenes = [
        imagen_a,
        imagen_d,
        imagen_f,
        celulas_agujereadas,
        imagen_g_operativa,
        imagen_g,
    ]
    lista_titulos = [
        "Imagen A",
        "Imagen D",
        "Imagen F",
        "XOR(A, D)",
        "XOR final",
        "Imagen G",
    ]

    graficar_imagenes(
        lista_imagenes,
        lista_titulos,
        prefijo=PREFIJO,
        filas=2,
        columnas=3,
        titulo_general="Punto 7: Células Tipo 2 y Tipo 3",
    )


if __name__ == "__main__":
    main()