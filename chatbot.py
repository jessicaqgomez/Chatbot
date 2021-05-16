#!/usr/bin/env python
# pylint: disable=C0116
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import pandas as pd
import io
import re
from string import punctuation, digits

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_markdown_v2(
        fr'Hola, soy tu profesor de la universidad de Piltover, ¿cómo te llamas?',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Para  iniciar usa /start, para registrarte usa /registro y para consultar usa /consulta')



def saludo( update: Update, context):
    nombre = str(update.message.text.upper())
    if validacion_string(nombre):
        update.message.reply_text("tu nombre contiene elementos no validos, por favor ingresalo nuevamente")
    else:
        resp= "Hola "+nombre.lower()+", Si deseas registrarte escribe '/registro', Si ya te encuentras registrado y deseas consultar el estado de tu trabajo escribe /consulta"
        update.message.reply_text(resp)

def validacion_string(cadena):

    invalid_element = len(set(cadena).intersection(punctuation+digits))
    if invalid_element>0:
        return True
    return False


def registro(update: Update, context):
    mensaje = "Para registrarte por favor escribe: /datos y separado por espacios escribe tu nombre, apellido y url de tu trabajo. Por ejemplo: /datos Jessica Quintero mitrabajo.docx"
    update.message.reply_text(mensaje)

def datos(update: Update, context:CallbackContext):
    
    validar_nombre = not validacion_string(str(context.args[0]))
    validar_apellido = not validacion_string(str(context.args[1]))
    if(validar_nombre and validar_apellido):
        identificador = ultimo_id()
        usuario = {'id':identificador,'nombre': str(context.args[0]),'apellido':str(context.args[1]),'documento':str(context.args[2]),'estado': 'enviado'}
        
        if crear_usuario(usuario):
            update.message.reply_text("su identificador es "+ str(identificador))
    else:
        if ~validar_nombre:
            update.message.reply_text("el nombre no es valido, por favor ingresa los datos de nuevo usando /datos")
        else:
            update.message.reply_text("el apellido no es valido, por favor ingresa los datos de nuevo usando /datos")

def crear_usuario(diccionario):
    df = pd.DataFrame(diccionario,index=[0])
    
    df.to_csv('Datos_alumnos.csv',index=False, sep=';',mode='a',header=False)
    return True

def consulta(update: Update, context):
    mensaje = "Para consultar el estado de tu trabajo por favor escribe: /id y, separado por espacio, tu numero de identificación. Por ejemplo: /id 124 "
    update.message.reply_text(mensaje)

def validar_int(numero):
    if numero.isdigit():
        return True
    return False


def identificador(update: Update, context):
    numero_identificador = context.args[0]
    if (validar_int(numero_identificador)):
        estado = buscar_documento(int(numero_identificador))
        if estado is None:
            update.message.reply_text("el identificador no existe, por favor ingrese un identificador existente")
        else:
            update.message.reply_text("el estado de su documento es:"+ estado)
    else:
        update.message.reply_text("el numero identificador es invalido, por favor vuelve a ingresarlo usando la instrucción /id")

def ultimo_id():
    dataframe=pd.read_csv('Datos_alumnos.csv',delimiter=";")
    dataframe = dataframe.dropna()
    dataframe.id = dataframe.id.astype(int)
    busqueda = str(dataframe.tail(1)['id'])
    ultimo= int((re.split("[ \n]", busqueda))[4])+1
    return ultimo

def buscar_documento(id):
    dataframe=pd.read_csv('Datos_alumnos.csv',delimiter=";")
    dataframe = dataframe.dropna()
    dataframe.id = dataframe.id.astype(int)
    fila= dataframe[dataframe['id']== id]
    if fila.empty:
        estado = None
    else:
        estado = fila.estado.item()
    return estado

def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("1884200283:AAHZa1nA3nyTTIdFC1lMQn9lGGaMjCrn-JM")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("registro",registro))
    dispatcher.add_handler(CommandHandler("consulta",consulta))
    dispatcher.add_handler(CommandHandler("datos",datos))
    dispatcher.add_handler(CommandHandler("id", identificador))
    #dispatcher.add_handler(CommandHandler("",))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, saludo))
    
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()