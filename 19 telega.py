from telegram import Update, Bot, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from credits import bot_token

bot = Bot(bot_token)
updater = Updater(bot_token, use_context=True)
dispatcher = updater.dispatcher


def start(update, context):
    context.bot.send_message(update.effective_chat.id, text='Привет я школьный дневник')


def info(update, context):
    context.bot.send_message(update.effective_chat.id,
                             text="Лишь попроси бота, и он поможет тебе с расписанием и некоторыми предметами!")


def get_day(update, context):
    keyboard = [
        [InlineKeyboardButton('Понедельник', callback_data='1'), InlineKeyboardButton('Вторник', callback_data='2')],
        [InlineKeyboardButton('Среда', callback_data='3'), InlineKeyboardButton('Четверг', callback_data='4')],
        [InlineKeyboardButton('Пятница', callback_data='5'), InlineKeyboardButton('Суббота', callback_data='6')],
        [InlineKeyboardButton('Воскресенье', callback_data='7')]
    ]
    update.message.reply_text('Выбери день', reply_markup=InlineKeyboardMarkup(keyboard))


def leters(update, context):
    keyboard = [
        [InlineKeyboardButton('Русский', callback_data='8'), InlineKeyboardButton('Математика', callback_data='9'),
         InlineKeyboardButton('Литература', callback_data='10')]
    ]
    update.message.reply_text('Выбери урок', reply_markup=InlineKeyboardMarkup(keyboard))


def open_file(name):
    a = open(name, 'r', encoding='utf-8')
    data = a.read()
    a.close()
    return data

def opens(name):
    a = open(name, 'r')
    data = a.read()
    a.close()
    return data


def button(update, context):
    q = update.callback_query
    q.answer()
    if q.data == '1':
        context.bot.send_message(update.effective_chat.id, open_file('mon.txt'))
    elif q.data == '2':
        context.bot.send_message(update.effective_chat.id, open_file('thu.txt'))
    elif q.data == '3':
        context.bot.send_message(update.effective_chat.id, open_file('tue.txt'))
    elif q.data == '8':
        context.bot.send_message(update.effective_chat.id, open_file('rus.txt'))
    elif q.data == '9':
        context.bot.send_message(update.effective_chat.id, open_file('math.txt'))
    elif q.data == '10':
        context.bot.send_message(update.effective_chat.id, open_file('lit.txt'))


def wall(update, context):
    file = open('wall.txt', 'a')
    user_name = str(update.message.from_user['first_name']) + '' + str(update.message.from_user['last_name'])
    result = ''
    for arg in context.args:
        result += arg + ' '
    file.write(user_name + ':' + result + '\n')
    file.close()


def show_wall(update, context):
    context.bot.send_message(update.effective_chat.id, opens('wall.txt'))

def wall_individual(update, context):
    user_name = str(update.message.from_user['first_name']) + '' + str(update.message.from_user['last_name'])
    file = open(str(user_name) + '.txt', 'a')
    result = ''
    for arg in context.args:
        result += arg + ' '
    file.write(user_name + ':' + result + '\n')
    file.close()


def show_wall_individual(update, context):
    user_name = str(update.message.from_user['first_name']) + '' + str(update.message.from_user['last_name'])
    context.bot.send_message(update.effective_chat.id, opens(str(user_name) + '.txt'))

start_handler = CommandHandler('start', start)
info_handler = CommandHandler('info', info)
get_day_handler = CommandHandler('getday', get_day)
leters_handler = CommandHandler('leters',leters)
button_handler = CallbackQueryHandler(button)
wall_handler = CommandHandler('wall', wall)
wall_individual_handler = CommandHandler('wallind', wall_individual)
show_wall_handler = CommandHandler('show', show_wall)
show_wall_individual_handler = CommandHandler('showind', show_wall_individual)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(info_handler)
dispatcher.add_handler(get_day_handler)
dispatcher.add_handler(leters_handler)
dispatcher.add_handler(button_handler)
dispatcher.add_handler(wall_handler)
dispatcher.add_handler(wall_individual_handler)
dispatcher.add_handler(show_wall_individual_handler)

updater.start_polling()
updater.idle()
