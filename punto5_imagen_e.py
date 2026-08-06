# -*- coding: utf-8 -*-
"""Punto 5: Generación de la imagen E.

Enunciado:
    ¿Cómo, de forma automática, a partir de la imagen C, usando
    SOLAMENTE el proceso de reconstrucción, las operaciones lógicas
    (AND, OR, XOR, NAND, NOR) y la inversión de imagen, generar la
    imagen E de todos los núcleos "sueltos" de las células de Tipo 4?

Pasos realizados:
    1. Se cargan las imágenes B y C generadas por los puntos 2 y 3.
    2. Se obtiene la máscara exterior directamente como el complemento
       de B (invertir_imagen(imagen_b)): la imagen rellena (fondo
       exterior unido con C) es exactamente igual al complemento de
       B, por la ley de De Morgan (ver docstring de generar_imagen_e).
    3. Se construye el marcador como el marco exterior de esa máscara
       (mismo patrón visual que crear_marcador_borde usa en los
       puntos 1 y 2: blanco solo en el borde, negro en todo el
       resto). No hace falta que el marcador ya tenga la forma
       completa del fondo real — alcanza con que toque esa región
       conectada, y la reconstrucción se encarga de expandirlo.
    4. Se reconstruye usando ese marcador de marco contra la máscara
       exterior. El crecimiento alcanza el anillo de cada célula (y
       su núcleo, si está pegado a la pared interior, Tipo 3), pero
       nunca un núcleo suelto (Tipo 4), que queda aislado y no
       conectado al resto.
    5. Se hace AND contra la imagen C, quedándose solo con la parte de
       las células ya alcanzadas (sin el fondo exterior).
    6. Se resta (XOR) ese resultado de la imagen C: como es
       subconjunto de C, el XOR deja únicamente los núcleos sueltos.
    7. Se invierte el resultado para volver a la polaridad visual:
       imagen E.
"""

# Importar constantes y funciones auxiliares
from util import NOMBRE_IMAGEN_B
from util import NOMBRE_IMAGEN_C
from util import NOMBRE_IMAGEN_E
from util import OPERACION_AND
from util import OPERACION_XOR
from util import cargar_imagen_resultado
from util import crear_marcador_borde
from util import guardar_imagen
from util import invertir_imagen
from util import operacion_logica
from util import reconstruccion_morfologica
from util import graficar_imagenes


def generar_imagen_e(imagen_b, imagen_c):
    """Genera la imagen E: núcleos sueltos de las células Tipo 4.

    La máscara exterior (fondo verdadero unido, por OR, con la propia
    imagen C) es exactamente igual al complemento de la imagen B. Esto
    se puede demostrar con la ley de De Morgan: llamando "hueco_real"
    a lo que representa B (las zonas encerradas, no conectadas al
    fondo verdadero) y "fondo_real" al fondo verdaderamente conectado
    al borde:

        mascara_exterior = fondo_real ∪ C
                          = complemento(complemento(fondo_real) ∩ complemento(C))
                          = complemento(hueco_real) [ya que
                            complemento(fondo_real) ∩ complemento(C)
                            es, por construcción, exactamente hueco_real]
                          = complemento(B)

    Por eso la máscara se obtiene directo con una inversión, sin
    reconstruir nada. El marcador, en cambio, se arma con el mismo
    patrón visual que crear_marcador_borde usa en los puntos 1 y 2:
    blanco solo en el marco exterior de la imagen, negro en el resto.
    No hace falta que el marcador ya cubra toda la forma del fondo
    real — alcanza con que toque esa región conectada, ya que la
    reconstrucción se encarga de expandirlo hasta ocupar el resto
    (se verificó numéricamente que da idéntico resultado que partir
    de un marcador más grande, con muchos menos píxeles de entrada).

    Args:
        imagen_b (numpy.ndarray): Imagen B (0/255), en polaridad
            operativa (agujeros en 255).
        imagen_c (numpy.ndarray): Imagen C (0/255), en polaridad
            operativa (células y núcleos en 255).

    Returns:
        tuple: Tupla (imagen_e, imagen_e_operativa, cuerpos_celulares,
        reconstruccion_exterior, mascara_exterior, marcador_borde).
        imagen_e es el resultado final (0/255), invertido a polaridad
        visual (fondo blanco, núcleos negros), lista para el informe
        y para el punto 6. imagen_e_operativa es el mismo resultado
        antes de invertir. Las demás son los pasos intermedios, en
        polaridad operativa, pensadas para mostrar en el informe.
    """
    mascara_exterior = invertir_imagen(imagen_b)
    marcador_borde = crear_marcador_borde(mascara_exterior)

    reconstruccion_exterior = reconstruccion_morfologica(marcador_borde, mascara_exterior)

    cuerpos_celulares = operacion_logica(reconstruccion_exterior, imagen_c, OPERACION_AND)
    imagen_e_operativa = operacion_logica(imagen_c, cuerpos_celulares, OPERACION_XOR)
    imagen_e = invertir_imagen(imagen_e_operativa)

    return (
        imagen_e,
        imagen_e_operativa,
        cuerpos_celulares,
        reconstruccion_exterior,
        mascara_exterior,
        marcador_borde,
    )


def main():
    """Función principal del programa."""

    PREFIJO = "punto5"

    # Obtener las imágenes B y C generadas por los puntos 2 y 3
    imagen_b = cargar_imagen_resultado(NOMBRE_IMAGEN_B)
    imagen_c = cargar_imagen_resultado(NOMBRE_IMAGEN_C)

    ruta_imagen_b = guardar_imagen(imagen_b, "imagen_b_operativa.png", prefijo=PREFIJO)
    print(f"Imagen B (operativa) guardada en: {ruta_imagen_b}")

    ruta_imagen_c = guardar_imagen(imagen_c, "imagen_c_operativa.png", prefijo=PREFIJO)
    print(f"Imagen C (operativa) guardada en: {ruta_imagen_c}")

    # Generar la imagen E y los pasos intermedios
    (
        imagen_e,
        imagen_e_operativa,
        cuerpos_celulares,
        reconstruccion_exterior,
        mascara_exterior,
        marcador_borde,
    ) = generar_imagen_e(imagen_b, imagen_c)

    ruta_marcador_borde = guardar_imagen(marcador_borde, "marcador_borde.png", prefijo=PREFIJO)
    print(f"Marcador (marco de la máscara) guardado en: {ruta_marcador_borde}")

    ruta_mascara_exterior = guardar_imagen(mascara_exterior, "mascara_exterior.png", prefijo=PREFIJO)
    print(f"Máscara exterior (= complemento de B) guardada en: {ruta_mascara_exterior}")

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
        imagen_b,
        imagen_c,
        marcador_borde,
        mascara_exterior,
        reconstruccion_exterior,
        cuerpos_celulares,
        imagen_e_operativa,
        imagen_e,
    ]
    lista_titulos = [
        "Imagen B",
        "Imagen C",
        "Marcador",
        "Máscara",
        "Reconstrucción",
        "Cuerpos celulares",
        "XOR final",
        "Imagen E",
    ]

    graficar_imagenes(
        lista_imagenes,
        lista_titulos,
        prefijo=PREFIJO,
        filas=2,
        columnas=4,
        titulo_general="Punto 5: Núcleos sueltos de las células Tipo 4",
    )


if __name__ == "__main__":
    main()