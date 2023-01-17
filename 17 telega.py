from telegram import Update, Bot
from telegram.ext import  Updater, CommandHandler, MessageHandler, Filters
from credits import bot_token
import random

bot = Bot(bot_token)
updater = Updater(bot_token, use_context=True)
dispatcher = updater.dispatcher

list = ['Я тебя люблю', 'Ты мое сокровище', 'Я тебя обожаю', 'Счастье ты мое', 'Мир прекрасен когда я рядом с тобой']
dictionary = {"яблоко": "apple", "груша": "pear",'розовый':'pink','желтый':'yellow','мороженое':'ice cream'}

def start(update, context):
    context.bot.send_message(update.effective_chat.id, 'Привет')

def info(update, context):
    context.bot.send_message(update.effective_chat.id, 'Создатель бота Аникеев Максим, программист от бога')

def love_message(update, context):
    a = random.randint(0,4)
    context.bot.send_message(update.effective_chat.id, text = list[a])

def message(update, context):
    a = update.message.text
    if a == 'Любимый':
        context.bot.send_message(update.effective_chat.id, 'Твой любимый - это бесконечно тебя любящий создатель этого бота Аникеев Максим, твой верный муж')
    elif a in dictionary.keys() or a in dictionary.values():
        for key, i in dictionary.items():
            if a == key:
                context.bot.send_message(update.effective_chat.id,i)
            elif a == i:
                context.bot.send_message(update.effective_chat.id, key)
    else:
        context.bot.send_message(update.effective_chat.id, 'я пока не знаю таких слов')

def unknown_command(update, context):
    context.bot.send_message(update.effective_chat.id, 'эта команда мне не известна')


start_handler = CommandHandler('start', start)
info_handler = CommandHandler('info', info)
love_message_handler = CommandHandler('lovemessage', love_message)
unknown_command_handler = MessageHandler(Filters.command, unknown_command)
message_handler = MessageHandler(Filters.text, message)



dispatcher.add_handler(info_handler)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(love_message_handler)
dispatcher.add_handler(unknown_command_handler)
dispatcher.add_handler(message_handler)



updater.start_polling()
updater.idle()
