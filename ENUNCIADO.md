# Enunciado — Trabajo Final

**Facultad Politécnica, UNA**
**Materia:** Procesamiento Digital de Imágenes
**Profesor:** Dr. José Luis Vázquez

## Contexto

En la Figura 1 del enunciado original se presenta una imagen que contiene
células de una misma colonia en varias fases de su vida. Los 4 tipos de
célula correspondientes a esas fases son:

- **Tipo 1**: célula sólida, sin agujero.
- **Tipo 2**: célula casi sólida, con un agujero pequeño (sin núcleo
  visible).
- **Tipo 3**: célula con anillo fino, agujero grande y un núcleo pegado a
  la pared interior del agujero.
- **Tipo 4**: célula con anillo fino, agujero grande y un núcleo suelto
  (no conectado a la pared) dentro del agujero.

El objetivo es clasificar las células según estos 4 tipos, siguiendo la
estrategia que se detalla en las 8 preguntas de abajo.

> **CUIDADO**: en ciertos puntos aparece el término **SOLAMENTE**. Esto
> significa que el uso de la dilatación y la erosión tradicionales está
> **formalmente prohibido** en esos puntos — solo se pueden usar
> herramientas de morfología matemática vistas en clase (reconstrucción,
> operaciones lógicas, inversión de imagen).

La imagen dada debe binarizarse (convertirse a binario), y para responder
todas las preguntas se debe programar una solución en Python con OpenCV.

## Las 8 preguntas

1. ¿Cómo, de forma automática, usando **SOLAMENTE** el proceso de
   reconstrucción, las operaciones lógicas (AND, OR, XOR, NAND, NOR) y la
   inversión de imagen, generar la imagen A sin pedazos ni células
   truncadas en los bordes de la imagen?
2. ¿Cómo, de forma automática, a partir de la imagen A, usando
   **SOLAMENTE** el proceso de reconstrucción, las operaciones lógicas
   (AND, OR, XOR, NAND, NOR) y la inversión de imagen, generar la imagen
   B de todos los agujeros de las células agujereadas (con citoplasma)?
3. ¿Cómo, de forma automática, a partir de la imagen B, usando
   **SOLAMENTE** el proceso de reconstrucción, las operaciones lógicas
   (AND, OR, XOR, NAND, NOR) y la inversión de imagen, generar la imagen
   C de todas las células agujereadas (con citoplasma) de Tipo 2, Tipo 3
   y Tipo 4?
4. ¿Cómo, de forma automática, a partir de la imagen C, usando
   **SOLAMENTE** el proceso de reconstrucción, las operaciones lógicas
   (AND, OR, XOR, NAND, NOR) y la inversión de imagen, generar la imagen
   D de todas las células no agujereadas (sin citoplasma) de Tipo 1?
5. ¿Cómo, de forma automática, a partir de la imagen C, usando
   **SOLAMENTE** el proceso de reconstrucción, las operaciones lógicas
   (AND, OR, XOR, NAND, NOR) y la inversión de imagen, generar la imagen
   E de todos los núcleos "sueltos" de las células de Tipo 4?
6. ¿Cómo, de forma automática, a partir de la imagen E, usando el proceso
   de reconstrucción, las operaciones lógicas (AND, OR, XOR, NAND, NOR),
   la inversión de imagen **y la dilatación y erosión tradicionales (no
   condicionales)**, generar la imagen F de todas las células de Tipo 4?
7. ¿Cómo, de forma automática, a partir de las imágenes A, D y F,
   usando las operaciones lógicas (AND, OR, XOR, NAND, NOR), generar la
   imagen G de todas las células de Tipo 2 y Tipo 3?
8. ¿Cómo harías para diferenciar las células de Tipo 2 y Tipo 3?

## Criterios de evaluación (resumen)

- Cumplimiento de cada consigna técnica, incluyendo las restricciones de
  operaciones permitidas en cada punto.
- Uso correcto de la imagen base y reproducibilidad de los resultados.
- Organización y claridad del código.
- Explicación clara del razonamiento seguido en el informe.
- Entrega en la fecha y el formato solicitados.