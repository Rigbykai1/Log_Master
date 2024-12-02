import os
import sys
import subprocess

def limpiar_consola():
    os.system('cls' if os.name == 'nt' else 'clear')

def cargar_modulos():
    global psutil
    import psutil
        
def verificar_dependencias(paquetes):
    try:
        cargar_modulos()
    except:
        print("Error al cargar optimizaciones")
        for paquete in paquetes:
            print(f"Cargando optimizacion...")
            subprocess.run([sys.executable, "-m", "pip", "install", paquete], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            limpiar_consola()


def cerrar_procesos_usuario():
    memoria_liberada = 0
    procesos_criticos = ["explorer.exe", "python.exe",
                         "cmd.exe", "taskmgr.exe"]
    rutas_sistema = ["c:\\windows", "c:\\program files",
                     "c:\\program files (x86)"]

    for proceso in psutil.process_iter(['pid', 'name', 'exe', 'memory_info']):
        try:
            nombre = proceso.info['name']
            pid = proceso.info['pid']
            ruta = (proceso.info['exe'] or "").lower()
            memoria = proceso.info['memory_info'].rss

            if nombre.lower() not in procesos_criticos and not any(ruta.startswith(ruta_sis) for ruta_sis in rutas_sistema):
                proceso.terminate()
                memoria_liberada += memoria / (1024 ** 2)
                print(f"Proceso '{nombre}' cerrado.")

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    print(f"\nMemoria total liberada: {memoria_liberada:.2f} MB.")


def main():
    try:
        print("Cerrando procesos de usuario...\n")
        paquetes = ["psutil"]
        verificar_dependencias(paquetes)
        cerrar_procesos_usuario()
    except Exception as e:
        print("\nError inesperado...")


if __name__ == "__main__":
    main()
    
