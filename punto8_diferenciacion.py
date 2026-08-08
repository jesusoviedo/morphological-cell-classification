# -*- coding: utf-8 -*-
"""Punto 8: Diferenciación entre células de Tipo 2 y Tipo 3.

Enunciado:
    ¿Cómo harías para diferenciar las células de Tipo 2 y Tipo 3?

Pasos realizados:
    1. Se carga la imagen G (Tipo 2 y Tipo 3 combinadas) generada en
       el punto 7, directamente en polaridad operativa.
    2. Se erosiona G con un elemento estructurante circular de radio
       6: lo suficientemente grande como para eliminar por completo
       el anillo fino de las células Tipo 3 (incluido su núcleo,
       también más chico que el elemento), pero sin llegar a eliminar
       el cuerpo, casi sólido, de las células Tipo 2. El radio se
       midió empíricamente sobre la imagen de referencia del
       enunciado (ver docstring de generar_diferenciacion).
    3. Se reconstruye desde lo que sobrevive a la erosión contra G
       como máscara: como solo sobrevive material de las células
       Tipo 2, la reconstrucción recupera únicamente esas células
       completas.
    4. Si se pide Tipo 3, se resta (XOR) ese resultado de G: como es
       subconjunto de G, el XOR deja únicamente las células Tipo 3.
    5. Se invierte el resultado para volver a la polaridad visual.

    El criterio es de espesor, no de tamaño de agujero: en la imagen
    de referencia, las células Tipo 2 son casi sólidas (con apenas un
    agujero minúsculo), mientras que las Tipo 3 tienen un anillo fino
    con un agujero grande y un núcleo pegado a la pared — la erosión
    aprovecha esa diferencia de espesor entre ambas.
"""

# Importar constantes y funciones auxiliares
import argparse

from util import NOMBRE_IMAGEN_G
from util import FORMA_CIRCULO
from util import OPERACION_XOR
from util import cargar_imagen_resultado
from util import guardar_imagen
from util import invertir_imagen
from util import operacion_logica
from util import erosion_binaria
from util import reconstruccion_morfologica
from util import graficar_imagenes

# Constantes para el parámetro tipo_celula
TIPO_CELULA_2 = 2
TIPO_CELULA_3 = 3

# Radio del elemento estructurante circular
RADIO_EROSION = 6


def generar_diferenciacion(imagen_g, tipo_celula):
    """Separa la imagen G en Tipo 2 o Tipo 3, según el parámetro.

    Las células Tipo 2 sobreviven a la erosión; ese remanente,
    reconstruido contra G, recupera las Tipo 2 completas -- la base
    común para ambos tipos: es la respuesta directa para Tipo 2, y su
    resta (XOR) contra G da Tipo 3 (ver los pasos marcados en el
    código).

    Args:
        imagen_g (numpy.ndarray): Imagen G (0/255), en polaridad
            operativa (Tipo 2 y Tipo 3 en 255).
        tipo_celula (int): TIPO_CELULA_2 o TIPO_CELULA_3 — qué tipo
            extraer.

    Returns:
        tuple: Tupla (imagen_resultado, imagen_resultado_operativa,
        imagen_erosionada, imagen_tipo2_operativa).
        imagen_resultado es el tipo pedido (0/255), en polaridad
        visual, lista para el informe. imagen_resultado_operativa es
        el mismo resultado antes de invertir. imagen_erosionada y
        imagen_tipo2_operativa son pasos intermedios, en polaridad
        operativa, pensados para mostrar en el informe.

    Raises:
        ValueError: Si tipo_celula no es TIPO_CELULA_2 ni
            TIPO_CELULA_3.
    """
    if tipo_celula not in (TIPO_CELULA_2, TIPO_CELULA_3):
        raise ValueError(
            "tipo_celula debe ser TIPO_CELULA_2 o TIPO_CELULA_3, "
            f"se recibió: {tipo_celula!r}"
        )

    # Paso 2: erosionar G con un elemento estructurante circular
    imagen_erosionada = erosion_binaria(imagen_g, forma=FORMA_CIRCULO, radio=RADIO_EROSION)
    # Paso 3: reconstruir desde lo que sobrevive, contra G como máscara
    imagen_tipo2_operativa = reconstruccion_morfologica(imagen_erosionada, imagen_g)

    if tipo_celula == TIPO_CELULA_2:
        imagen_resultado_operativa = imagen_tipo2_operativa
    else:
        # Paso 4: si se pide Tipo 3, restar (XOR) ese resultado de G
        imagen_resultado_operativa = operacion_logica(imagen_g, imagen_tipo2_operativa, OPERACION_XOR)

    # Paso 5: invertir a polaridad visual
    imagen_resultado = invertir_imagen(imagen_resultado_operativa)

    return imagen_resultado, imagen_resultado_operativa, imagen_erosionada, imagen_tipo2_operativa


