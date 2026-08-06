# -*- coding: utf-8 -*-
"""Módulo de utilidades para el Trabajo Final de PDI.

Contiene funciones auxiliares para descargar la imagen base del trabajo
desde Google Drive y almacenarla localmente en la carpeta 'img'.
"""

import os
import requests
import cv2
import numpy as np
from scipy.ndimage import binary_dilation
import matplotlib.pyplot as plt

# Constantes para la descarga de la imagen base
ID_IMAGEN_BASE = "1zjP2KHLyJjB0iyuquUZY3tWyorw-ysU3"
NOMBRE_IMAGEN = "5ab3_0Artificial.bmp"
CARPETA_IMG = "img"

# Constantes para los nombres de las imágenes generadas en cada punto
NOMBRE_IMAGEN_A = "imagen_a.png"
NOMBRE_IMAGEN_B = "imagen_b.png"
NOMBRE_IMAGEN_C = "imagen_c.png"
NOMBRE_IMAGEN_D = "imagen_d.png"
NOMBRE_IMAGEN_E = "imagen_e.png"
NOMBRE_IMAGEN_F = "imagen_f.png"
NOMBRE_IMAGEN_G = "imagen_g.png"

# Constantes para las operaciones lógicas, usadas con operacion_logica()
OPERACION_AND = "and"
OPERACION_OR = "or"
OPERACION_XOR = "xor"
OPERACION_NAND = "nand"
OPERACION_NOR = "nor"

def descargar_imagen(id_archivo=ID_IMAGEN_BASE, nombre_destino=NOMBRE_IMAGEN, carpeta=CARPETA_IMG):
    """Descarga un archivo desde Google Drive dado su ID.

    Si el archivo ya existe en la carpeta de destino, no vuelve a
    descargarlo. Construye la URL de descarga directa a partir del ID
    del archivo de Google Drive y descarga su contenido en memoria.

    Args:
        id_archivo (str, optional): ID del archivo en Google Drive,
            extraído de la URL para compartir (parte entre '/d/' y
            '/view'). Por defecto es ID_IMAGEN_BASE.
        nombre_destino (str, optional): Nombre con el que se guardará
            el archivo descargado. Por defecto es NOMBRE_IMAGEN.
        carpeta (str, optional): Carpeta donde se guardará el archivo.
            Por defecto es 'img'.

    Returns:
        str: Ruta completa donde está guardada la imagen (recién
        descargada, o ya existente de una ejecución anterior).

    Raises:
        requests.exceptions.RequestException: Si ocurre un error de red
            al intentar descargar el archivo.
    """
    ruta_destino = os.path.join(carpeta, nombre_destino)

    if os.path.exists(ruta_destino):
        return ruta_destino

    url_descarga = f"https://drive.google.com/uc?export=download&id={id_archivo}"

    sesion = requests.Session()
    respuesta = sesion.get(url_descarga, stream=True)

    # Google Drive puede devolver una página de confirmación cuando el
    # archivo es grande. Se busca el token de confirmación en las cookies.
    token_confirmacion = None
    for clave, valor in respuesta.cookies.items():
        if clave.startswith("download_warning"):
            token_confirmacion = valor
            break

    if token_confirmacion:
        parametros = {"id": id_archivo, "confirm": token_confirmacion}
        respuesta = sesion.get(
            "https://drive.google.com/uc?export=download",
            params=parametros,
            stream=True,
        )

    respuesta.raise_for_status()

    ruta_guardada = guardar_en_carpeta_img(respuesta.content, nombre_destino, carpeta)
    return ruta_guardada


def guardar_en_carpeta_img(contenido, nombre_destino, carpeta=CARPETA_IMG):
    """Guarda contenido binario dentro de una carpeta local.

    Si la carpeta indicada no existe, la crea antes de guardar el
    archivo.

    Args:
        contenido (bytes): Contenido binario a escribir en el archivo.
        nombre_destino (str): Nombre con el que se guardará el archivo.
        carpeta (str, optional): Carpeta donde se almacenará el
            archivo. Por defecto es 'img'.

    Returns:
        str: Ruta completa del archivo guardado.
    """
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)

    ruta_destino = os.path.join(carpeta, nombre_destino)

    with open(ruta_destino, "wb") as archivo:
        archivo.write(contenido)

    return ruta_destino


