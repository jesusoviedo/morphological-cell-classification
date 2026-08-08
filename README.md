# Clasificación de Células mediante Morfología Matemática

Clasificación automática de células de una colonia en sus distintas fases de
vida (4 tipos), utilizando herramientas de morfología matemática:
reconstrucción morfológica, operaciones lógicas (AND, OR, XOR, NAND, NOR) e
inversión de imagen. La mayoría de los puntos usa exclusivamente estas tres
herramientas (según lo exige el enunciado en cada caso); el punto 8, de
enfoque abierto, además usa erosión binaria tradicional como criterio de
diferenciación.

Trabajo desarrollado para la materia **Procesamiento Digital de Imágenes**,
Facultad Politécnica - UNA, a partir de una imagen base con células en
distintas fases (Tipo 1 a Tipo 4).

> El enunciado completo del trabajo (las 8 preguntas del ejercitario, la
> restricción de herramientas por punto, y los criterios de evaluación)
> está en [`ENUNCIADO.md`](ENUNCIADO.md).

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
├── ENUNCIADO.md          # texto completo del trabajo final (las 8 preguntas)
├── util.py               # funciones compartidas (descarga, binarización, etc.)
├── img/                  # se genera automáticamente al ejecutar los puntos
│   ├── 5ab3_0Artificial.bmp   # imagen base descargada
│   ├── imagen_a.png           # resultado canónico del punto 1
│   ├── imagen_b.png           # resultado canónico del punto 2
│   ├── ...                    # imagen_c.png ... imagen_g.png (puntos 3 a 7)
│   ├── imagen_tipo2.png       # resultado del punto 8 (Tipo 2) -- excepción,
│   │                          #   no sigue la nomenclatura de letra
│   ├── imagen_tipo3.png       # resultado del punto 8 (Tipo 3) -- ídem
│   ├── resumen_comparacion.png  # panel de síntesis (base + A a G + Tipo2/3)
│   ├── punto1/                # imágenes intermedias del punto 1 (máscara, marcador, etc.)
│   ├── punto2/                # imágenes intermedias del punto 2
│   ├── ...                    # una subcarpeta por punto (puntos 3 a 7)
│   ├── punto8_tipo2/          # intermedias del punto 8 (Tipo 2) -- excepción,
│   │                          #   el punto 8 usa 2 subcarpetas, no 1
│   └── punto8_tipo3/          # intermedias del punto 8 (Tipo 3) -- ídem
├── punto1_imagen_a.py    # células sin truncar en los bordes
├── punto2_imagen_b.py    # agujeros de células con citoplasma
├── punto3_imagen_c.py    # células agujereadas Tipo 2, 3 y 4
├── punto4_imagen_d.py    # células Tipo 1 sin citoplasma
├── punto5_imagen_e.py    # núcleos sueltos Tipo 4
├── punto6_imagen_f.py    # células Tipo 4 completas
├── punto7_imagen_g.py    # células Tipo 2 y Tipo 3
├── punto8_diferenciacion.py  # diferenciación entre Tipo 2 y Tipo 3 (parametrizable)
├── ejecutar_todos_los_puntos.py  # corre los 8 puntos en orden, en un solo comando
└── generar_resumen_pipeline.py   # panel resumen (imagen base + A a G + Tipo2/3)
```

Los resultados que se encadenan entre puntos (`imagen_a.png`, `imagen_b.png`,
etc.) se guardan directamente en `img/`, mientras que las imágenes
intermedias de cada punto (máscara, marcador, pasos de la reconstrucción,
etc.) se guardan en una subcarpeta `img/puntoN/` propia, para no mezclarlas
todas sueltas.

## Uso

### Todo en uno

La forma más simple de correr el trabajo completo es con
`ejecutar_todos_los_puntos.py`, que corre los 8 puntos en orden, uno
por uno, imprimiendo en la consola cuál se está ejecutando en cada
momento:

```bash
python ejecutar_todos_los_puntos.py
```

Si algún punto termina con error, la ejecución **se corta ahí mismo**
— los puntos siguientes no se llegan a correr, ya que dependerían de
un resultado que no se generó. El mensaje de error del punto que
falló se muestra en la consola tal cual, seguido de un aviso indicando
en qué punto se cortó la cadena.

### Punto por punto

También se puede ejecutar cada punto del enunciado como un script
independiente:

```bash
python punto1_imagen_a.py
python punto2_imagen_b.py
python punto3_imagen_c.py
python punto4_imagen_d.py
python punto5_imagen_e.py
python punto6_imagen_f.py
python punto7_imagen_g.py
python punto8_diferenciacion.py
```

Los puntos deben ejecutarse **en orden**, ya que cada uno depende del
resultado canónico guardado por el anterior (por ejemplo, `punto2_imagen_b.py`
carga `img/imagen_a.png`, generado por `punto1_imagen_a.py`). Si el archivo de
entrada correspondiente no existe todavía, el script va a fallar con un
`FileNotFoundError` indicando qué archivo falta.

La imagen base (`5ab3_0Artificial.bmp`) se descarga automáticamente la
primera vez que se ejecuta `punto1_imagen_a.py`; las ejecuciones siguientes
reutilizan el archivo ya descargado en `img/`.

`punto8_diferenciacion.py` es el único punto parametrizable: acepta un
argumento opcional `--tipo_celula` (`2` o `3`) para generar solamente ese
tipo. Sin el argumento, genera ambos:

```bash
python punto8_diferenciacion.py                  # genera Tipo 2 y Tipo 3
python punto8_diferenciacion.py --tipo_celula 2   # solo Tipo 2
python punto8_diferenciacion.py --tipo_celula 3   # solo Tipo 3
```

### Panel resumen

Una vez generados todos los resultados (puntos 1 a 8), `generar_resumen_pipeline.py`
arma un único panel con la imagen base y los 9 resultados canónicos (A a
G, más Tipo 2 y Tipo 3), pensado para el cierre del informe:

```bash
python generar_resumen_pipeline.py
```

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