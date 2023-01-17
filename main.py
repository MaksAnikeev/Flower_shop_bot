import os
from telegram import Update, Bot
from telegram.ext import (CallbackQueryHandler, CommandHandler, Filters,
                          MessageHandler, Updater)
from dotenv import load_dotenv

def main():
    load_dotenv()
    tg_bot_token = os.getenv("TG_BOT_TOKEN")
    bot = Bot(token=tg_bot_token)
    updater = Updater(token=tg_bot_token, use_context=True)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    updater.start_polling()
    updater.idle()

def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"К какому событию готовимся? Выберите один из вариантов, либо укажите свой"
    )


if __name__ == '__main__':
    main()