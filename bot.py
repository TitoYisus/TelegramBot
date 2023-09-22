# -*- coding: utf-8 -*-

import os
import telebot
import requests
import json
import csv
from dotenv import load_dotenv
from collections import namedtuple
from datetime import date, datetime

load_dotenv()
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)


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
                     "comas sin espacios [OPCIONAL]\n\nAsegúrate de guardarlo como CSV UTF-8\n\n" +
                     "PREGUNTA A ALGUIEN POR EL GRUPO SI TIENES ALGUNA DUDA")
    
    local_photo_path = './files/ejemplo.jpg'
    mensajito = "ejemplo de excel antes de guardarlo como csv"
    bot.send_photo(chat_id=cid, photo=open(local_photo_path, 'rb'), caption=mensajito)
    local_photo_path = './files/tipo_csv.jpg'
    mensajito = "opción de tipo que seleccionar en \"guardar como\""
    bot.send_photo(chat_id=cid, photo=open(local_photo_path, 'rb'), caption=mensajito)

@bot.message_handler(func=lambda message: message.document.mime_type == 'text/csv', content_types=['document'])
def actualizar(message):
    if message.caption == "/s":
        descargar_csv(message)
        diccionario = parse_recordatorios(message)
        actualizar_json(message, diccionario)
    else:
        bot.reply_to(message, "Veo que has mandado un .csv, si quieres que me lo descargue " +
                     "actualizar los recordatorios asegúrate de ponerle el comando '/s' como caption")

def descargar_csv(message):
    cid = message.chat.id
    nombre = message.document.file_name
    bot.reply_to(message, "Descargando " + nombre + "...")
    
    id_archivo = message.document.file_id
    file_link = bot.get_file_url(id_archivo)

    file_path = "./files/recordatorios.csv"
    response = requests.get(file_link)
    with open(file_path, 'wb') as recordatorios:
        recordatorios.write(response.content)

def parse_recordatorios(message):
    cid = message.chat.id
    bot.send_message(chat_id=cid, text="Descarga finalizada. Parseando datos...")

    file_path = "./files/recordatorios.csv"
    recordatorios = []
    with open(file_path, encoding='utf-8') as fichero:
        lector = csv.reader(fichero, delimiter=';')
        next(lector)
        for linea in lector:
            fecha_hoy = date.today()
            fecha_r = datetime.strptime(linea[0], "%d/%m/%Y").date()
            if fecha_hoy < fecha_r:
                fecha = linea[0]
                texto = linea[1]
                usuarios = parsea_usuarios(linea[2])

                tupla = (fecha, texto, usuarios)
                recordatorios.append(tupla)
    
    res = ordena_por_fecha(recordatorios)
    return res

def parsea_usuarios(usuarios):
    lista_usuarios = usuarios.split(",")
    return lista_usuarios

def ordena_por_fecha(recordatorios):
    res = dict()
    for r in recordatorios:
        if r[0] not in res:
            lista = []
            lista.append(r)
            res[r[0]] = lista
        else:
            res[r[0]].append(r)
    return res

def actualizar_json(message, recordatorios):
    cid = message.chat.id
    bot.send_message(chat_id=cid, text="Parseo finalizado. Actualizando recordatorios...")

    file_path = "./files/reminders.json"
    with open(file_path, 'r') as f:
        res = json.load(f)
        for key, value in recordatorios.items():
            if key not in res:
                res[key] = value
            else:
                lista = list(value[0])
                if lista not in res[key]:
                    res[key].extend(value)
    
    claves = list(res.keys())
    fechas = []
    for c in claves:
        fechas.append(datetime.strptime(c, "%d/%m/%Y").date())
    fechas.sort()
    claves = []
    for f in fechas:
        claves.append(f.strftime("%d/%m/%Y"))
    res2 = {i:res[i] for i in claves}
    
    with open(file_path, 'w') as f:
        json.dump(res2, f)
    
    bot.send_message(chat_id=cid, text="Todos los recordatorios actualizados. Espero que tengas un día estupendo <3")
    return


bot.infinity_polling()