from telegram.ext import Updater, CommandHandler, ConversationHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

INPUT_TEXT = 0

def start(update, context):

    button1 = InlineKeyboardButton(
        text='Sobre el autor',
        url='https://www.google.com'
    )

    button2 = InlineKeyboardButton(
        text='Twitter',
        url='https://www.twitter.com/jonascub'
    )

    update.message.reply_text(
        text = 'Haz click en un botón.',
        reply_markup = InlineKeyboardMarkup([
            [button1],
            [button2]
        ])
    )

if __name__ == '__main__':

    updater = Updater(token='1567579918:AAESqcz3McNtKJ_ep_1guLKbuEMowkxS3Lk', use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))

    updater.start_polling()
    updater.idle()