def main(tipo_celula):
    """Función principal del programa.

    Args:
        tipo_celula (int): TIPO_CELULA_2 o TIPO_CELULA_3 — qué tipo de
            célula extraer y documentar en esta corrida.
    """
    prefijo = f"punto8_tipo{tipo_celula}"

    # Paso 1: obtener la imagen G generada por el punto anterior
    imagen_g = cargar_imagen_resultado(NOMBRE_IMAGEN_G)

    ruta_imagen_g = guardar_imagen(imagen_g, "imagen_g_operativa.png", prefijo=prefijo)
    print(f"Imagen G (operativa) guardada en: {ruta_imagen_g}")

    # Generar la diferenciación y los pasos intermedios
    (
        imagen_resultado,
        imagen_resultado_operativa,
        imagen_erosionada,
        imagen_tipo2_operativa,
    ) = generar_diferenciacion(imagen_g, tipo_celula)

    ruta_erosionada = guardar_imagen(imagen_erosionada, "imagen_erosionada.png", prefijo=prefijo)
    print(f"Imagen erosionada guardada en: {ruta_erosionada}")

    ruta_tipo2 = guardar_imagen(imagen_tipo2_operativa, "reconstruccion_tipo2.png", prefijo=prefijo)
    print(f"Reconstrucción (Tipo 2) guardada en: {ruta_tipo2}")

    ruta_resultado_operativa = guardar_imagen(imagen_resultado_operativa, "imagen_resultado_operativa.png", prefijo=prefijo)
    print(f"Resultado (operativa) guardado en: {ruta_resultado_operativa}")

    ruta_resultado = guardar_imagen(imagen_resultado, f"imagen_tipo{tipo_celula}.png")
    print(f"Imagen Tipo {tipo_celula} guardada en: {ruta_resultado}")

    # Graficar: Tipo 3 necesita un paso extra (el XOR) que Tipo 2 no
    if tipo_celula == TIPO_CELULA_2:
        lista_imagenes = [imagen_g, imagen_erosionada, imagen_tipo2_operativa, imagen_resultado]
        lista_titulos = ["Imagen G", "Erosión", "Reconstrucción", "Tipo 2"]
    else:
        lista_imagenes = [imagen_g, imagen_erosionada, imagen_tipo2_operativa, imagen_resultado_operativa, imagen_resultado]
        lista_titulos = ["Imagen G", "Erosión", "Reconstrucción", "XOR", "Tipo 3"]

    graficar_imagenes(
        lista_imagenes,
        lista_titulos,
        prefijo=prefijo,
        filas=2,
        columnas=3,
        titulo_general=f"Punto 8: Diferenciación -- extrayendo Tipo {tipo_celula}",
    )


def parsear_argumentos():
    """Define y parsea los argumentos de línea de comandos.

    Returns:
        argparse.Namespace: objeto con el atributo tipo_celula, que
        vale TIPO_CELULA_2, TIPO_CELULA_3, o None si no se pasó
        --tipo_celula por línea de comandos (en cuyo caso se generan
        los dos tipos).
    """
    parser = argparse.ArgumentParser(
        description=(
            "Punto 8: diferencia las células Tipo 2 de las Tipo 3 en "
            "la imagen G (punto 7)."
        )
    )
    parser.add_argument(
        "--tipo_celula",
        type=int,
        choices=[TIPO_CELULA_2, TIPO_CELULA_3],
        default=None,
        help=(
            "Qué tipo de célula extraer: 2 para Tipo 2, 3 para "
            "Tipo 3. Si no se especifica, se generan ambos."
        ),
    )

    return parser.parse_args()


if __name__ == "__main__":
    argumentos = parsear_argumentos()

    if argumentos.tipo_celula is None:
        # Sin --tipo_celula: generar ambos tipos en una sola corrida.
        main(TIPO_CELULA_2)
        main(TIPO_CELULA_3)
    else:
        main(argumentos.tipo_celula)