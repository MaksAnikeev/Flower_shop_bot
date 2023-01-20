import os
from telegram import (Update, Bot, InlineKeyboardMarkup, InlineKeyboardButton,
                      KeyboardButton, ReplyKeyboardMarkup)
from telegram.ext import (CallbackQueryHandler, CommandHandler, Filters,
                          MessageHandler, Updater, ConversationHandler)
from dotenv import load_dotenv
import requests
from textwrap import dedent


FIRST, SECOND, THIRD = range(3)

def main():

    load_dotenv()
    tg_bot_token = os.getenv('TG_BOT_TOKEN')
    bot = Bot(token=tg_bot_token)

    reasons_menu_keyboard = ['День рождения', 'Свадьба', 'В школу',
                        'Без повода', 'Другой повод', 'Выход']
    #get_reasons_menu_keyboard()
    categories_menu_keyboard =  ['~500', '~1000', '~2000',
                        'больше', 'Не важно', 'Назад']
    #get_categories_menu_keyboard()

    updater = Updater(token=tg_bot_token, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    choice_handler = MessageHandler(Filters.text(reasons_menu_keyboard[:-2]), choice_button)
    dispatcher.add_handler(choice_handler)

    start_over_handler = MessageHandler(Filters.text("Назад"), start_over)
    dispatcher.add_handler(start_over_handler)

    get_bunch_handler = MessageHandler(Filters.text(categories_menu_keyboard[:-1]), get_bunch)
    dispatcher.add_handler(get_bunch_handler)

    # get_another_reason_handler = MessageHandler(Filters.text(reasons_menu_keyboard[-1]), get_another_reason)
    # dispatcher.add_handler(get_another_reason_handler)



    updater.start_polling()
    updater.idle()

def get_reasons_menu_keyboard():

    url = f"http://127.0.0.1:8000/reasons/send/"
    response = requests.get(url)
    print(response)
    categories = response.json()['reasons']
    keyboard_caption = list(categories)     
    return keyboard_caption

def get_categories_menu_keyboard():

    url = f"http://127.0.0.1:8000/categories/send/"
    response = requests.get(url)
    print(response)
    categories = response.json()['categories']
    keyboard_caption = list(categories) 
    return keyboard_caption


def build_menu(buttons, n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu


def start(update, context):
    
    reasons_menu_keyboard = ['День рождения', 'Свадьба', 'В школу',
                        'Без повода', 'Другой повод', 'Выход']
    #get_reasons_menu_keyboard()
    keyboard = [KeyboardButton(key) for key in reasons_menu_keyboard]
    
    reply_markup =  ReplyKeyboardMarkup(build_menu(keyboard, n_cols=2), one_time_keyboard=True)    
    update.message.reply_text(
            'К какому событию готовимся? Выберите один из вариантов, либо укажите свой:', 
            reply_markup=reply_markup
            )
    

def start_over(update, context):

    reasons_menu_keyboard = ['День рождения', 'Свадьба', 'В школу',
                        'Без повода', 'Другой повод', 'Выход']
    #get_reasons_menu_keyboard()
    keyboard = [KeyboardButton(key) for key in reasons_menu_keyboard]
    
    reply_markup =  ReplyKeyboardMarkup(build_menu(keyboard, n_cols=2), one_time_keyboard=True)    
   
    update.message.reply_text(
        text="Выберите событие", reply_markup=reply_markup
    )
    


def choice_button(update, context):
        
    categories_menu_keyboard = ['~500', '~1000', '~2000',
                        'больше', 'Не важно', 'Назад']
    #get_categories_menu_keyboard()
    keyboard = [KeyboardButton(key) for key in categories_menu_keyboard]
    
    reply_markup =  ReplyKeyboardMarkup(build_menu(keyboard, n_cols=2), one_time_keyboard=True)
    context.user_data['reason'] = update.message.text.title()   
    update.message.reply_text(
            text=f"На какую сумму рассчитываете?", reply_markup=reply_markup
            )


# def get_another_reason():
#
#     keyboard = ['Да']
#     update.message.reply_text(text='Другая причина')
    
def get_bunch(update, context):
    url = f"http://127.0.0.1:8000/bunch/send/"
    context.user_data['category'] = update.message.text.title() 
    payload = {
        "category": context.user_data['category'],
        "reason": context.user_data['reason'],
    }
    print(payload)
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


def end_conversation(update, _):
    
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Приходите ещё")
    return ConversationHandler.END


if __name__ == '__main__':
    main()
    