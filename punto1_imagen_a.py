# -*- coding: utf-8 -*-
"""Punto 1: Generación de la imagen A.

Enunciado:
    ¿Cómo, de forma automática, usando SOLAMENTE el proceso de
    reconstrucción, las operaciones lógicas (AND, OR, XOR, NAND, NOR) y
    la inversión de imagen, generar la imagen A sin pedazos ni células
    truncadas en los bordes de la imagen?
"""

# Importar funciones auxiliares
from util import NOMBRE_IMAGEN
from util import NOMBRE_IMAGEN_A
from util import descargar_imagen
from util import cargar_imagen_binaria
from util import operacion_and
from util import operacion_xor
from util import guardar_imagen
from util import invertir_imagen
from util import reconstruccion_morfologica
from util import crear_marcador_borde
from util import graficar_imagenes


def obtener_imagen_base():
    """Obtiene la imagen base del trabajo en sus dos polaridades.

    Descarga la imagen base si todavía no existe localmente (la
    verificación la hace internamente descargar_imagen), y luego la
    carga en escala de grises, generando dos versiones binarizadas:

    - imagen_original: mantiene la polaridad original de la imagen de
      entrada (fondo blanco, células negras), sin invertir. Es la que
      se usa para mostrar en el informe.
    - imagen_mascara: invertida (células en 255, fondo en 0), lista
      para usarse como máscara en las operaciones lógicas y la
      reconstrucción morfológica del resto del pipeline.

    Returns:
        tuple: Tupla (imagen_original, imagen_mascara), ambas
        numpy.ndarray (0/255).
    """
    print(f"Descargando imagen {NOMBRE_IMAGEN}...")
    ruta_imagen = descargar_imagen()

    imagen_original = cargar_imagen_binaria(ruta_imagen, invertir_automatico=False)
    imagen_mascara = cargar_imagen_binaria(ruta_imagen)
    
    print(f"Imagen {NOMBRE_IMAGEN} descargada en: {ruta_imagen}")

    return imagen_original, imagen_mascara


def generar_imagen_a(imagen_mascara, imagen_marcador):
    """Genera la imagen A: células sin truncar en los bordes.
 
    Reconstruye a partir del marcador de borde los objetos que tocan
    el borde de la imagen, y los elimina de la máscara mediante XOR
    (válido porque la reconstrucción es siempre un subconjunto de la
    máscara). El resultado se invierte antes de devolverlo, para que
    imagen_a quede en la misma polaridad original que imagen_original
    (fondo blanco, células negras), lista para el informe.
 
    Args:
        imagen_mascara (numpy.ndarray): Imagen binaria (0/255), en
            polaridad invertida (células en 255), con todas las
            células, usada como máscara de la reconstrucción.
        imagen_marcador (numpy.ndarray): Marcador de borde (0/255), en
            la misma polaridad invertida.
 
    Returns:
        tuple: Tupla (imagen_a, imagen_con_operacion_xor,
        image_con_objeto_borde).
        imagen_a (numpy.ndarray) es la imagen A final (0/255), ya
        invertida a la polaridad original (fondo blanco, células
        negras). imagen_con_operacion_xor (numpy.ndarray) es el
        resultado del XOR, todavía en polaridad invertida (operativa),
        antes de la inversión final. image_con_objeto_borde
        (numpy.ndarray) es la reconstrucción de los objetos que tocan
        el borde, también en polaridad invertida. Estas dos últimas se
        devuelven para poder mostrar los pasos intermedios en el
        informe.
    """

    image_con_objeto_borde = reconstruccion_morfologica(imagen_marcador, imagen_mascara)
    imagen_con_operacion_xor = operacion_xor(imagen_mascara, image_con_objeto_borde)
    imagen_a = invertir_imagen(imagen_con_operacion_xor)
    return imagen_a, imagen_con_operacion_xor, image_con_objeto_borde


def main():
    """Función principal del programa."""

    PREFIJO = "punto1"

    # Obtener la imagen original y la máscara
    imagen_original, imagen_mascara = obtener_imagen_base()

    ruta_imagen_original = guardar_imagen(imagen_original, "imagen_original.png", prefijo=PREFIJO)
    print(f"Imagen original guardada en: {ruta_imagen_original}")

    ruta_imagen_mascara = guardar_imagen(imagen_mascara, "imagen_mascara.png", prefijo=PREFIJO)
    print(f"Imagen máscara guardada en: {ruta_imagen_mascara}")

    # Crear el marcador de borde a partir de la imagen máscara
    imagen_marcador = crear_marcador_borde(imagen_mascara)

    ruta_imagen_marcador = guardar_imagen(imagen_marcador, "imagen_marcador.png", prefijo=PREFIJO)
    print(f"Imagen marcador guardada en: {ruta_imagen_marcador}")

    # Generar la imagen A y la imagen con objetos de borde
    imagen_a, imagen_con_operacion_xor, image_con_objeto_borde = generar_imagen_a(imagen_mascara, imagen_marcador)

    ruta_image_con_objeto_borde = guardar_imagen(image_con_objeto_borde, "image_con_objeto_borde.png", prefijo=PREFIJO)
    print(f"Imagen con objetos de borde guardada en: {ruta_image_con_objeto_borde}")

    ruta_imagen_con_operacion_xor = guardar_imagen(imagen_con_operacion_xor, "imagen_con_operacion_xor.png", prefijo=PREFIJO)
    print(f"Imagen con operación XOR guardada en: {ruta_imagen_con_operacion_xor}")

    ruta_imagen_a = guardar_imagen(imagen_a, NOMBRE_IMAGEN_A)
    print(f"Imagen A guardada en: {ruta_imagen_a}")

    # Graficar todas las imágenes generadas
    lista_imagenes = [
        imagen_original, 
        imagen_mascara, 
        imagen_marcador, 
        image_con_objeto_borde,
        imagen_con_operacion_xor, 
        imagen_a]
    lista_titulos = [
        "Imagen Original (entrada)",
        "Máscara (operativa, invertida)",
        "Marcador (borde de la máscara)",
        "Reconstrucción(Marcador, Máscara)",
        "XOR(Máscara, Reconstrucción)",
        "Imagen A (resultado, invertida)",
    ]

    graficar_imagenes(lista_imagenes, 
                      lista_titulos, 
                      prefijo=PREFIJO, 
                      filas=2, 
                      columnas=3, 
                      titulo_general="Punto 1: Células sin sin pedazos ni células truncadas en los bordes")


if __name__ == "__main__":
    main()