def binarizar_imagen(imagen, umbral=127, valor_maximo=255, invertir_automatico=True):
    """Convierte una imagen en escala de grises a una imagen binaria.

    Por defecto utiliza un umbral fijo de 127. Si se pasa umbral=None, el
    umbral se calcula automáticamente mediante el método de Otsu.

    Si invertir_automatico es True, se invierte el resultado de
    THRESH_BINARY. Esto es necesario en imágenes como la de este
    trabajo, donde las células son oscuras sobre un fondo claro: al
    umbralizar con THRESH_BINARY, el fondo (y no las células) queda en
    valor_maximo, así que hay que invertir para que el objeto de
    interés quede codificado en valor_maximo. La decisión de invertir
    o no queda a cargo de quien llama a la función, según la polaridad
    conocida de la imagen de entrada — no se intenta detectar
    automáticamente.

    Args:
        imagen (numpy.ndarray): Imagen en escala de grises a binarizar.
        umbral (int, optional): Valor de umbral fijo a utilizar. Si es
            None, el umbral se calcula automáticamente con el método
            de Otsu. Por defecto es 127.
        valor_maximo (int, optional): Valor asignado a los píxeles que
            representan al objeto de interés. Por defecto es 255.
        invertir_automatico (bool, optional): Si es True, invierte el
            resultado de THRESH_BINARY. Si es False, se respeta el
            resultado tal cual lo entrega THRESH_BINARY, sin invertir
            nada. Por defecto es True.

    Returns:
        numpy.ndarray: Imagen binaria resultante.
    """
    if umbral is None:
        _, imagen_binaria = cv2.threshold(imagen, 
                                          0, 
                                          valor_maximo, 
                                          cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    else:
        _, imagen_binaria = cv2.threshold(imagen, 
                                          umbral, 
                                          valor_maximo, 
                                          cv2.THRESH_BINARY)    

    if invertir_automatico:
        imagen_binaria = invertir_imagen(imagen_binaria)

    return imagen_binaria


def cargar_imagen_binaria(ruta_imagen, umbral=127, valor_maximo=255, invertir_automatico=True):
    """Carga una imagen desde disco y la convierte a binaria.

    Lee la imagen en escala de grises desde la ruta indicada y aplica
    la binarización correspondiente, siguiendo el criterio de umbral
    fijo empleado en el material de cátedra.

    Args:
        ruta_imagen (str): Ruta del archivo de imagen a cargar.
        umbral (int, optional): Valor de umbral fijo a utilizar. Si es
            None, el umbral se calcula automáticamente con el método
            de Otsu. Por defecto es 127.
        valor_maximo (int, optional): Valor asignado a los píxeles que
            representan al objeto de interés. Por defecto es 255.
        invertir_automatico (bool, optional): Si es True, invierte el
            resultado de THRESH_BINARY. Si es False, se respeta el
            resultado tal cual lo entrega THRESH_BINARY, sin invertir
            nada. Por defecto es True.

    Returns:
        numpy.ndarray: Imagen binaria resultante.

    Raises:
        FileNotFoundError: Si no se pudo leer la imagen desde la ruta
            indicada.
    """
    imagen_gris = cv2.imread(ruta_imagen, cv2.IMREAD_GRAYSCALE)

    if imagen_gris is None:
        raise FileNotFoundError(f"No se pudo leer la imagen: {ruta_imagen}")

    return binarizar_imagen(imagen_gris, umbral, valor_maximo, invertir_automatico)


def guardar_imagen(imagen, nombre_destino, carpeta=CARPETA_IMG, prefijo=None):
    """Guarda una imagen en disco dentro de una carpeta local.

    Si la carpeta de destino no existe, la crea antes de guardar la
    imagen. Pensada para almacenar tanto los resultados canónicos que
    se encadenan entre puntos (imagen A, B, C, etc., guardados
    directamente en carpeta, sin prefijo) como las imágenes
    intermedias de cada punto (guardadas en una subcarpeta con el
    nombre del prefijo, para no mezclarlas todas sueltas dentro de
    carpeta).

    Args:
        imagen (numpy.ndarray): Imagen a guardar.
        nombre_destino (str): Nombre del archivo de salida, incluyendo
            extensión (por ejemplo 'imagen_a.png').
        carpeta (str, optional): Carpeta donde se guardará la imagen.
            Por defecto es 'img'.
        prefijo (str, optional): Si se indica, la imagen se guarda
            dentro de una subcarpeta con ese nombre, dentro de
            carpeta (se crea si no existe). Si es None, se guarda
            directamente en carpeta. Por defecto es None.

    Returns:
        str: Ruta completa donde se guardó la imagen.

    Raises:
        IOError: Si OpenCV no pudo escribir la imagen en la ruta
            indicada (por ejemplo, por una extensión no soportada).
    """
    carpeta_destino = os.path.join(carpeta, prefijo) if prefijo else carpeta

    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)

    ruta_destino = os.path.join(carpeta_destino, nombre_destino)

    if not cv2.imwrite(ruta_destino, imagen):
        raise IOError(f"No se pudo guardar la imagen en: {ruta_destino}")

    return ruta_destino


