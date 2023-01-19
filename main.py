import os
from telegram import Update, Bot, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (CallbackQueryHandler, CommandHandler, Filters,
                          MessageHandler, Updater)
from dotenv import load_dotenv

def main():
    load_dotenv()
    tg_bot_token = os.getenv("TG_BOT_TOKEN")
    bot = Bot(token=tg_bot_token)
    updater = Updater(token=tg_bot_token, use_context=True)
    app = updater.dispatcher
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(CommandHandler('help', help_command))
    updater.start_polling()
    updater.idle()


def start(update, context):
    keyboard = [
        [
            InlineKeyboardButton("День рождения", callback_data='1'),
            InlineKeyboardButton("Свадьба", callback_data='2'),
        ],
        [   InlineKeyboardButton("В школу", callback_data='3'),
            InlineKeyboardButton("Без повода", callback_data='4'),
        ],
        [InlineKeyboardButton("Другой повод", callback_data='5')],
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)    
    update.message.reply_text('К какому событию готовимся? Выберите один из вариантов, либо укажите свой:', reply_markup=reply_markup)
    


def button(update, context):
    query = update.callback_query
    variant = query.data    
    query.answer()    
    query.edit_message_text(text=f"Выбранный вариант: {variant}")


def help_command(update, context):
    update.message.reply_text("Используйте `/start` для тестирования.")
    

if __name__ == '__main__':
    main()