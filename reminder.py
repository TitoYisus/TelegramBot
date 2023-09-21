import os
import telebot
from dotenv import load_dotenv
from datetime import date

load_dotenv()

BOT_TOKEN = os.environ.get('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)

today = date.today()
dia = str(today.day)
mes = str(today.month)



@bot.message_handler(commands=['anadir'])
def add_dates(message):
    bot.send_message(chat_id="-1001882486742", text="prueba")



bot.infinity_polling()