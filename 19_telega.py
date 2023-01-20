import os
import requests
import pprint

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
from random import choice


class States(Enum):
    CHOISE_REASON = auto()
    CHOISE_CATEGORY = auto()
    CHOISE_PEOPLE = auto()
    MESSAGE_TO_FLORIST = auto()
    GET_NAME = auto()
    GET_ADDRESS = auto()
    GET_DELIVERY_PERIOD = auto()

class BotData:
    frorist_chat_id = 704859099
    courier_chat_id = 704859099
    # frorist_chat_id = 5432002795
    # courier_chat_id = 5432002795


def call_api(endpoint):
    url = f"http://127.0.0.1:8000/{endpoint}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def start(update, context):
    categories = call_api('reasons/send/')['reasons']
    categories.extend(["Без повода", "Другой повод"])
    message_keyboard = list(chunked(categories, 2))
    print(update.message.chat.id)

    markup = ReplyKeyboardMarkup(
        message_keyboard,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    menu_msg = 'К какому событию готовимся? Выберите один из вариантов, либо укажите свой'
    
    update.message.reply_text(text=menu_msg, reply_markup=markup)
    return States.CHOISE_REASON


def another_reason(update, context):
    update.message.reply_text('Напишите флористу')
    return States.MESSAGE_TO_FLORIST


def message_to_florist(update, context):
    update.message.chat.id = BotData.frorist_chat_id
    menu_msg = update.message.text
    update.message.reply_text(text=menu_msg)
    return


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
        if not bunches['bunch']:
            update.message.reply_text('Такого букета нет 😥')
        else:
            bunch = choice (bunches['bunch'])

            menu_msg = dedent(f"""\
                <b>{bunch.get('name')}</b>
                <b>Цена {bunch.get('price')} руб</b>
    
                <b>Описание</b>
                {bunch.get('description')}
                <b>Состав:</b>
                {bunch.get('composition')}
                """).replace("    ", "")

            context.user_data["order"] = menu_msg

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
    return States.MESSAGE_TO_FLORIST


def order(update, context):
    update.message.reply_text('Напишите ваше имя')
    return States.GET_NAME


def get_name(update, context):
    context.user_data["user_name"] = update.message.text
    update.message.reply_text('По какому адресу доставить')
    return States.GET_ADDRESS

def get_address(update, context):
    context.user_data["address"] = update.message.text
    update.message.reply_text('В какой день и в какое время желаете получить доставку')
    return States.GET_DELIVERY_PERIOD

def get_delivery_time(update, context):
    context.user_data["delivery_time"] = update.message.text
    update.message.reply_text('Спасибо за заказ, в ближайшее время курьер свяжется с вами')
    update.message.chat.id = BotData.courier_chat_id
    menu_msg = dedent(f"""\
                <b>Имя клиента: {context.user_data["user_name"]}</b>
                <b>Адрес: {context.user_data["address"]} </b>
                <b>Дата и время доставки: {context.user_data["delivery_time"]}</b>
                """).replace("    ", "")
    update.message.reply_text(text=menu_msg)
    return


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
            States.MESSAGE_TO_FLORIST: [
                MessageHandler(
                    Filters.text, message_to_florist
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
                ),
                MessageHandler(
                    Filters.text("Заказ"), order
                )

            ],
            States.GET_NAME: [
                MessageHandler(
                    Filters.text, get_name
                ),
            ],
            States.GET_ADDRESS: [
                MessageHandler(
                    Filters.text, get_address
                ),
            ],
            States.GET_DELIVERY_PERIOD: [
                MessageHandler(
                    Filters.text, get_delivery_time
                ),
            ],

        },
        fallbacks=[],
        allow_reentry=True,
        name='bot_conversation',
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()
