import os
import qrcode
from telegram import ChatAction, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, ConversationHandler, CallbackQueryHandler, MessageHandler, Filters


INPUT_TEXT = 0


def start(update, context):
    
    update.message.reply_text(
        text='Hola, bienvenido, qué deseas hacer?\n\nUsa /qr para generar un código QR.',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text='Generar QR.', callback_data='qr')],
            [InlineKeyboardButton(text='Sobre el Autor', url='https://www.twitter.com/jonascub')]
        ])
    )

def qr_command_handler(update, context):
    
    update.message.reply_text('Enviame el texto para generarte un código QR.')
    return INPUT_TEXT

def qr_callback_handler(update, context):

    query = update.callback_query
    query.answer()

    query.edit_message_text(
        text='Enviame el texto para generarte un código QR.'
    )

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
    updater = Updater(token='1567579918:AAESqcz3McNtKJ_ep_1guLKbuEMowkxS3Lk', use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler('start', start))

    dp.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler('qr', qr_command_handler),
            CallbackQueryHandler(pattern='qr', callback=qr_callback_handler)
        ],
        states={
            INPUT_TEXT: [MessageHandler(Filters.text, input_text)]
        },
        fallbacks=[]
    ))

    updater.start_polling()
    updater.idle()