def cargar_imagen_resultado(nombre_archivo, carpeta=CARPETA_IMG, invertir=True):
    """Carga una imagen resultado previamente guardada en disco.

    Pensada para que un punto lea el resultado guardado por un punto
    anterior (por ejemplo, que el Punto 2 cargue la imagen A generada
    por el Punto 1). Los resultados se guardan en polaridad visual
    (fondo blanco, células negras, igual a como se ven en el informe),
    por lo que, por defecto, esta función invierte la imagen al
    cargarla para devolverla en polaridad operativa (células en 255),
    lista para usarse en reconstrucción u operaciones lógicas.

    Args:
        nombre_archivo (str): Nombre del archivo a cargar, incluyendo
            extensión (por ejemplo 'imagen_a.png').
        carpeta (str, optional): Carpeta donde buscar el archivo. Por
            defecto es 'img'.
        invertir (bool, optional): Si es True, invierte la imagen
            cargada para pasar de polaridad visual a polaridad
            operativa. Si es False, devuelve la imagen tal cual está
            guardada en disco. Por defecto es True.

    Returns:
        numpy.ndarray: Imagen cargada en escala de grises.

    Raises:
        FileNotFoundError: Si no se pudo leer la imagen desde la ruta
            indicada.
    """
    ruta_origen = os.path.join(carpeta, nombre_archivo)
    imagen = cv2.imread(ruta_origen, cv2.IMREAD_GRAYSCALE)

    if imagen is None:
        raise FileNotFoundError(f"No se pudo leer la imagen: {ruta_origen}")

    if invertir:
        imagen = invertir_imagen(imagen)

    return imagen


def graficar_imagenes(imagenes, titulos, prefijo, filas=1, columnas=None,
                       titulo_general=None, carpeta=CARPETA_IMG):
    """Muestra y guarda una grilla de imágenes con matplotlib.

    Arma una figura con la cantidad de filas y columnas indicada,
    mostrando cada imagen de la lista en su celda correspondiente, en
    el mismo orden en que aparecen. Si la grilla tiene más celdas que
    imágenes, las celdas sobrantes quedan vacías (sin ejes ni imagen)
    en vez de lanzar un error.

    Args:
        imagenes (list): Lista de imágenes (numpy.ndarray) a mostrar,
            en el orden en que deben aparecer en la grilla.
        titulos (list): Lista de títulos, uno por imagen, en el mismo
            orden que imagenes.
        prefijo (str): Prefijo utilizado para nombrar el archivo
            guardado (por ejemplo 'punto3' genera
            'punto3_comparacion.png').
        filas (int, optional): Cantidad de filas de la grilla. Por
            defecto es 1.
        columnas (int, optional): Cantidad de columnas de la grilla.
            Si es None, se calcula automáticamente como la cantidad de
            imágenes (es decir, todas en una sola fila). Por defecto
            es None.
        titulo_general (str, optional): Título general de la figura,
            mostrado arriba de toda la grilla. Si es None, no se
            muestra. Por defecto es None.
        carpeta (str, optional): Carpeta donde se guardará la figura.
            Por defecto es 'img'.

    Returns:
        str: Ruta completa donde se guardó la figura.

    Raises:
        ValueError: Si la cantidad de imágenes no coincide con la
            cantidad de títulos, o si la grilla (filas x columnas) no
            alcanza para la cantidad de imágenes.
    """
    if len(imagenes) != len(titulos):
        raise ValueError(
            "La cantidad de imágenes debe coincidir con la cantidad de títulos."
        )

    if columnas is None:
        columnas = len(imagenes)

    if filas * columnas < len(imagenes):
        raise ValueError(
            "La grilla (filas x columnas) no alcanza para la cantidad de imágenes."
        )

    if not os.path.exists(carpeta):
        os.makedirs(carpeta)

    figura, ejes = plt.subplots(filas, columnas, figsize=(5 * columnas, 5 * filas))
    figura.patch.set_facecolor("#dddddd")
    ejes = np.array(ejes).reshape(-1)

    for indice, eje in enumerate(ejes):
        eje.set_facecolor("#dddddd")
        if indice < len(imagenes):
            eje.imshow(imagenes[indice], cmap="gray", vmin=0, vmax=255)
            eje.set_title(titulos[indice])
        eje.axis("off")

    if titulo_general is not None:
        figura.suptitle(titulo_general)

    plt.tight_layout()

    ruta_destino = os.path.join(carpeta, f"{prefijo}_comparacion.png")
    figura.savefig(ruta_destino)

    plt.show()

    return ruta_destino


