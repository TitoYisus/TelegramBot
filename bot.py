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

    bot.send_message(chat_id=cid, text="Envíame un csv (con caption '/s') separado por punto y coma (;) " + 
                     "con los recordatorios definidos en las siguientes columnas:\n\n1. \"fecha\": " +
                     "Fecha en la que recordar (formato DD/MM/YYYY)\n2. \"mensaje\": mensaje que " +
                     "quieras que se envíe\n3. \"user\": usuarios a los que mencionar separados por " +
                     "comas [OPCIONAL]\n\t(p.ej. alice, bob)\n\n PREGUNTA A ALGUIEN POR EL GRUPO " +
                     "SI TIENES ALGUNA DUDA")
    
    local_photo_path = './files/ejemplo.jpg'
    mensajito = "ejemplo de excel antes de guardarlo como csv"
    bot.send_photo(chat_id=cid, photo=open(local_photo_path, 'rb'), caption=mensajito)

@bot.message_handler(func=lambda message: message.document.mime_type == 'text/csv', content_types=['document'])
def descargar_archivo(message):
    cid = message.chat.id
    archivo = message.document
    nombre = archivo.file_name
    id_archivo = archivo.file_id
    bot.reply_to(message, "Descargando " + nombre + "...")
    file_link = bot.get_file_url(id_archivo)
    print(file_link)
    descarga = bot.get_file(id_archivo)
    print(descarga)
    descarga.download(custom_path="./files/recordatorios.csv")
    





'''
@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, message.text)
'''

bot.infinity_polling()