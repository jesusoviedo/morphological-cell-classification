# -*- coding: utf-8 -*-
"""Punto 5: Generación de la imagen E.

Enunciado:
    ¿Cómo, de forma automática, a partir de la imagen C, usando
    SOLAMENTE el proceso de reconstrucción, las operaciones lógicas
    (AND, OR, XOR, NAND, NOR) y la inversión de imagen, generar la
    imagen E de todos los núcleos "sueltos" de las células de Tipo 4?

Pasos realizados:
    1. Se carga la imagen C generada por el punto 3 (original y en
       polaridad operativa).
    2. Se invierte C (complemento): el fondo exterior y los agujeros
       internos quedan en 255.
    3. Se construye el marcador de borde sobre ese complemento, y se
       reconstruye el fondo verdaderamente conectado al marco
       exterior de la imagen.
    4. Se une (OR) ese fondo exterior con la imagen C: de esta forma
       el fondo exterior queda garantizado como subconjunto de la
       nueva máscara combinada, por construcción, cumpliendo la
       condición que exige la reconstrucción morfológica (el marcador
       debe ser subconjunto de la máscara).
    5. Se reconstruye usando el fondo exterior como marcador contra
       esa máscara combinada. El crecimiento alcanza el anillo de
       cada célula (y su núcleo, si está pegado a la pared interior,
       Tipo 3), pero nunca un núcleo suelto (Tipo 4), que queda
       aislado y no conectado al resto.
    6. Se hace AND contra la imagen C, quedándose solo con la parte de
       las células ya alcanzadas (sin el fondo exterior).
    7. Se resta (XOR) ese resultado de la imagen C: como es
       subconjunto de C, el XOR deja únicamente los núcleos sueltos.
    8. Se invierte el resultado para volver a la polaridad visual:
       imagen E.
"""

# Importar funciones auxiliares
from util import NOMBRE_IMAGEN_C
from util import NOMBRE_IMAGEN_E
from util import cargar_imagen_resultado
from util import crear_marcador_borde
from util import guardar_imagen
from util import invertir_imagen
from util import operacion_and
from util import operacion_or
from util import operacion_xor
from util import reconstruccion_morfologica
from util import graficar_imagenes


def obtener_imagen_c():
    """Obtiene la imagen C generada por el punto 3.

    Carga "imagen_c.png" (el resultado canónico del punto 3) en sus
    dos polaridades: tal como quedó guardada en disco (polaridad
    visual, invertir=False), útil para mostrar en el informe de dónde
    se partió, y también invertida a polaridad operativa
    (invertir=True, el valor por defecto), que es la que necesita la
    reconstrucción y las operaciones lógicas.

    Returns:
        tuple: Tupla (imagen_c_original, imagen_c). La primera está en
        polaridad visual (tal cual se guardó); la segunda en polaridad
        operativa (células y núcleos en 255).
    """
    imagen_c_original = cargar_imagen_resultado(NOMBRE_IMAGEN_C, invertir=False)
    imagen_c = cargar_imagen_resultado(NOMBRE_IMAGEN_C)

    return imagen_c_original, imagen_c


def generar_imagen_e(imagen_c):
    """Genera la imagen E: núcleos sueltos de las células Tipo 4.

    El fondo exterior reconstruido no es, por sí solo, subconjunto de
    la imagen C (son disjuntos en los píxeles de las células, el mismo
    problema que se resolvió en el punto 3). Por eso, antes de usarlo
    como marcador, se lo une (OR) con la propia imagen C: en esa
    máscara combinada, el fondo exterior sí es subconjunto por
    construcción, y la reconstrucción resultante puede usarse sin
    violar la condición exigida por el profesor.

    Args:
        imagen_c (numpy.ndarray): Imagen C (0/255), en polaridad
            operativa (células y núcleos en 255).

    Returns:
        tuple: Tupla (imagen_e, imagen_e_operativa, cuerpos_celulares,
        reconstruccion_exterior, mascara_exterior, fondo_exterior,
        marcador_fondo, complemento_c).
        imagen_e es el resultado final (0/255), invertido a polaridad
        visual (fondo blanco, núcleos negros), lista para el informe
        y para el punto 6. imagen_e_operativa es el mismo resultado
        antes de invertir. Las demás son los pasos intermedios, en
        polaridad operativa, pensadas para mostrar en el informe.
    """
    complemento_c = invertir_imagen(imagen_c)
    marcador_fondo = crear_marcador_borde(complemento_c)
    fondo_exterior = reconstruccion_morfologica(marcador_fondo, complemento_c)

    mascara_exterior = operacion_or(fondo_exterior, imagen_c)
    reconstruccion_exterior = reconstruccion_morfologica(fondo_exterior, mascara_exterior)

    cuerpos_celulares = operacion_and(reconstruccion_exterior, imagen_c)
    imagen_e_operativa = operacion_xor(imagen_c, cuerpos_celulares)
    imagen_e = invertir_imagen(imagen_e_operativa)

    return (
        imagen_e,
        imagen_e_operativa,
        cuerpos_celulares,
        reconstruccion_exterior,
        mascara_exterior,
        fondo_exterior,
        marcador_fondo,
        complemento_c,
    )


