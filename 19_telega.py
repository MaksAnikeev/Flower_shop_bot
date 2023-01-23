import os
from enum import Enum, auto
from random import choice
from textwrap import dedent
from time import sleep

import phonenumbers
import requests
from dotenv import load_dotenv
from more_itertools import chunked
from telegram import (Bot, InlineKeyboardButton, InlineKeyboardMarkup,
                      KeyboardButton, ParseMode, ReplyKeyboardMarkup, Update)
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          CommandHandler, ConversationHandler, Filters,
                          MessageHandler, Updater)


class States(Enum):
    START = auto()
    CHOISE_REASON = auto()
    CHOISE_CATEGORY = auto()
    CHOISE_PEOPLE = auto()
    REASON_TO_FLORIST = auto()
    MESSAGE_TO_FLORIST = auto()
    MESSAGE_TO_COURIER = auto()
    GET_NAME = auto()
    GET_BUNCH_ID = auto()
    GET_ADDRESS = auto()
    USER_PHONE_NUMBER = auto()
    GET_DELIVERY_PERIOD = auto()
    CONFIRM_ORDER = auto()


class BotData:
    FLORIST_CHAT_ID = 704859099
    COURIER_CHAT_ID = 704859099
    # frorist_chat_id = 704859099
    # courier_chat_id = 5432002795


def call_api_get(endpoint):
    url = f"http://127.0.0.1:8000/{endpoint}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def call_api_post(endpoint, payload):
    url = f"http://127.0.0.1:8000/{endpoint}"
    response = requests.post(url, data=payload)
    response.raise_for_status()
    return response.json()


def greeting(update, context):
    if update.message.chat.id == BotData.COURIER_CHAT_ID:
        update.message.reply_text('Напишите дату на которую хотите посмотреть заказы в формате YYYY-MM-DD (2023-01-23)')
        return States.MESSAGE_TO_COURIER

    greeting_msg = '''Закажите доставку праздничного букета,
    собранного специально для ваших любимых, родных и коллег.
    Наш букет со смыслом станет главным подарком на вашем празднике!'''
    update.message.reply_text(text=greeting_msg)
    sleep(2)
    update.message.reply_text(text='Для продолжения нажми любую клавишу')
    return States.START


