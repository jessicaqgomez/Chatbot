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
    return True


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