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
       subconjunto exigida por el profesor. El crecimiento alcanza
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


def obtener_imagenes_previas():
    """Obtiene las imágenes B, C y E generadas por los puntos 2, 3 y 5.

    Carga "imagen_b.png", "imagen_c.png" e "imagen_e.png" directamente
    en polaridad operativa (invertir=True, el valor por defecto), que
    es la única que necesita este punto: ninguna se usa en su
    polaridad visual en ningún paso del cómputo.

    Returns:
        tuple: Tupla (imagen_b, imagen_c, imagen_e), las tres
        numpy.ndarray (0/255), en polaridad operativa (agujeros,
        células y núcleos sueltos, respectivamente, en 255).
    """
    imagen_b = cargar_imagen_resultado(NOMBRE_IMAGEN_B)
    imagen_c = cargar_imagen_resultado(NOMBRE_IMAGEN_C)
    imagen_e = cargar_imagen_resultado(NOMBRE_IMAGEN_E)

    return imagen_b, imagen_c, imagen_e


def generar_imagen_f(imagen_b, imagen_c, imagen_e):
    """Genera la imagen F: células Tipo 4 completas.

    El núcleo suelto (imagen E) está desconectado del anillo dentro de
    la imagen C — por eso no alcanza con reconstruir directo contra C
    (el marcador nunca podría "cruzar" esa distancia). En cambio, se
    une (OR) la imagen B (el hueco real que separaba núcleo y anillo)
    con la imagen C: esa unión rellena exactamente el hueco,
    reconectando núcleo y anillo en una sola región continua, sin
    necesidad de dilatar nada.

    Como E es subconjunto de C (el núcleo es parte del material
    celular que C ya contiene) y C es a su vez subconjunto de
    OR(B, C), se cumple que E es subconjunto de la máscara usada en
    la reconstrucción, respetando la condición exigida por el
    profesor.

    La reconstrucción, al arrancar desde cada núcleo suelto, solo
    alcanza las células Tipo 4 (las únicas con una semilla en E); las
    células Tipo 3 (núcleo pegado, sin aportar a E) y Tipo 1 (sin
    agujero, ausentes de B y C) quedan afuera del resultado.

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
    imagen_or = operacion_logica(imagen_b, imagen_c, OPERACION_OR)
    imagen_reconstruida = reconstruccion_morfologica(imagen_e, imagen_or)

    imagen_f_operativa = operacion_logica(imagen_reconstruida, imagen_c, OPERACION_AND)
    imagen_f = invertir_imagen(imagen_f_operativa)

    return imagen_f, imagen_f_operativa, imagen_reconstruida, imagen_or


def main():
    """Función principal del programa."""

    PREFIJO = "punto6"

    # Obtener las imágenes B, C y E generadas por los puntos anteriores
    imagen_b, imagen_c, imagen_e = obtener_imagenes_previas()

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