# -*- coding: utf-8 -*-
"""Punto 3: Generación de la imagen C.

Enunciado:
    ¿Cómo, de forma automática, a partir de la imagen B, usando
    SOLAMENTE el proceso de reconstrucción, las operaciones lógicas
    (AND, OR, XOR, NAND, NOR) y la inversión de imagen, generar la
    imagen C de todas las células agujereadas (con citoplasma) de
    Tipo 2, Tipo 3 y Tipo 4?

Pasos realizados:
    1. Se cargan las imágenes A y B generadas por los puntos 1 y 2
       (originales y en polaridad operativa).
    2. Se rellenan los agujeros de la imagen A (misma técnica del
       punto 2), obteniendo imagen_rellena.
    3. Se reconstruye usando la imagen B como marcador contra
       imagen_rellena como máscara — acá sí el marcador es
       subconjunto estricto de la máscara, como exige la
       reconstrucción morfológica, ya que donde B tiene el agujero
       marcado, la imagen rellena también vale 255. El resultado es
       la silueta completa de cada célula agujereada, rellena.
    4. Se hace AND contra la imagen A original para reabrir el
       agujero real (operación lógica, sin restricción de
       subconjunto).
    5. Se invierte el resultado para volver a la polaridad visual:
       imagen C.
"""

# Importar funciones auxiliares
from util import NOMBRE_IMAGEN_A
from util import NOMBRE_IMAGEN_B
from util import NOMBRE_IMAGEN_C
from util import cargar_imagen_resultado
from util import guardar_imagen
from util import invertir_imagen
from util import operacion_and
from util import reconstruccion_morfologica
from util import rellenar_agujeros
from util import graficar_imagenes


def obtener_imagenes_previas():
    """Obtiene las imágenes A y B generadas por los puntos anteriores.

    Carga "imagen_a.png" e "imagen_b.png" directamente en polaridad
    operativa (invertir=True, el valor por defecto), que es la única
    que necesita este punto: ni A ni B se usan en su polaridad visual
    en ningún paso del cómputo.

    Returns:
        tuple: Tupla (imagen_a, imagen_b), ambas numpy.ndarray (0/255),
        en polaridad operativa (células y agujeros, respectivamente,
        en 255).
    """
    imagen_a = cargar_imagen_resultado(NOMBRE_IMAGEN_A)
    imagen_b = cargar_imagen_resultado(NOMBRE_IMAGEN_B)

    return imagen_a, imagen_b


def generar_imagen_c(imagen_a, imagen_b):
    """Genera la imagen C: células agujereadas (Tipo 2, 3 y 4) completas.

    La consulta al profesor confirmó que el marcador debe ser
    subconjunto estricto de la máscara, y que usar imagen_b
    directamente contra imagen_a no es válido (en los píxeles del
    agujero, imagen_b vale 255 e imagen_a vale 0 — son disjuntas ahí,
    no hay superposición que "ajustar" con una intersección directa).

    En cambio, se usa imagen_b como marcador contra imagen_rellena
    (la imagen A con los agujeros ya rellenados) como máscara: ahí sí
    imagen_b es subconjunto literal de imagen_rellena, porque donde
    imagen_b vale 255 (el agujero), imagen_rellena también vale 255
    (ya fue rellenado). La reconstrucción recupera así, para cada
    célula agujereada, su silueta completa rellena (sin distinguir
    todavía el agujero real). El AND final contra imagen_a "reabre"
    el agujero verdadero: es una operación lógica, no una
    reconstrucción, así que no aplica ninguna restricción de
    subconjunto en este paso.

    Las células de Tipo 1 (sin agujero) nunca son alcanzadas por el
    marcador, por lo que no aparecen en el resultado.

    Args:
        imagen_a (numpy.ndarray): Imagen A (0/255), en polaridad
            operativa (células en 255).
        imagen_b (numpy.ndarray): Imagen B (0/255), en polaridad
            operativa (agujeros en 255), usada como marcador.

    Returns:
        tuple: Tupla (imagen_c, imagen_c_operativa,
        celulas_agujereadas_rellenas, imagen_rellena).
        imagen_c es el resultado final (0/255), invertido a polaridad
        visual (fondo blanco, células negras), lista para el informe
        y para el punto 4. imagen_c_operativa es el mismo resultado
        antes de invertir, en polaridad operativa. Las otras dos son
        pasos intermedios (imagen_rellena, y las células agujereadas
        ya rellenas antes del AND final), pensadas para mostrar en el
        informe.
    """
    imagen_rellena = rellenar_agujeros(imagen_a)
    celulas_agujereadas_rellenas = reconstruccion_morfologica(imagen_b, imagen_rellena)

    imagen_c_operativa = operacion_and(celulas_agujereadas_rellenas, imagen_a)
    imagen_c = invertir_imagen(imagen_c_operativa)

    return imagen_c, imagen_c_operativa, celulas_agujereadas_rellenas, imagen_rellena


def main():
    """Función principal del programa."""

    PREFIJO = "punto3"

    # Obtener las imágenes A y B generadas por los puntos anteriores
    imagen_a, imagen_b = obtener_imagenes_previas()

    ruta_imagen_a = guardar_imagen(imagen_a, "imagen_a_operativa.png", prefijo=PREFIJO)
    print(f"Imagen A (operativa) guardada en: {ruta_imagen_a}")

    ruta_imagen_b = guardar_imagen(imagen_b, "imagen_b_operativa.png", prefijo=PREFIJO)
    print(f"Imagen B (operativa) guardada en: {ruta_imagen_b}")

    # Generar la imagen C
    imagen_c, imagen_c_operativa, celulas_agujereadas_rellenas, imagen_rellena = generar_imagen_c(imagen_a, imagen_b)

    ruta_imagen_rellena = guardar_imagen(imagen_rellena, "imagen_rellena.png", prefijo=PREFIJO)
    print(f"Imagen rellena (A sin agujeros) guardada en: {ruta_imagen_rellena}")

    ruta_celulas_rellenas = guardar_imagen(celulas_agujereadas_rellenas, "celulas_agujereadas_rellenas.png", prefijo=PREFIJO)
    print(f"Células agujereadas (rellenas) guardadas en: {ruta_celulas_rellenas}")

    ruta_imagen_c_operativa = guardar_imagen(imagen_c_operativa, "imagen_c_operativa.png", prefijo=PREFIJO)
    print(f"Imagen C (operativa) guardada en: {ruta_imagen_c_operativa}")

    ruta_imagen_c = guardar_imagen(imagen_c, NOMBRE_IMAGEN_C)
    print(f"Imagen C guardada en: {ruta_imagen_c}")

    # Graficar todas las imágenes generadas
    lista_imagenes = [
        imagen_a,
        imagen_b,
        imagen_rellena,
        celulas_agujereadas_rellenas,
        imagen_c_operativa,
        imagen_c,
    ]
    lista_titulos = [
        "Imagen A",
        "Imagen B",
        "Rellena",
        "Reconstrucción",
        "AND final",
        "Imagen C",
    ]

    graficar_imagenes(
        lista_imagenes,
        lista_titulos,
        prefijo=PREFIJO,
        filas=2,
        columnas=3,
        titulo_general="Punto 3: Células agujereadas (Tipo 2, 3 y 4)",
    )


if __name__ == "__main__":
    main()