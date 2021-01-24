import os
import qrcode
from telegram import ChatAction
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters


INPUT_TEXT = 0


def start(update, context):
    
    update.message.reply_text('Hola, bienvenido, qué deseas hacer?\n\nUsa /qr para generar un código QR.')

def qr_command_handler(update, context):
    
    update.message.reply_text('Enviame un texto para generarte un código QR.')
    return INPUT_TEXT

def input_text(update, context):
    
    chat =  update.message.chat
    text =  update.message.text

    filname = generate_qr(text)
    send_qr(filname, chat)

    return ConversationHandler.END

def generate_qr(text):
    
    filename = text + '.jpg'
    img = qrcode.make(text)
    img.save(filename)

    return filename

def send_qr(filename, chat):
    
    chat.send_action(
        action=ChatAction.UPLOAD_PHOTO,
        timeout=None
    )

    chat.send_photo(
        photo = open(filename, 'rb')
    )

    os.unlink(filename)


if __name__ == '__main__':
    updater = Updater(token='TOKEN', use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler('start', start))

    dp.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler('qr', qr_command_handler)
        ],
        states={
            INPUT_TEXT: [MessageHandler(Filters.text, input_text)]
        },
        fallbacks=[]
    ))

    updater.start_polling()
    updater.idle()