def start(update, context):
    reasons = call_api_get('reasons/send/')['reasons']
    context.user_data['reasons'] = reasons
    reasons.extend(["Без повода", "Другой повод"])
    message_keyboard = list(chunked(reasons, 2))

    markup = ReplyKeyboardMarkup(
        message_keyboard,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    menu_msg = 'К какому событию готовимся? Выберите один из вариантов, либо укажите свой'

    update.message.reply_text(text=menu_msg, reply_markup=markup)
    return States.CHOISE_REASON


def another_reason(update, context):
    update.message.reply_text('Напишите ваш повод и флорист с вами свяжется')
    return States.REASON_TO_FLORIST


def get_phonenumber(update, context):
    context.user_data['another_reason'] = update.message.text
    update.message.reply_text('Напишите номер телефона, по которому с вами свяжется флорист.'
                              ' Номер вводится в формате +7(946)3457687')
    return States.MESSAGE_TO_FLORIST


def message_to_florist(update, context):
    phone_number = phonenumbers.parse(update.message.text, "RU")
    if not phonenumbers.is_valid_number(phone_number):
        message_keyboard = [
            [
                KeyboardButton(
                    'Отправить свой номер телефона',
                    request_contact=True)
            ]
        ]
        markup = ReplyKeyboardMarkup(
            message_keyboard,
            one_time_keyboard=True,
            resize_keyboard=True)
        error_message = dedent("""\
            Введенный номер некорректен. Номер вводится в формате +7(946)3457687. Попробуйте снова:
            """)
        update.message.reply_text(error_message, reply_markup=markup)
        return States.MESSAGE_TO_FLORIST

    context.user_data["phone_number"] = update.message.text
    menu_msg = dedent(f"""\
            <b>Ваше сообщение отправлено флористу, он свяжется с вами в ближайшее время</b>
            
            <b>Повод клиента:</b>
            {context.user_data['another_reason']}
            <b>Телефон для связи:</b>
            {context.user_data["phone_number"]}
            """).replace("    ", "")
    update.message.reply_text(
        text=menu_msg,
        parse_mode=ParseMode.HTML
    )
    update.message.chat.id = BotData.FLORIST_CHAT_ID
    menu_msg = dedent(f"""\
            это видит флорист
            <b>Повод клиента:</b>
            {context.user_data['another_reason']}
            <b>Телефон для связи:</b>
            {context.user_data["phone_number"]}
            """).replace("    ", "")
    update.message.reply_text(
        text=menu_msg,
        parse_mode=ParseMode.HTML
    )
    return


def send_orders_courier(update, context):
    payload = {
        "delivered_at": update.message.text,
    }
    response = call_api_post('courier/send/', payload=payload)
    orders = response['orders']
    update.message.chat.id = BotData.COURIER_CHAT_ID

    for order in orders:
        menu_msg = dedent(f"""\
                    <b>Адрес:</b>
                    {order['address']}
                    <b>Время доставки:</b>
                    {order['delivered_at']}
                    <b>Контактное лицо:</b>
                    {order['firstname']}
                    <b>Тип оплаты:</b>
                    {order['method_payment']}
                    <b>Телефон:</b>
                    {order['phonenumber']}
                    <b>ID букета:</b>
                    {order['bunch_id']}
                    <b>Цена:</b>
                    {order['price']}
                    <b>Комментарий:</b>
                    {order['comment']}
                    """).replace("    ", "")
        update.message.reply_text(
            text=menu_msg,
            parse_mode=ParseMode.HTML
        )
    return


def choise_category(update, context):
    response = call_api_get('categories/send/')
    categories = response['categories']
    context.user_data['categories'] = categories
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


def get_answer_from_catalogue(context, random_category=False):
    payload = {
        "category": context.user_data['category'],
        "reason": context.user_data['reason'],
    }
    response = call_api_post('bunch/send/', payload=payload)
    if random_category:
        response = call_api_get('random_bunch/send/')
    return response


def get_bunch(update, context):
    context.user_data['category'] = update.message.text
    bunches = get_answer_from_catalogue(context)
    if not bunches['bunch']:
        get_default_bunch(update, context)
        return States.START
    context.user_data['bunches'] = bunches
    get_choice_bunch(update, context)
    return States.CHOISE_PEOPLE


def get_default_bunch(update, context):
    update.message.reply_text('Букета по критериям нет😥, выводится случайный букет')
    response = call_api_get('random_bunch/send/')
    bunch = response['bunch']
    menu_msg = get_menu_msg(bunch)
    context.user_data["order"] = menu_msg
    message_keyboard = [
        [
            "Флорист",
            "Заказ"],
        ["Задать другие параметры"],
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
    return States.START


def get_menu_msg(bunch):
    menu_msg = dedent(f"""\
        <b>{bunch.get('name')}</b>
        <b>Цена {bunch.get('price')} руб</b>
        <b>Описание</b>
        {bunch.get('description')}
        <b>Состав:</b>
        {bunch.get('composition')}
        <b>id букета:</b>
        {bunch.get('bunch_id')}
        """).replace("    ", "")
    return menu_msg


def get_choice_bunch(update, context):
    bunch = choice(context.user_data['bunches']['bunch'])
    menu_msg = get_menu_msg(bunch)
    context.user_data["order"] = menu_msg
    message_keyboard = [
        [
            "Флорист",
            "Заказ"],
        ["Другой букет",
         "Все букеты"]
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

    return States.CHOISE_PEOPLE


def show_all_bunches(update, context):
    bunches = context.user_data['bunches']
    for bunch in bunches['bunch']:
        menu_msg = get_menu_msg(bunch)
        bunch_img = requests.get(bunch['image'])
        update.message.reply_photo(
            bunch_img.content,
            caption=menu_msg,
            parse_mode=ParseMode.HTML
        )
    message_keyboard = [
        [
            "Флорист",
            "Заказ"],
        [
            "Другой букет",
            "Все букеты"]
    ]
    markup = ReplyKeyboardMarkup(
        message_keyboard,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    update.message.reply_text(text='Выберите букет', reply_markup=markup)
    return States.CHOISE_PEOPLE


def florist(update, context):
    update.message.reply_text('Напишите флористу')
    return States.REASON_TO_FLORIST


def order(update, context):
    update.message.reply_text('Напишите ваше имя')
    return States.GET_NAME


def get_name(update, context):
    context.user_data["user_name"] = update.message.text
    update.message.reply_text('Напишите id понравившегося букета. Он есть в описании букета.')
    return States.GET_BUNCH_ID


def get_bunch_id(update, context):
    context.user_data["bunch_id"] = update.message.text
    update.message.reply_text('По какому адресу доставить')
    return States.GET_ADDRESS


def get_address(update, context):
    context.user_data["address"] = update.message.text
    update.message.reply_text('Введите номер телефона для связи. Номер вводится в формате +7(946)3457687')
    return States.USER_PHONE_NUMBER


def get_user_phone_number(update: Update, context: CallbackContext) -> States:
    phone_number = phonenumbers.parse(update.message.text, "RU")
    if not phonenumbers.is_valid_number(phone_number):
        message_keyboard = [
            [
                KeyboardButton(
                    'Отправить свой номер телефона',
                    request_contact=True)
            ]
        ]
        markup = ReplyKeyboardMarkup(
            message_keyboard,
            one_time_keyboard=True,
            resize_keyboard=True)
        error_message = dedent("""\
        Введенный номер некорректен. Номер вводится в формате +7(946)3457687'. Попробуйте снова:
        """)
        update.message.reply_text(error_message, reply_markup=markup)
        return States.USER_PHONE_NUMBER
    context.user_data["phone_number"] = update.message.text
    update.message.reply_text(
        'В какой день и в какое время желаете получить доставку. Напишите дату в формате YYYY-MM-DD HH:MM (2023-01-23 15:00)')
    return States.GET_DELIVERY_PERIOD


def get_delivery_time(update, context):
    context.user_data["delivery_time"] = update.message.text
    update.message.reply_text('Пожалуйста, проверьте детали заказа')
    payload = {
        'firstname': context.user_data["user_name"],
        'address': context.user_data["address"],
        'phonenumber': context.user_data["phone_number"],
        'delivered_at': context.user_data["delivery_time"],
        'bunch_id': context.user_data["bunch_id"]
    }
    order = call_api_post('order/create/', payload=payload)
    context.user_data["order_id_delete"] = order['order_id']
    message_keyboard = [
        [
            "Все верно",
            "В заказе ошибка"],
    ]

    markup = ReplyKeyboardMarkup(
        message_keyboard,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    menu_msg = dedent(f"""\
                        <b>Вы выбрали букет №:</b>
                        {order['bunch_id']}
                        <b>Состав букета:</b>
                        {order['composition']}
                        <b>Описание:</b>
                        {order['description']}
                        <b>Название:</b>
                        {order['name']}
                        <b>Цена:</b>
                        {order['price']}
                        
                        <b>Адрес доставки:</b>
                        {context.user_data["address"]}
                        <b>Дата доставаки:</b>
                        {context.user_data["delivery_time"]}
                        <b>Телефон для связи:</b>
                        {context.user_data["phone_number"]}
                        """).replace("    ", "")

    bunch_img = requests.get(order['image'])
    update.message.reply_photo(
        bunch_img.content,
        caption=menu_msg,
        reply_markup=markup,
        parse_mode=ParseMode.HTML
    )
    return States.CONFIRM_ORDER


def order_confirmed(update, context):
    update.message.reply_text(
        'Спасибо за заказ, в ближайшее время курьер свяжется с вами')


def order_delete(update, context):
    payload = {
        'order_id': context.user_data["order_id_delete"],
    }
    answer = call_api_post('order/delete/', payload=payload)
    update.message.reply_text(answer['message'])
    return States.GET_NAME


if __name__ == '__main__':
    load_dotenv()
    tg_bot_token = os.getenv("TG_BOT_TOKEN")
    bot = Bot(token=tg_bot_token)
    updater = Updater(token=tg_bot_token, use_context=True)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", greeting)],
        states={
            States.START: [
                MessageHandler(
                    Filters.text("Флорист"), florist
                ),
                MessageHandler(
                    Filters.text("Заказ"), order
                ),
                MessageHandler(
                    Filters.text, start
                ),
            ],
            States.CHOISE_REASON: [
                MessageHandler(
                    Filters.text("Другой повод"), another_reason,
                ),
                MessageHandler(
                    Filters.text, choise_category
                ),
            ],
            States.MESSAGE_TO_COURIER: [
                MessageHandler(
                    Filters.text, send_orders_courier
                ),
            ],
            States.REASON_TO_FLORIST: [
                MessageHandler(
                    Filters.text, get_phonenumber
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
                ),
                MessageHandler(
                    Filters.text("Другой букет"), get_choice_bunch
                ),
                MessageHandler(
                    Filters.text("Все букеты"), show_all_bunches
                )
            ],
            States.GET_NAME: [
                MessageHandler(
                    Filters.text, get_name
                ),
            ],
            States.GET_BUNCH_ID: [
                MessageHandler(
                    Filters.text, get_bunch_id
                ),
            ],
            States.GET_ADDRESS: [
                MessageHandler(
                    Filters.text, get_address
                ),
            ],
            States.USER_PHONE_NUMBER: [
                MessageHandler(
                    Filters.text, get_user_phone_number
                ),
            ],
            States.GET_DELIVERY_PERIOD: [
                MessageHandler(
                    Filters.text, get_delivery_time
                ),
            ],
            States.CONFIRM_ORDER: [
                MessageHandler(
                    Filters.text("Все верно"), order_confirmed
                ),
                MessageHandler(
                    Filters.text("В заказе ошибка"), order_delete
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