def operacion_logica(imagen_a, imagen_b, operacion):
    """Aplica una operación lógica entre dos imágenes binarias.

    Centraliza las 5 operaciones lógicas del enunciado en una sola
    función. El parámetro operacion se pasa siempre con una de las
    constantes OPERACION_AND, OPERACION_OR, OPERACION_XOR,
    OPERACION_NAND, OPERACION_NOR definidas en este mismo módulo, en
    vez de escribir el texto suelto: así, un error de tipeo en el
    nombre de la constante falla de inmediato con NameError al
    llamarla, en vez de fallar en silencio con un string mal escrito.

    Args:
        imagen_a (numpy.ndarray): Primera imagen binaria.
        imagen_b (numpy.ndarray): Segunda imagen binaria.
        operacion (str): Una de las constantes OPERACION_* definidas
            en este módulo.

    Returns:
        numpy.ndarray: Resultado de aplicar la operación píxel a píxel.

    Raises:
        ValueError: Si operacion no es una de las 5 reconocidas.
    """
    if operacion == OPERACION_AND:
        return cv2.bitwise_and(imagen_a, imagen_b)
    elif operacion == OPERACION_OR:
        return cv2.bitwise_or(imagen_a, imagen_b)
    elif operacion == OPERACION_XOR:
        return cv2.bitwise_xor(imagen_a, imagen_b)
    elif operacion == OPERACION_NAND:
        return cv2.bitwise_not(cv2.bitwise_and(imagen_a, imagen_b))
    elif operacion == OPERACION_NOR:
        return cv2.bitwise_not(cv2.bitwise_or(imagen_a, imagen_b))
    else:
        raise ValueError(f"Operación desconocida: {operacion!r}")


def invertir_imagen(imagen):
    """Invierte los valores de una imagen binaria o en escala de grises.

    Args:
        imagen (numpy.ndarray): Imagen a invertir.

    Returns:
        numpy.ndarray: Imagen con los valores invertidos.
    """
    return cv2.bitwise_not(imagen)


def reconstruccion_morfologica(marcador, mascara):
    """Realiza la reconstrucción morfológica binaria por dilatación.

    Dilata repetidamente el marcador (elemento estructurante 3x3, de
    8-conectividad) intersecándolo con la máscara mediante AND lógico,
    hasta que la imagen resultante deja de cambiar entre iteraciones.

    Args:
        marcador (numpy.ndarray): Imagen binaria (0/255) que sirve
            como marcador, es decir, el punto de partida de la
            dilatación.
        mascara (numpy.ndarray): Imagen binaria (0/255) que sirve como
            máscara, es decir, el límite que no puede superar la
            dilatación.

    Returns:
        numpy.ndarray: Imagen binaria (0/255) reconstruida.

    Raises:
        ValueError: Si las dimensiones del marcador y la máscara no
            coinciden, o si el marcador no es subconjunto de la
            máscara (condición exigida por la reconstrucción
            morfológica).
    """
    if marcador.shape != mascara.shape:
        raise ValueError("Las dimensiones del marcador y la máscara deben ser iguales.")

    marcador_bool = marcador.astype(bool)
    mascara_bool = mascara.astype(bool)

    if np.any(marcador_bool & np.logical_not(mascara_bool)):
        raise ValueError(
            "El marcador no es subconjunto de la máscara: hay píxeles "
            "del marcador (en 255) que caen fuera de la máscara (en 0). "
        )

    reconstruida = marcador_bool.copy()

    while True:
        anterior = reconstruida.copy()
        dilatada = binary_dilation(reconstruida, structure=np.ones((3, 3)))
        reconstruida = dilatada & mascara_bool

        if np.array_equal(reconstruida, anterior):
            break

    return (reconstruida * 255).astype(np.uint8)


