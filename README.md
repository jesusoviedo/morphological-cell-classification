# Clasificación de Células mediante Morfología Matemática

Clasificación automática de células de una colonia en sus distintas fases de
vida (4 tipos), utilizando exclusivamente herramientas de morfología
matemática: reconstrucción morfológica, operaciones lógicas (AND, OR, XOR,
NAND, NOR) e inversión de imagen.

Trabajo desarrollado para la materia **Procesamiento Digital de Imágenes**,
Facultad Politécnica - UNA, a partir de una imagen base con células en
distintas fases (Tipo 1 a Tipo 4).

## Configuración del entorno

El entorno se gestiona con **conda** y está definido en `environment.yml`.

Para crear el entorno:

```bash
conda env create -f environment.yml
```

Para activarlo:

```bash
conda activate trabajo_final
```

Si más adelante se agregan dependencias nuevas al `environment.yml`, el
entorno se actualiza con:

```bash
conda env update -f environment.yml --prune
```

## Estructura del proyecto

```
morphological-cell-classification/
├── .gitignore
├── environment.yml       # definición del entorno conda
├── LICENSE               # MIT
├── README.md
├── util.py               # funciones compartidas (descarga, binarización, etc.)
├── img/                  # se genera automáticamente al ejecutar los puntos
│   ├── 5ab3_0Artificial.bmp   # imagen base descargada
│   ├── imagen_a.png           # resultado canónico del punto 1
│   ├── imagen_b.png           # resultado canónico del punto 2
│   ├── ...                    # imagen_c.png, imagen_d.png, etc., a medida que se resuelven
│   ├── punto1/                # imágenes intermedias del punto 1 (máscara, marcador, etc.)
│   ├── punto2/                # imágenes intermedias del punto 2
│   └── ...                    # una subcarpeta por cada punto resuelto
├── punto1_imagen_a.py    # células sin truncar en los bordes
├── punto2_imagen_b.py    # agujeros de células con citoplasma
├── punto3_imagen_c.py    # células agujereadas Tipo 2, 3 y 4
├── punto4_imagen_d.py    # células Tipo 1 sin citoplasma
├── punto5_imagen_e.py    # núcleos sueltos Tipo 4
├── punto6_imagen_f.py    # células Tipo 4 completas (dilatación/erosión permitida)
├── punto7_imagen_g.py    # células Tipo 2 y Tipo 3
└── punto8_diferenciacion.py  # diferenciación entre Tipo 2 y Tipo 3
```

> Los archivos `puntoN_*.py` se van a ir agregando a medida que se resuelva
> cada punto del enunciado.

Los resultados que se encadenan entre puntos (`imagen_a.png`, `imagen_b.png`,
etc.) se guardan directamente en `img/`, mientras que las imágenes
intermedias de cada punto (máscara, marcador, pasos de la reconstrucción,
etc.) se guardan en una subcarpeta `img/puntoN/` propia, para no mezclarlas
todas sueltas.

## Uso

Cada punto del enunciado se ejecuta como un script independiente:

```bash
python punto1_imagen_a.py
python punto2_imagen_b.py
python punto3_imagen_c.py
python punto4_imagen_d.py
python punto5_imagen_e.py
```

Los puntos deben ejecutarse **en orden**, ya que cada uno depende del
resultado canónico guardado por el anterior (por ejemplo, `punto2_imagen_b.py`
carga `img/imagen_a.png`, generado por `punto1_imagen_a.py`). Si el archivo de
entrada correspondiente no existe todavía, el script va a fallar con un
`FileNotFoundError` indicando qué archivo falta.

La imagen base (`5ab3_0Artificial.bmp`) se descarga automáticamente la
primera vez que se ejecuta `punto1_imagen_a.py`; las ejecuciones siguientes
reutilizan el archivo ya descargado en `img/`.

*(Los comandos de `punto6_imagen_f.py`, `punto7_imagen_g.py` y
`punto8_diferenciacion.py` se agregan a medida que se resuelven.)*

## Autores

* **Jesús Oviedo Riquelme** - j92riquelme@gmail.com
* **Sofía Rivas Gaona** - sofiarivasgaona@gmail.com
* **Liz Torres Cáceres** - kokoldtc@gmail.com
* **Gabriela Velázquez Sánchez** - vsga17@gmail.com
* **Miguel Angel Vera** - miguev83@gmail.com
* **Ernesto Yampey Cristaldo** - e.yampey@hotmail.com

## Licencia

Este proyecto está bajo la licencia MIT — ver el archivo [LICENSE](LICENSE)
para más detalles. En resumen, permite usar, copiar, modificar y distribuir
el código libremente, incluso con fines comerciales, siempre que se
mantenga el aviso de copyright original.