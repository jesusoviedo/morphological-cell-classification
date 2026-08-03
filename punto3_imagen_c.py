# -*- coding: utf-8 -*-
"""Punto 3: Generación de la imagen C.

Enunciado:
    ¿Cómo, de forma automática, a partir de la imagen B, usando
    SOLAMENTE el proceso de reconstrucción, las operaciones lógicas
    (AND, OR, XOR, NAND, NOR) y la inversión de imagen, generar la
    imagen C de todas las células agujereadas (con citoplasma) de
    Tipo 2, Tipo 3 y Tipo 4?
"""

# Importar funciones auxiliares
from util import NOMBRE_IMAGEN_A
from util import NOMBRE_IMAGEN_B
from util import NOMBRE_IMAGEN_C
from util import cargar_imagen_resultado
from util import guardar_imagen
from util import invertir_imagen
from util import reconstruccion_morfologica
from util import graficar_imagenes


def obtener_imagenes_previas():
    """Obtiene las imágenes A y B generadas por los puntos anteriores.

    Carga "imagen_a.png" e "imagen_b.png" (los resultados canónicos de
    los puntos 1 y 2) en sus dos polaridades: tal como quedaron
    guardadas en disco (polaridad visual, invertir=False), útil para
    mostrar en el informe de dónde se partió, y también invertidas a
    polaridad operativa (invertir=True, el valor por defecto), que es
    la que necesita la reconstrucción: en imagen_a, las células quedan
    en 255; en imagen_b, los agujeros quedan en 255.

    Returns:
        tuple: Tupla (imagen_a_original, imagen_b_original, imagen_a,
        imagen_b). Las dos primeras están en polaridad visual (tal
        cual se guardaron); las dos últimas en polaridad operativa.
    """
    imagen_a_original = cargar_imagen_resultado(NOMBRE_IMAGEN_A, invertir=False)
    imagen_b_original = cargar_imagen_resultado(NOMBRE_IMAGEN_B, invertir=False)

    imagen_a = cargar_imagen_resultado(NOMBRE_IMAGEN_A)
    imagen_b = cargar_imagen_resultado(NOMBRE_IMAGEN_B)

    return imagen_a_original, imagen_b_original, imagen_a, imagen_b


def generar_imagen_c(imagen_a, imagen_b):
    """Genera la imagen C: células agujereadas (Tipo 2, 3 y 4) completas.

    Reconstruye, usando imagen_b (los agujeros) como marcador e
    imagen_a (todas las células) como máscara, las células completas
    que tienen agujero. El marcador no es subconjunto estricto de la
    máscara en sentido literal (el agujero, en imagen_b, cae
    exactamente donde imagen_a tiene fondo), pero la reconstrucción
    igual recupera el anillo completo de cada célula agujereada,
    porque agujero y anillo son vecinos directos (8-conectados): en
    la primera iteración, la dilatación del marcador alcanza el
    anillo, que sí satisface la máscara, y desde ahí el crecimiento
    continúa con normalidad hasta completar la célula.

    Las células de Tipo 1 (sin agujero) nunca son alcanzadas por el
    marcador, por lo que no aparecen en el resultado.

    Args:
        imagen_a (numpy.ndarray): Imagen A (0/255), en polaridad
            operativa (células en 255), usada como máscara.
        imagen_b (numpy.ndarray): Imagen B (0/255), en polaridad
            operativa (agujeros en 255), usada como marcador.

    Returns:
        tuple: Tupla (imagen_c, imagen_c_operativa). imagen_c es el
        resultado final (0/255), invertido a polaridad visual (fondo
        blanco, células negras), lista para el informe y para el
        punto 4. imagen_c_operativa es el resultado de la reconstrucción
        antes de invertir, en polaridad operativa, pensada para
        mostrar el paso intermedio en el informe.
    """
    imagen_c_operativa = reconstruccion_morfologica(imagen_b, imagen_a)
    imagen_c = invertir_imagen(imagen_c_operativa)

    return imagen_c, imagen_c_operativa


def main():
    """Función principal del programa."""

    PREFIJO = "punto3"

    # Obtener las imágenes A y B generadas por los puntos anteriores
    imagen_a_original, imagen_b_original, imagen_a, imagen_b = obtener_imagenes_previas()

    ruta_imagen_a_original = guardar_imagen(imagen_a_original, "imagen_a_original.png", prefijo=PREFIJO)
    print(f"Imagen A (original) guardada en: {ruta_imagen_a_original}")

    ruta_imagen_b_original = guardar_imagen(imagen_b_original, "imagen_b_original.png", prefijo=PREFIJO)
    print(f"Imagen B (original) guardada en: {ruta_imagen_b_original}")

    ruta_imagen_a = guardar_imagen(imagen_a, "imagen_a_mascara.png", prefijo=PREFIJO)
    print(f"Imagen A (máscara) guardada en: {ruta_imagen_a}")

    ruta_imagen_b = guardar_imagen(imagen_b, "imagen_b_marcador.png", prefijo=PREFIJO)
    print(f"Imagen B (marcador) guardada en: {ruta_imagen_b}")

    # Generar la imagen C
    imagen_c, imagen_c_operativa = generar_imagen_c(imagen_a, imagen_b)

    ruta_imagen_c_operativa = guardar_imagen(imagen_c_operativa, "imagen_c_operativa.png", prefijo=PREFIJO)
    print(f"Imagen C (operativa) guardada en: {ruta_imagen_c_operativa}")

    ruta_imagen_c = guardar_imagen(imagen_c, NOMBRE_IMAGEN_C)
    print(f"Imagen C guardada en: {ruta_imagen_c}")

    # Graficar todas las imágenes generadas
    lista_imagenes = [
        imagen_a_original,
        imagen_b_original,
        imagen_a,
        imagen_b,
        imagen_c_operativa,
        imagen_c,
    ]
    lista_titulos = [
        "Imagen A (original)",
        "Imagen B (original)",
        "Imagen A (máscara, operativa, invertida)",
        "Imagen B (marcador, operativa, invertida)",
        "Reconstrucción(Marcador, Máscara)",
        "Imagen C (resultado, invertida)",
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