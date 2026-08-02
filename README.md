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

### Dependencias principales

- Python 3.14
- OpenCV
- Matplotlib
- Spyder (IDE)

## Estructura del proyecto

```
morphological-cell-classification/
├── environment.yml       # definición del entorno conda
├── util.py               # funciones compartidas (descarga, binarización, etc.)
├── img/                  # imagen base y resultados intermedios (se genera automáticamente)
└── README.md
```

## Convenciones de código

- Docstrings en formato Google (`Args`, `Returns`, etc.)
- Sin type hints
- Nombres de métodos y variables en español

## Uso

*(Sección a completar a medida que se desarrollen los scripts de cada punto
del enunciado.)*