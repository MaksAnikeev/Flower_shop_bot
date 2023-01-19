import os
from telegram import (Update, Bot, InlineKeyboardMarkup, InlineKeyboardButton,
                      KeyboardButton, ReplyKeyboardMarkup)
from telegram.ext import (CallbackQueryHandler, CommandHandler, Filters,
                          MessageHandler, Updater, ConversationHandler)
from dotenv import load_dotenv

FIRST, SECOND, THIRD = range(3)

def main():

    load_dotenv()
    tg_bot_token = os.getenv('TG_BOT_TOKEN')
    bot = Bot(token=tg_bot_token)
    updater = Updater(token=tg_bot_token, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    choice_handler = MessageHandler(Filters.text(["День рождения", 'Свадьба', 'В школу',
                        'Без повода', 'Другой повод']), choice_button)
    dispatcher.add_handler(choice_handler)

    start_over_handler = MessageHandler(Filters.text("Назад"), start_over)
    dispatcher.add_handler(start_over_handler)

    updater.start_polling()
    updater.idle()

def get_caption_menu_keyboard(caption_kind=1):

    if caption_kind:
       keyboard_caption = ['День рождения', 'Свадьба', 'В школу',
                        'Без повода', 'Другой повод', 'Выход']
    else:
       keyboard_caption = ['~500', '~1000', '~2000',
                        'больше', 'Не важно', 'Назад'] 
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
    
    keyboard_caption = get_caption_menu_keyboard(1)
    keyboard = [KeyboardButton(key) for key in keyboard_caption]
    
    reply_markup =  ReplyKeyboardMarkup(build_menu(keyboard, n_cols=2), one_time_keyboard=True)    
    update.message.reply_text(
            'К какому событию готовимся? Выберите один из вариантов, либо укажите свой:', 
            reply_markup=reply_markup
            )
    

def start_over(update, _):

    #query = update.callback_query
    keyboard_caption = get_caption_menu_keyboard(1)
    keyboard = [KeyboardButton(key) for key in keyboard_caption]
    
    reply_markup =  ReplyKeyboardMarkup(build_menu(keyboard, n_cols=2), one_time_keyboard=True)    
   
    update.message.reply_text(
        text="Выберите событие", reply_markup=reply_markup
    )
    

#def choice_birtday(update, _):



def choice_button(update, context):
    #query = update.callback_query
    #variant = query.data  
    #query.answer() 
    
    keyboard_caption = get_caption_menu_keyboard(0)
    keyboard = [KeyboardButton(key) for key in keyboard_caption]
    
    reply_markup =  ReplyKeyboardMarkup(build_menu(keyboard, n_cols=2), one_time_keyboard=True)
    event = update.message.text.title()   
    update.message.reply_text(
            text=f"{event}  На какую сумму рассчитываете?", reply_markup=reply_markup
            )
    return SECOND


def end_conversation(update, _):
    
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Приходите ещё")
    return ConversationHandler.END


if __name__ == '__main__':
    main()
    