import os
import requests
import pprint
import phonenumbers

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
from time import sleep


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

class BotData:
    frorist_chat_id = 704859099
    courier_chat_id = 704859099
    # frorist_chat_id = 5432002795
    # courier_chat_id = 5432002795

# TODO сделать использование этой функции во всех запросах
# TODO пройтись по боту и посмотреть чтобы везде были кнопки назад или оформить заказ, чтобы клиент не оставался без кнопки
# TODO рассказать Максу как сделать чтобы бот отправлял сообщения в другой чат или бота, а то просто смена chat_id не решает задачу


def call_api(endpoint):
    url = f"http://127.0.0.1:8000/{endpoint}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def start(update, context):
    categories = call_api('reasons/send/')['reasons']
    context.user_data['reasons'] = categories
    categories.extend(["Без повода", "Другой повод", "Курьер"])    
    message_keyboard = list(chunked(categories, 2))   
    greeting_msg = '''Закажите доставку праздничного букета, 
собранного специально для ваших любимых, родных и коллег.
Наш букет со смыслом станет главным подарком на вашем празднике!'''     
    update.message.reply_text(text=greeting_msg, )
    sleep(2)
    markup = ReplyKeyboardMarkup(
        message_keyboard,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    menu_msg = 'К какому событию готовимся? Выберите один из вариантов, либо укажите свой'
    
    update.message.reply_text(text=menu_msg, reply_markup=markup)
    return States.CHOISE_REASON


def start_over(update, context):
    categories = call_api('reasons/send/')['reasons']
    context.user_data['reasons'] = categories
    categories.extend(["Без повода", "Другой повод", "Курьер"])    
    message_keyboard = list(chunked(categories, 2))      
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

    update.message.chat.id = BotData.frorist_chat_id
    menu_msg = dedent(f"""\
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

# TODO сделать чтобы курьер не видел меню для клиента, а клиент не видел курьера
def courier(update, context):
    update.message.reply_text('Напишите дату на которую хотите посмотреть заказы в формате YYYY-MM-DD')
    return States.MESSAGE_TO_COURIER


def send_orders_courier(update, context):
    url = f"http://127.0.0.1:8000/courier/send/"
    payload = {
        "delivered_at": update.message.text,
    }
    response = requests.post(url, data=payload)
    response.raise_for_status()
    pprint(response.json())
    # TODO взять инфу с джейсона и прислать курьеру заказы
    return


def choise_category(update, context):
    url = f"http://127.0.0.1:8000/categories/send/"
    response = requests.get(url)
    categories = response.json()['categories']
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
    url = "http://127.0.0.1:8000/bunch/send/"
    response = requests.post(url, data=payload)
    if random_category:
        url = "http://127.0.0.1:8000/random_bunch/send/"
        response = requests.post(url)
    response.raise_for_status()
    return  response





def get_bunch(update, context):
    context.user_data['category'] = update.message.text
    response = get_answer_from_catalogue(context)
    if response.ok:
        bunches = response.json()        
        if not bunches['bunch']:
            get_default_bunch(update, context)
            return States.START
        context.user_data['bunches'] = bunches
        get_choice_bunch(update, context)           
    else:
        update.message.reply_text('Ошибка соединения, начните поиск сначала 😥')
        return States.CHOISE_CATEGORY
    return States.CHOISE_PEOPLE


def get_default_bunch(update, context):

    update.message.reply_text('Букета по критериям нет😥, выводится случайный букет')    
    url = "http://127.0.0.1:8000/random_bunch/send/"
    response = requests.get(url)
    print(response)
    bunch = response.json()['bunch']
    print(bunch)
    menu_msg = get_menu_msg(bunch)
    context.user_data["order"] = menu_msg
    message_keyboard = [
                [
                    "Флорист",
                    "Заказ"],
                [   "Задать другие параметры"],
                #    "Все букеты"]
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
                [    "Другой букет",
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
        'В какой день и в какое время желаете получить доставку. Напишите дату в формате YYYY-MM-DD HH:MM')
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

    # TODO сначала отправляем запрос и создаем объект и все сообщения подтверждения заказа уже берем из джейона

    url = f"http://127.0.0.1:8000/order/create/"
    payload = {
        'firstname': context.user_data["user_name"],
        'address': context.user_data["address"],
        'phonenumber': context.user_data["phone_number"],
        'delivered_at': context.user_data["delivery_time"],
        'bunch_id': context.user_data["bunch_id"]
    }
    response = requests.post(url, data=payload)
    pprint(response.json())
    # TODO из джейсона отправить клиенту описание его заказа, фото и описание его букета, если данные некорректные,
    # TODO то status false значит надо писать сообщение из джейсона про некорректные данные и давать кнопку начать с ввода имени
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
            States.START: [
                MessageHandler(
                    Filters.text, start_over
                ),        
            ],
            States.CHOISE_REASON: [
                MessageHandler(
                    Filters.text("Другой повод"), another_reason,
                ),
                MessageHandler(
                    Filters.text("Курьер"), courier
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

        },
        fallbacks=[],
        allow_reentry=True,
        name='bot_conversation',
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()
