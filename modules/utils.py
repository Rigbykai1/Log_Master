import subprocess
import importlib
import sys


# Función para verificar si un módulo está instalado
def verificar_modulo(modulo):
    try:
        importlib.import_module(modulo)
        return True
    except ImportError:
        return False


# Función para instalar el módulo si no está presente
def instalar_modulo(paquete):
    subprocess.run([sys.executable, "-m", "pip", "install", paquete],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main():
    print("Cargando modulos")


if __name__ == "__main__":
    main()
