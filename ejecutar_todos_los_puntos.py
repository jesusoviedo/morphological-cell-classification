# -*- coding: utf-8 -*-
"""Ejecuta todos los puntos del trabajo final, en orden, en un solo comando.

Corre cada punto (1 a 8) como un proceso independiente, en el mismo
orden en que se ejecutarían a mano (cada uno depende del resultado
canónico guardado por el anterior). Si un punto termina con error, se
corta la cadena ahí mismo.
"""

import subprocess
import sys

# Los 8 puntos, en el orden en que dependen unos de otros.
PUNTOS = [
    "punto1_imagen_a.py",
    "punto2_imagen_b.py",
    "punto3_imagen_c.py",
    "punto4_imagen_d.py",
    "punto5_imagen_e.py",
    "punto6_imagen_f.py",
    "punto7_imagen_g.py",
    "punto8_diferenciacion.py",
]


def ejecutar_punto(nombre_script):
    """Ejecuta un script de un punto como proceso independiente.

    Usa el mismo intérprete de Python que está corriendo este script
    (sys.executable), para respetar el entorno conda activo. No
    captura la salida del proceso hijo: los print() de cada punto se
    siguen viendo en la consola tal cual, en tiempo real.

    Args:
        nombre_script (str): Nombre del archivo .py a ejecutar (por
            ejemplo, "punto1_imagen_a.py").

    Returns:
        bool: True si el script terminó sin errores (código de salida
        0), False en caso contrario.
    """
    print()
    print("=" * 60)
    print(f"Ejecutando {nombre_script}...")
    print("=" * 60)

    try:
        resultado = subprocess.run([sys.executable, nombre_script])
    except FileNotFoundError:
        print(f"No se encontró el archivo {nombre_script} en esta carpeta.")
        return False

    return resultado.returncode == 0


def main():
    """Corre los 8 puntos en orden, cortando la cadena ante el primer error."""
    for nombre_script in PUNTOS:
        exito = ejecutar_punto(nombre_script)

        if not exito:
            print()
            print(f"{nombre_script} terminó con error -- se detiene la ejecución.")
            print("Los puntos siguientes no se llegaron a ejecutar.")
            sys.exit(1)

    print()
    print("=" * 60)
    print("Los 8 puntos se ejecutaron correctamente, de punta a punta.")
    print("=" * 60)


if __name__ == "__main__":
    main()