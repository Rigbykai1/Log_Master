# Log_master: Exposición de Vulnerabilidades en Windows

Este proyecto tiene como objetivo demostrar cómo ciertas vulnerabilidades en la configuración de sistemas operativos y software pueden ser explotadas para obtener acceso no autorizado a dispositivos. El propósito de este proyecto es educativo y está diseñado para ser utilizado únicamente en entornos controlados y con el consentimiento explícito del propietario del sistema.

## Comenzando 🚀

Este repositorio contiene una serie de herramientas y scripts para realizar auditorías de seguridad en sistemas Windows. Estos scripts pueden ayudar a identificar y entender algunas de las debilidades más comunes en la seguridad, como la falta de control en la ejecución de programas no autorizados.

## Requisitos

- Python 3.x
- Módulos adicionales como `pynput`, `pyautogui`, y `pillow` (detallados en la instalación)

## Instalación 🔧

1. Clona este repositorio:

    ```bash
    git clone 
    ```

2. Navega a la carpeta del proyecto:

    ```bash
    cd Log_master
    ```

3. Instalación de modulos:

    ```bash
    No requiere instalación, cada modulo instala las dependencias por sí mismo.
    ```

4. El único permiso de usuario que solicita el script es al ejecutar el .bat para la instalación de Windows.


## Uso 👌

Este proyecto puede ser ejecutado en un entorno de prueba o una máquina controlada para simular y analizar las vulnerabilidades en el sistema operativo. **Nunca uses este script en sistemas sin el consentimiento explícito de su propietario**.

### Importante(realizar antes de ejecutar el optimizador.py)

El script realiza un envío de datos por la plataforma de Telegram, por lo que debes configurar un bot utilizando a [BotFather](https://t.me/BotFather).

- Crear un bot con /newbot y sigues los pasos hasta crearlo.
- Luego escribe /token y seleccionas el bot que hiciste.
- El API Token lo pegas en el script sender.py
- Una vez realizado el bot, haces un nuevo grupo, en el que debes agregar al bot Rose @MissRose_bot y el bot que creaste.
- Luego solo escribes /id y copias el ID para luego pegarlo en el script de sender.py


Para ejecutar el script, simplemente corre el siguiente comando:

```bash
py Optimizador.py
```

El script intentará acceder a ciertos directorios y configuraciones del sistema para demostrar cómo se podrían comprometer si no se gestionan correctamente las configuraciones de seguridad.
Instala los dos archivos importantes en documentos/utils, además instala la clave de registro para correr luego de cada reinicio.

Para eliminar lo que realiza el script escribe Windows + R y escribes regedit, luego avanzas por esta ruta "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run\OS_optimization".

## Construido con 🛠️

- **Python 3.x**: Lenguaje de programación utilizado.
- **pynput**: Para escuchar las teclas presionadas.
- **pyautogui**: Para realizar capturas de pantalla.
- **pillow**: Para comprimir las imágenes y ahorrar espacio.

## Contribuyendo 🖇️

Para contribuir, realiza un fork de este repositorio, agrega tus mejoras y abre un pull request con una descripción detallada de los cambios realizados.

## Versionado 📌

Este proyecto utiliza Git para el control de versiones. Puedes ver el historial de cambios desde el primer commit.

## Autores ✒️

- **Rigbykai1** - Proyecto - [Rigbykai1](https://github.com/Rigbykai1)

## Licencia 📄
Este proyecto no tiene licencia formal, pero puedes usarlo libremente y contribuir con mejoras si lo deseas.

## Agradecimientos 🎉
Gracias por tomarte el tiempo de leer este README.
- Comparte el proyecto con otros. 📢
- Invita a alguien del equipo a un café ☕ o una cerveza 🍺.
- Agradece públicamente a quienes han contribuido. 🤓

## Menciones
Plantilla realizada con ❤️ por Villanuevand 😊