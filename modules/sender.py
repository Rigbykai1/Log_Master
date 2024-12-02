from utils import verificar_modulo
from utils import instalar_modulo
import time


# Función para cargar los módulos e instalarlos si no lo están
def cargar_modulos():
    global InputFile, Application
    if not verificar_modulo("telegram"):
        instalar_modulo("python-telegram-bot")

    from telegram import InputFile
    from telegram.ext import Application


# Función asincrónica para enviar un documento
async def enviar_documento(documento):
    cargar_modulos()

    api_token = ""
    chat_id = ""
    

    application = Application.builder().token(api_token).build()
    bot = application.bot
    try:
        with open(documento, 'rb') as file:
            await bot.send_document(chat_id=chat_id, document=InputFile(file, filename=documento))
    except Exception as error:
        print(f"Parece que hubo un error al enviar el documento: {error}")
        time.sleep(5)
        await bot.send_document(chat_id=chat_id, document=InputFile(file, filename=documento))


def main():
    print("Cargando Sender...")


if __name__ == "__main__":
    main()
