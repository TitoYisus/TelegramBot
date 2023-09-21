import os
import telebot
from dotenv import load_dotenv
import json

load_dotenv()

BOT_TOKEN = os.environ.get('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Qué pasa, pisha?")

@bot.message_handler(commands=['ayuda'])
def send_help(message):
    bot.reply_to(message, "")

@bot.message_handler(commands=['anadir'])
def add_dates(message):
    cid = message.chat.id
    nombre = message.chat.title
    bot.send_message(chat_id=cid, text=nombre)






'''
@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, message.text)
'''

bot.infinity_polling()