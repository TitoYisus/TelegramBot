import os
import telebot
import json
from dotenv import load_dotenv
from datetime import date, datetime, timedelta

load_dotenv()

BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

today = date.today()
cid = -1001882486742
aviso = "*IMPORTANTE*\n\nToca extender la expiración en PythonAnywhere si queréis que esto siga funcionando"

def manda_mensaje():
    #bot.send_message(cid, text="esto es una prueba de recordatorio")

    file_path = "./files/reminders.json"
    with open(file_path, 'r') as f:
        recordatorios = json.load(f)
        k,v = list(recordatorios.items())[0]
        fecha = datetime.strptime(k, "%d/%m/%Y").date()
        
        if fecha == today:
            for r in v:
                mensaje = r[1]
                usuarios = r[2]
                users = ""
                for u in usuarios:
                    users = users + "@"+u + " "
                texto = users + "\n\n" + mensaje
                bot.send_message(cid, texto)
            del recordatorios[k]
        
        else:
            texto = "No hay ningún recordatorio para hoy. Espero que tengáis un gran día! <3"
            bot.send_message(cid, texto)
    
    with open(file_path, 'w') as f:
        json.dump(recordatorios, f)

    return

def comprueba_fecha_task():
    '''
    AVISAR DEL EXPIRY EL 1 Y EL 17 DE CADA MES
    '''
    dia = today.day
    print(dia)
    if dia==1 or dia==17:
        bot.send_message(cid, aviso, parse_mode='Markdown')
    return



def main():
    manda_mensaje()
    comprueba_fecha_task()

if __name__ == '__main__':
    main()
