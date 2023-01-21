import os
from telegram import Update, Bot, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (CallbackQueryHandler, CommandHandler, Filters,
                          MessageHandler, Updater)
from dotenv import load_dotenv
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
import requests
from textwrap import dedent
from enum import Enum, auto


class States(Enum):
    CHOISE_REASON = auto()
    CHOISE_CATEGORY = auto()
    CHOISE_PEOPLE = auto()
>>>>>>> Stashed changes

def main():
    load_dotenv()
    tg_bot_token = os.getenv("TG_BOT_TOKEN")
    bot = Bot(token=tg_bot_token)
    updater = Updater(token=tg_bot_token, use_context=True)
<<<<<<< Updated upstream
    app = updater.dispatcher
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(CommandHandler('help', help_command))
=======
=======
>>>>>>> Stashed changes
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    choice_handler = MessageHandler(Filters.text(reasons_menu_keyboard[:-2]), choice_button)
    dispatcher.add_handler(choice_handler)

    start_over_handler = MessageHandler(Filters.text("Назад"), start_over)
    dispatcher.add_handler(start_over_handler)

    get_bunch_handler = MessageHandler(Filters.text(categories_menu_keyboard[:-1]), get_bunch)
    dispatcher.add_handler(get_bunch_handler)

    get_another_reason_handler = MessageHandler(Filters.text('Другой повод'), get_another_reason)
    dispatcher.add_handler(get_another_reason_handler)
<<<<<<< Updated upstream


=======
>>>>>>> Stashed changes

>>>>>>> Stashed changes
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
    
<<<<<<< Updated upstream
    reply_markup = InlineKeyboardMarkup(keyboard)    
    update.message.reply_text('К какому событию готовимся? Выберите один из вариантов, либо укажите свой:', reply_markup=reply_markup)
    
=======
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

    reply_markup = InlineKeyboardMarkup(keyboard)    
    update.message.reply_text('К какому событию готовимся? Выберите один из вариантов, либо укажите свой:', reply_markup=reply_markup)
    
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
            text="На какую сумму рассчитываете?", reply_markup=reply_markup
            )


def get_another_reason(update, context):

    #keyboard = ['Сохранить', 'Отмена']
    #reply_markup =  ReplyKeyboardMarkup(build_menu(keyboard, n_cols=2), 
      #  resize_keyboard=True)
    update.message.reply_text(text='Введите Ваш повод')
   # reply = update.message.text.title()
   # if reply == keyboard[0]:
    context.user_data['reason'] = update.message.text()
    update.message.reply_text(context.user_data['reason'])


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

def choice_button(update, context):
        
    categories_menu_keyboard = ['~500', '~1000', '~2000',
                        'больше', 'Не важно', 'Назад']
    #get_categories_menu_keyboard()
    keyboard = [KeyboardButton(key) for key in categories_menu_keyboard]
    
    reply_markup =  ReplyKeyboardMarkup(build_menu(keyboard, n_cols=2), one_time_keyboard=True)
    context.user_data['reason'] = update.message.text.title()   
    update.message.reply_text(
            text="На какую сумму рассчитываете?", reply_markup=reply_markup
            )


def get_another_reason(update, context):

    #keyboard = ['Сохранить', 'Отмена']
    #reply_markup =  ReplyKeyboardMarkup(build_menu(keyboard, n_cols=2), 
      #  resize_keyboard=True)
    update.message.reply_text(text='Введите Ваш повод')
   # reply = update.message.text.title()
   # if reply == keyboard[0]:
    context.user_data['reason'] = update.message.text()
    update.message.reply_text(context.user_data['reason'])


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
>>>>>>> Stashed changes


def button(update, context):
    query = update.callback_query
    variant = query.data    
    query.answer()    
    query.edit_message_text(text=f"Выбранный вариант: {variant}")


def help_command(update, context):
    update.message.reply_text("Используйте `/start` для тестирования.")
    

if __name__ == '__main__':
    main()