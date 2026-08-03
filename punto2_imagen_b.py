# -*- coding: utf-8 -*-
"""Punto 2: Generación de la imagen B.

Enunciado:
    ¿Cómo, de forma automática, a partir de la imagen A, usando
    SOLAMENTE el proceso de reconstrucción, las operaciones lógicas
    (AND, OR, XOR, NAND, NOR) y la inversión de imagen, generar la
    imagen B de todos los agujeros de las células agujereadas (con
    citoplasma)?
"""

# Importar funciones auxiliares
from util import NOMBRE_IMAGEN_A
from util import NOMBRE_IMAGEN_B
from util import cargar_imagen_resultado
from util import operacion_xor
from util import guardar_imagen
from util import invertir_imagen
from util import reconstruccion_morfologica
from util import crear_marcador_borde
from util import graficar_imagenes


def obtener_imagen_a():
    """Obtiene la imagen A generada por el punto 1.

    Carga "imagen_a.png" (el resultado canónico del punto 1) tal como
    quedó guardada en disco, es decir, en polaridad visual (fondo
    blanco, células negras). Esta misma imagen sirve tanto para
    mostrarla en el informe como para usarse directamente como el
    complemento de la imagen A en polaridad operativa, ya que ambas
    coinciden matemáticamente (ver generar_imagen_b).

    Returns:
        numpy.ndarray: Imagen A (0/255), en polaridad visual.
    """
    imagen_a = cargar_imagen_resultado(NOMBRE_IMAGEN_A, invertir=False)

    return imagen_a


def generar_imagen_b(imagen_a):
    """Genera la imagen B: agujeros de las células con citoplasma.

    Aplica la técnica de relleno de agujeros vista en clase. Como
    imagen_a llega en polaridad visual (que coincide matemáticamente
    con el complemento de la imagen A en polaridad operativa), se usa
    directamente como máscara para reconstruir el fondo conectado al
    borde: se construye un marcador restringido al marco exterior de
    esa misma imagen, y se reconstruye a partir de él (lo que recupera
    únicamente el fondo verdaderamente conectado al borde, dejando
    afuera los agujeros internos, que no lo tocan). Se invierte el
    resultado para obtener la imagen con los agujeros rellenados
    (polaridad operativa). Para el XOR final, se necesita imagen_a en
    esa misma polaridad operativa, así que se invierte una única vez
    antes de restarla de la imagen rellena (válido porque la imagen
    rellenada es siempre un superconjunto de la imagen A). Por último,
    se invierte el resultado para dejar imagen_b en polaridad visual,
    lista para el informe y para encadenar con el punto 3.

    Las células de Tipo 1 (sin citoplasma) no tienen agujero, por lo
    que nunca aportan píxeles al resultado.

    Args:
        imagen_a (numpy.ndarray): Imagen A (0/255), en polaridad
            visual (células en 0), tal como la devuelve
            obtener_imagen_a().

    Returns:
        tuple: Tupla (imagen_b, imagen_agujeros_operativa,
        imagen_rellena, imagen_reconstruida_fondo,
        imagen_marcador_relleno, imagen_a_operativa).
        imagen_b es el resultado final (0/255), en polaridad visual
        (fondo blanco, agujeros negros), lista para el informe y para
        el punto 3. imagen_a_operativa es imagen_a invertida a
        polaridad operativa (células en 255), devuelta para poder
        mostrar en el informe los dos operandos del XOR final. Las
        demás son los pasos intermedios, en polaridad operativa,
        pensadas para mostrar en el informe.
    """
    imagen_marcador_relleno = crear_marcador_borde(imagen_a)
    imagen_reconstruida_fondo = reconstruccion_morfologica(
        imagen_marcador_relleno, imagen_a
    )
    imagen_rellena = invertir_imagen(imagen_reconstruida_fondo)

    # imagen_a llega en polaridad visual; para el XOR final se necesita
    # en polaridad operativa (células en 255), igual que imagen_rellena.
    imagen_a_operativa = invertir_imagen(imagen_a)
    imagen_agujeros_operativa = operacion_xor(imagen_rellena, imagen_a_operativa)

    imagen_b = invertir_imagen(imagen_agujeros_operativa)

    return imagen_b, imagen_agujeros_operativa, imagen_rellena, imagen_reconstruida_fondo, imagen_marcador_relleno, imagen_a_operativa


def main():
    """Función principal del programa."""

    PREFIJO = "punto2"

    # Obtener la imagen A generada por el punto 1
    imagen_a = obtener_imagen_a()

    ruta_imagen_a_entrada = guardar_imagen(imagen_a, "imagen_a_entrada.png", prefijo=PREFIJO)
    print(f"Imagen A de entrada guardada en: {ruta_imagen_a_entrada}")

    # Generar la imagen B y los pasos intermedios
    imagen_b, imagen_agujeros_operativa, imagen_rellena, imagen_reconstruida_fondo, imagen_marcador_relleno, imagen_a_operativa = generar_imagen_b(imagen_a)

    ruta_imagen_marcador_relleno = guardar_imagen(imagen_marcador_relleno, "imagen_marcador_relleno.png", prefijo=PREFIJO)
    print(f"Imagen marcador de relleno guardada en: {ruta_imagen_marcador_relleno}")

    ruta_imagen_reconstruida_fondo = guardar_imagen(imagen_reconstruida_fondo, "imagen_reconstruida_fondo.png", prefijo=PREFIJO)
    print(f"Imagen reconstruida (fondo) guardada en: {ruta_imagen_reconstruida_fondo}")

    ruta_imagen_rellena = guardar_imagen(imagen_rellena, "imagen_rellena.png", prefijo=PREFIJO)
    print(f"Imagen rellena guardada en: {ruta_imagen_rellena}")

    ruta_imagen_a_operativa = guardar_imagen(imagen_a_operativa, "imagen_a_operativa.png", prefijo=PREFIJO)
    print(f"Imagen A (operativa) guardada en: {ruta_imagen_a_operativa}")

    ruta_imagen_agujeros_operativa = guardar_imagen(imagen_agujeros_operativa, "imagen_agujeros_operativa.png", prefijo=PREFIJO)
    print(f"Imagen agujeros (operativa) guardada en: {ruta_imagen_agujeros_operativa}")

    ruta_imagen_b = guardar_imagen(imagen_b, NOMBRE_IMAGEN_B)
    print(f"Imagen B guardada en: {ruta_imagen_b}")

    lista_imagenes = [
        imagen_a,
        imagen_marcador_relleno,
        imagen_reconstruida_fondo,
        imagen_rellena,
        imagen_a_operativa,
        imagen_agujeros_operativa,
        imagen_b,
    ]
    lista_titulos = [
        "Imagen A (entrada / máscara)",
        "Marcador (borde de la máscara)",
        "Reconstrucción(Marcador, Máscara)",
        "Imagen rellena (Reconstrucción invertida)",
        "Imagen A (operativa, invertida)",
        "XOR(Imagen rellena, Imagen A operativa)",
        "Imagen B (resultado, invertida)",
    ]

    graficar_imagenes(
        lista_imagenes,
        lista_titulos,
        prefijo=PREFIJO,
        filas=3,
        columnas=3,
        titulo_general="Punto 2: Agujeros de las células con citoplasma")


if __name__ == "__main__":
    main()