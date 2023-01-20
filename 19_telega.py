import os
import requests

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
from enum import Enum, auto


class States(Enum):
    CHOISE_REASON = auto()
    CHOISE_CATEGORY = auto()
    CHOISE_PEOPLE = auto()


def start(update, context):
    url = f"http://127.0.0.1:8000/reasons/send/"
    response = requests.get(url)
    categories = response.json()['reasons']
    categories.extend(["Без повода", "Другой повод"])
    message_keyboard = list(chunked(categories, 2))
    markup = ReplyKeyboardMarkup(
        message_keyboard,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    menu_msg = 'Привет. Выберите повод для букета'
    update.message.reply_text(text=menu_msg, reply_markup=markup)
    return States.CHOISE_REASON


def another_reason(update, context):
    update.message.reply_text('Напишите флористу')


def choise_category(update, context):
    url = f"http://127.0.0.1:8000/categories/send/"
    response = requests.get(url)
    categories = response.json()['categories']
    categories.extend(["Не важно"])
    message_keyboard = list(chunked(categories, 2))
    markup = ReplyKeyboardMarkup(
        message_keyboard,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    menu_msg = 'Выберите ценовую категорию'
    update.message.reply_text(text=menu_msg, reply_markup=markup)
    context.user_data['reason'] = update.message.text
    return States.CHOISE_CATEGORY


def get_bunch(update, context):
    context.user_data['category'] = update.message.text
    url = f"http://127.0.0.1:8000/bunch/send/"
    payload = {
        "category": context.user_data['category'],
        "reason": context.user_data['reason'],
    }
    response = requests.post(url, data=payload)

    if response.ok:
        bunches = response.json()
        pprint(bunches)
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

    return States.CHOISE_PEOPLE


def florist(update, context):
    update.message.reply_text('Напишите флористу')


if __name__ == '__main__':
    load_dotenv()
    tg_bot_token = os.getenv("TG_BOT_TOKEN")
    bot = Bot(token=tg_bot_token)
    updater = Updater(token=tg_bot_token, use_context=True)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            States.CHOISE_REASON: [
                MessageHandler(
                    Filters.text("Другой повод"), another_reason
                ),
                MessageHandler(
                    Filters.text, choise_category
                ),
            ],
            States.CHOISE_CATEGORY: [
                MessageHandler(
                    Filters.text, get_bunch
                )
            ],
            States.CHOISE_PEOPLE: [
                MessageHandler(
                    Filters.text("Флорист"), florist
                )
            ],
        },
        fallbacks=[],
        allow_reentry=True,
        name='bot_conversation',
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()