def main():
    """Función principal del programa."""

    PREFIJO = "punto5"

    # Obtener la imagen C generada por el punto 3
    imagen_c_original, imagen_c = obtener_imagen_c()

    ruta_imagen_c_original = guardar_imagen(imagen_c_original, "imagen_c_original.png", prefijo=PREFIJO)
    print(f"Imagen C (original) guardada en: {ruta_imagen_c_original}")

    ruta_imagen_c = guardar_imagen(imagen_c, "imagen_c_operativa.png", prefijo=PREFIJO)
    print(f"Imagen C (operativa) guardada en: {ruta_imagen_c}")

    # Generar la imagen E y los pasos intermedios
    (
        imagen_e,
        imagen_e_operativa,
        cuerpos_celulares,
        reconstruccion_exterior,
        mascara_exterior,
        fondo_exterior,
        marcador_fondo,
        complemento_c,
    ) = generar_imagen_e(imagen_c)

    ruta_complemento_c = guardar_imagen(complemento_c, "complemento_c.png", prefijo=PREFIJO)
    print(f"Complemento de C guardado en: {ruta_complemento_c}")

    ruta_marcador_fondo = guardar_imagen(marcador_fondo, "marcador_fondo.png", prefijo=PREFIJO)
    print(f"Marcador del fondo guardado en: {ruta_marcador_fondo}")

    ruta_fondo_exterior = guardar_imagen(fondo_exterior, "fondo_exterior.png", prefijo=PREFIJO)
    print(f"Fondo exterior reconstruido guardado en: {ruta_fondo_exterior}")

    ruta_mascara_exterior = guardar_imagen(mascara_exterior, "mascara_exterior.png", prefijo=PREFIJO)
    print(f"Máscara exterior (OR) guardada en: {ruta_mascara_exterior}")

    ruta_reconstruccion_exterior = guardar_imagen(reconstruccion_exterior, "reconstruccion_exterior.png", prefijo=PREFIJO)
    print(f"Reconstrucción desde el exterior guardada en: {ruta_reconstruccion_exterior}")

    ruta_cuerpos_celulares = guardar_imagen(cuerpos_celulares, "cuerpos_celulares.png", prefijo=PREFIJO)
    print(f"Cuerpos celulares guardados en: {ruta_cuerpos_celulares}")

    ruta_imagen_e_operativa = guardar_imagen(imagen_e_operativa, "imagen_e_operativa.png", prefijo=PREFIJO)
    print(f"Imagen E (operativa) guardada en: {ruta_imagen_e_operativa}")

    ruta_imagen_e = guardar_imagen(imagen_e, NOMBRE_IMAGEN_E)
    print(f"Imagen E guardada en: {ruta_imagen_e}")

    # Graficar todas las imágenes generadas
    lista_imagenes = [
        imagen_c_original,
        imagen_c,
        complemento_c,
        marcador_fondo,
        fondo_exterior,
        mascara_exterior,
        reconstruccion_exterior,
        cuerpos_celulares,
        imagen_e_operativa,
        imagen_e,
    ]
    lista_titulos = [
        "Imagen C (original)",
        "Imagen C (operativa, invertida)",
        "Complemento de C",
        "Marcador (borde del complemento)",
        "Fondo exterior reconstruido",
        "OR(Fondo exterior, Imagen C)",
        "Reconstrucción(Marcador=Fondo, Máscara=OR)",
        "AND(Reconstrucción, Imagen C)",
        "XOR(Imagen C, Cuerpos celulares)",
        "Imagen E (resultado, invertida)",
    ]

    graficar_imagenes(
        lista_imagenes,
        lista_titulos,
        prefijo=PREFIJO,
        filas=2,
        columnas=5,
        titulo_general="Punto 5: Núcleos sueltos de las células Tipo 4",
    )


if __name__ == "__main__":
    main()