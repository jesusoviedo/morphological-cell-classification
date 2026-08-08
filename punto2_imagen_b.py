# -*- coding: utf-8 -*-
"""Punto 2: Generación de la imagen B.

Enunciado:
    ¿Cómo, de forma automática, a partir de la imagen A, usando
    SOLAMENTE el proceso de reconstrucción, las operaciones lógicas
    (AND, OR, XOR, NAND, NOR) y la inversión de imagen, generar la
    imagen B de todos los agujeros de las células agujereadas (con
    citoplasma)?

Pasos realizados:
    1. Se carga la imagen A tal como se guardó (polaridad visual, que
       coincide matemáticamente con el complemento de su polaridad
       operativa).
    2. Se construye el marcador de borde sobre esa misma imagen, que
       ya cumple el rol de complemento.
    3. Se reconstruye el fondo verdaderamente conectado al marco
       exterior de la imagen.
    4. Se invierte ese fondo reconstruido: se obtiene la imagen A con
       los agujeros ya rellenados.
    5. Se resta (XOR) la imagen A original (en polaridad operativa) de
       la rellenada, quedando únicamente los agujeros.
    6. Se invierte el resultado para volver a la polaridad visual:
       imagen B.
"""

# Importar constantes y funciones auxiliares
from util import NOMBRE_IMAGEN_A
from util import NOMBRE_IMAGEN_B
from util import OPERACION_XOR
from util import cargar_imagen_resultado
from util import operacion_logica
from util import guardar_imagen
from util import invertir_imagen
from util import reconstruccion_morfologica
from util import crear_marcador_borde
from util import graficar_imagenes


def generar_imagen_b(imagen_a):
    """Genera la imagen B: agujeros de las células con citoplasma.

    Aplica la técnica de relleno de agujeros (ver Conceptos previos)
    para obtener la imagen rellena, y resta (XOR) la imagen A original
    para quedarse solo con los agujeros (ver los pasos marcados en el
    código). Las células Tipo 1 nunca aportan píxeles al resultado, al
    no tener agujero.

    Args:
        imagen_a (numpy.ndarray): Imagen A (0/255), en polaridad
            visual (células en 0), tal como se guardó en el punto 1.

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
    # Paso 2: construir el marcador de borde sobre imagen_a
    imagen_marcador_relleno = crear_marcador_borde(imagen_a)
    # Paso 3: reconstruir el fondo conectado al marco exterior
    imagen_reconstruida_fondo = reconstruccion_morfologica(
        imagen_marcador_relleno, imagen_a
    )
    # Paso 4: invertir para obtener la imagen con agujeros rellenados
    imagen_rellena = invertir_imagen(imagen_reconstruida_fondo)

    # imagen_a llega en polaridad visual; para el XOR final se necesita
    # en polaridad operativa (células en 255), igual que imagen_rellena.
    imagen_a_operativa = invertir_imagen(imagen_a)
    # Paso 5: restar (XOR) la imagen A original de la rellenada
    imagen_agujeros_operativa = operacion_logica(imagen_rellena, imagen_a_operativa, OPERACION_XOR)

    # Paso 6: invertir a polaridad visual
    imagen_b = invertir_imagen(imagen_agujeros_operativa)

    return imagen_b, imagen_agujeros_operativa, imagen_rellena, imagen_reconstruida_fondo, imagen_marcador_relleno, imagen_a_operativa


def main():
    """Función principal del programa."""

    PREFIJO = "punto2"

    # Paso 1: obtener la imagen A generada por el punto 1
    imagen_a = cargar_imagen_resultado(NOMBRE_IMAGEN_A, invertir=False)

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
        "Imagen A",
        "Marcador",
        "Reconstrucción",
        "Rellena",
        "Imagen A (operativa)",
        "XOR",
        "Imagen B",
    ]

    graficar_imagenes(
        lista_imagenes,
        lista_titulos,
        prefijo=PREFIJO,
        filas=2,
        columnas=4,
        titulo_general="Punto 2: Agujeros de las células con citoplasma")


if __name__ == "__main__":
    main()