import os
import requests
import time

from telegram import (InlineKeyboardButton, InlineKeyboardMarkup, Update, Bot,
                      ReplyKeyboardMarkup, KeyboardButton)
from telegram.ext import (CallbackQueryHandler, CallbackContext,
                          CommandHandler, ConversationHandler,
                          MessageHandler, Updater, Filters)
from telegram import ParseMode
from dotenv import load_dotenv
from pprint import pprint
from textwrap import dedent
from more_itertools import chunked


load_dotenv()
tg_bot_token = os.getenv("TG_BOT_TOKEN")
bot = Bot(token=tg_bot_token)
updater = Updater(token=tg_bot_token)
dispatcher = updater.dispatcher


def start(update, context):
    context.bot.send_message(update.effective_chat.id, text='Привет хочешь букет')
    time.sleep(3)
    return choise(update, context)


def choise(update, context):
    url = f"http://127.0.0.1:8000/categories/send/"
    response = requests.get(url)
    print(response)
    categories = response.json()['categories']
    categories.extend(["Не важно", "Свое предложение"])
    message_keyboard = list(chunked(categories, 2))
    markup = ReplyKeyboardMarkup(
        message_keyboard,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    menu_msg = 'Пора бы сделать выбор'
    update.message.reply_text(text=menu_msg, reply_markup=markup)






def get_bunch(update, context):
    url = f"http://127.0.0.1:8000/bunch/send/"
    payload = {
        "category": 'более 2000р',
        "reason": 'День рождения',
    }
    response = requests.post(url, data=payload)

    if response.ok:
        bunches = response.json()
        bunch = bunches['bunch'][0]

        menu_msg = dedent(f"""\
            <b>{bunch.get('name')}</b>
            <b>Цена {bunch.get('price')} руб</b>

            <b>Описание</b>
            {bunch.get('description')}
            <b>Состав:</b>
            {bunch.get('composition')}
            """).replace("    ", "")

        message_keyboard = [
            [
                "Флорист",
                "Заказ"
            ]
        ]
        markup = ReplyKeyboardMarkup(
            message_keyboard,
            resize_keyboard=True,
            one_time_keyboard=True
        )
        bunch_img = requests.get(bunch['image'])
        update.message.reply_photo(
            bunch_img.content,
            caption=menu_msg,
            reply_markup=markup,
            parse_mode=ParseMode.HTML
        )
    else:
        update.message.reply_text('Такого букета нет 😥')


def get_no(update, context):
    update.message.reply_text('Ну и дура')


def choise2(update, context):
    keyboard = [
        [InlineKeyboardButton('Позвонить', callback_data='1'), InlineKeyboardButton('Написать', callback_data='2')],
    ]
    update.message.reply_text('Дай ответ', reply_markup=InlineKeyboardMarkup(keyboard))


def button(update, context):
    q = update.callback_query
    q.answer()
    if q.data == '1':
        context.bot.send_message(update.effective_chat.id, 'Че звонить когда все заняты')
    elif q.data == '2':
        context.bot.send_message(update.effective_chat.id, 'Пиши, все равно не ответим')

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

get_bunch_handler = MessageHandler(Filters.text("✅ Да"), get_bunch)
dispatcher.add_handler(get_bunch_handler)

get_no_handler = MessageHandler(Filters.text("❌ Нет"), get_no)
dispatcher.add_handler(get_no_handler)

florist_handler = MessageHandler(Filters.text("Флорист"), choise2)
dispatcher.add_handler(florist_handler)

button_handler = CallbackQueryHandler(button)
dispatcher.add_handler(button_handler)

updater.start_polling()
updater.idle()