def crear_marcador_borde(imagen_binaria):
    """Construye un marcador restringido al marco exterior de la imagen.

    Genera una máscara con 255 únicamente en el marco exterior (fila
    superior, fila inferior, columna izquierda y columna derecha) de
    la imagen, y la combina con AND contra la imagen recibida. El
    resultado conserva solo los píxeles de esa imagen que caen justo
    sobre el borde, quedando en 0 en todo lo demás.

    Es una función genérica: sirve tanto para construir el marcador
    que identifica objetos que tocan el borde (aplicada directamente
    sobre la imagen binaria), como para la técnica de relleno de
    agujeros (aplicada sobre el complemento de la imagen).

    Args:
        imagen_binaria (numpy.ndarray): Imagen binaria (0/255) sobre
            la que se construye el marcador.

    Returns:
        numpy.ndarray: Marcador (0/255), subconjunto de
        imagen_binaria, con los píxeles del borde encendidos.
    """
    marco = np.zeros_like(imagen_binaria)
    marco[0, :] = 255
    marco[-1, :] = 255
    marco[:, 0] = 255
    marco[:, -1] = 255

    return operacion_logica(imagen_binaria, marco, OPERACION_AND)


def rellenar_agujeros(imagen):
    """Rellena los agujeros internos de una imagen binaria.

    Aplica la técnica de relleno de agujeros vista en clase: como la
    polaridad visual de una imagen coincide matemáticamente con el
    complemento de su polaridad operativa, se usa ese complemento
    directamente como máscara para reconstruir el fondo verdaderamente
    conectado al marco exterior de la imagen (dejando afuera los
    agujeros internos, que no lo tocan), y se invierte el resultado
    para obtener la imagen con los agujeros rellenados.

    Args:
        imagen (numpy.ndarray): Imagen binaria (0/255), en polaridad
            operativa (objeto de interés en 255).

    Returns:
        numpy.ndarray: Imagen con los agujeros rellenados (0/255), en
        la misma polaridad operativa que la entrada (objeto de
        interés, incluidos los agujeros ya rellenados, en 255).
    """
    complemento = invertir_imagen(imagen)
    marcador = crear_marcador_borde(complemento)
    reconstruida_fondo = reconstruccion_morfologica(marcador, complemento)

    return invertir_imagen(reconstruida_fondo)


def crear_elemento_estructurante(forma="cruz", tamano=3):
    """Crea un elemento estructurante para operaciones morfológicas.

    Args:
        forma (str, optional): Forma del elemento estructurante. Debe
            ser 'cruz', 'rectangulo' o 'elipse'. Por defecto es
            'cruz'.
        tamano (int, optional): Tamaño (ancho y alto) del elemento
            estructurante, en píxeles. Por defecto es 3.

    Returns:
        numpy.ndarray: Elemento estructurante generado.

    Raises:
        ValueError: Si la forma indicada no es una de las soportadas.
    """
    formas_soportadas = {
        "cruz": cv2.MORPH_CROSS,
        "rectangulo": cv2.MORPH_RECT,
        "elipse": cv2.MORPH_ELLIPSE,
    }

    if forma not in formas_soportadas:
        raise ValueError(
            f"Forma '{forma}' no soportada. Debe ser una de: "
            f"{list(formas_soportadas.keys())}"
        )

    return cv2.getStructuringElement(formas_soportadas[forma], (tamano, tamano))