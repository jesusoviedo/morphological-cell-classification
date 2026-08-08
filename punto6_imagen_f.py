# -*- coding: utf-8 -*-
"""Punto 6: Generación de la imagen F.

Enunciado:
    ¿Cómo, de forma automática, a partir de la imagen E, usando el
    proceso de reconstrucción, las operaciones lógicas (AND, OR, XOR,
    NAND, NOR), la inversión de imagen y la dilatación y erosión
    tradicionales (no condicionales), generar la imagen F de todas las
    células de Tipo 4?

Pasos realizados:
    1. Se cargan las imágenes B, C y E generadas por los puntos 2, 3
       y 5, directamente en polaridad operativa.
    2. Se une (OR) B con C: como B es el hueco real (que separaba el
       núcleo suelto del anillo) y C es la célula agujereada completa
       (anillo + núcleo), la unión rellena exactamente ese hueco,
       reconectando núcleo y anillo en una sola región continua.
    3. Se reconstruye usando E (los núcleos sueltos) como marcador
       contra esa unión como máscara. Como E es subconjunto de C (y
       por lo tanto de OR(B, C)), se cumple la condición de
       subconjunto que exige la reconstrucción morfológica. El crecimiento alcanza
       únicamente las células Tipo 4 (las que tienen un núcleo suelto
       que sirve de semilla); las Tipo 3 no tienen semilla en E, así
       que no se reconstruyen.
    4. Se hace AND contra la imagen C, reabriendo el hueco real de
       cada célula Tipo 4 recuperada (la unión del paso 2 lo había
       tapado).
    5. Se invierte el resultado para volver a la polaridad visual:
       imagen F.

    No hizo falta usar dilatación ni erosión tradicionales para este
    punto: el enunciado las permite, pero no las exige (mismo
    criterio ya aplicado en los puntos 4 y 7), y el truco de unir B
    con C antes de reconstruir logra el mismo efecto (reconectar el
    núcleo suelto con el anillo) sin necesidad de dilatar nada.
"""

# Importar constantes y funciones auxiliares
from util import NOMBRE_IMAGEN_B
from util import NOMBRE_IMAGEN_C
from util import NOMBRE_IMAGEN_E
from util import NOMBRE_IMAGEN_F
from util import OPERACION_AND
from util import OPERACION_OR
from util import cargar_imagen_resultado
from util import guardar_imagen
from util import invertir_imagen
from util import operacion_logica
from util import reconstruccion_morfologica
from util import graficar_imagenes


def generar_imagen_f(imagen_b, imagen_c, imagen_e):
    """Genera la imagen F: células Tipo 4 completas.

    El núcleo suelto (E) está desconectado del anillo dentro de C; se
    une (OR) B con C para reconectarlos antes de reconstruir, sin
    necesidad de dilatar nada (ver los pasos marcados en el código).
    E es subconjunto de OR(B, C), cumpliendo la condición que exige la
    reconstrucción. Solo las células Tipo 4 tienen semilla en E, así
    que son las únicas alcanzadas.

    Args:
        imagen_b (numpy.ndarray): Imagen B (0/255), en polaridad
            operativa (agujeros en 255).
        imagen_c (numpy.ndarray): Imagen C (0/255), en polaridad
            operativa (células agujereadas en 255).
        imagen_e (numpy.ndarray): Imagen E (0/255), en polaridad
            operativa (núcleos sueltos en 255), usada como marcador.

    Returns:
        tuple: Tupla (imagen_f, imagen_f_operativa,
        imagen_reconstruida, imagen_or).
        imagen_f es el resultado final (0/255), invertido a polaridad
        visual (fondo blanco, células negras), lista para el informe.
        imagen_f_operativa es el mismo resultado antes de invertir.
        Las otras dos son pasos intermedios, en polaridad operativa,
        pensadas para mostrar en el informe.
    """
    # Paso 2: unir (OR) B con C, reconectando núcleo y anillo
    imagen_or = operacion_logica(imagen_b, imagen_c, OPERACION_OR)
    # Paso 3: reconstruir usando E como marcador contra esa unión
    imagen_reconstruida = reconstruccion_morfologica(imagen_e, imagen_or)

    # Paso 4: AND contra la imagen C, reabriendo el hueco real
    imagen_f_operativa = operacion_logica(imagen_reconstruida, imagen_c, OPERACION_AND)
    # Paso 5: invertir a polaridad visual
    imagen_f = invertir_imagen(imagen_f_operativa)

    return imagen_f, imagen_f_operativa, imagen_reconstruida, imagen_or


def main():
    """Función principal del programa."""

    PREFIJO = "punto6"

    # Paso 1: obtener las imágenes B, C y E generadas por los puntos anteriores
    imagen_b = cargar_imagen_resultado(NOMBRE_IMAGEN_B)
    imagen_c = cargar_imagen_resultado(NOMBRE_IMAGEN_C)
    imagen_e = cargar_imagen_resultado(NOMBRE_IMAGEN_E)

    ruta_imagen_b = guardar_imagen(imagen_b, "imagen_b_operativa.png", prefijo=PREFIJO)
    print(f"Imagen B (operativa) guardada en: {ruta_imagen_b}")

    ruta_imagen_c = guardar_imagen(imagen_c, "imagen_c_operativa.png", prefijo=PREFIJO)
    print(f"Imagen C (operativa) guardada en: {ruta_imagen_c}")

    ruta_imagen_e = guardar_imagen(imagen_e, "imagen_e_operativa.png", prefijo=PREFIJO)
    print(f"Imagen E (operativa) guardada en: {ruta_imagen_e}")

    # Generar la imagen F y los pasos intermedios
    imagen_f, imagen_f_operativa, imagen_reconstruida, imagen_or = generar_imagen_f(
        imagen_b, imagen_c, imagen_e
    )

    ruta_imagen_or = guardar_imagen(imagen_or, "imagen_or_b_c.png", prefijo=PREFIJO)
    print(f"OR(B, C) guardado en: {ruta_imagen_or}")

    ruta_imagen_reconstruida = guardar_imagen(imagen_reconstruida, "imagen_reconstruida.png", prefijo=PREFIJO)
    print(f"Reconstrucción guardada en: {ruta_imagen_reconstruida}")

    ruta_imagen_f_operativa = guardar_imagen(imagen_f_operativa, "imagen_f_operativa.png", prefijo=PREFIJO)
    print(f"Imagen F (operativa) guardada en: {ruta_imagen_f_operativa}")

    ruta_imagen_f = guardar_imagen(imagen_f, NOMBRE_IMAGEN_F)
    print(f"Imagen F guardada en: {ruta_imagen_f}")

    # Graficar todas las imágenes generadas
    lista_imagenes = [
        imagen_b,
        imagen_c,
        imagen_e,
        imagen_or,
        imagen_reconstruida,
        imagen_f_operativa,
        imagen_f,
    ]
    lista_titulos = [
        "Imagen B",
        "Imagen C",
        "Imagen E",
        "OR(B, C)",
        "Reconstrucción",
        "AND final",
        "Imagen F",
    ]

    graficar_imagenes(
        lista_imagenes,
        lista_titulos,
        prefijo=PREFIJO,
        filas=2,
        columnas=4,
        titulo_general="Punto 6: Células Tipo 4 completas",
    )


if __name__ == "__main__":
    main()