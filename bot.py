import sys
import time
import telepot
from telepot.loop import MessageLoop
import sqlite3


def send_to_all(playlist):
    try:
        connection = sqlite3.connect('db.sqlite3')
        sql = "SELECT * from users_registered;"
        cursor = connection.cursor()
        cursor.execute(sql)
        for id, chat_id in cursor.fetchall():
            bot.sendMessage(chat_id, playlist)
    except:
        pass


def unsubscribe(chat_id):
    try:
        connection = sqlite3.connect('db.sqlite3')
        sql1 = "SELECT * from users_registered;"
        cursor = connection.cursor()
        cursor.execute(sql1)
        for id, inscrito in cursor.fetchall():
            if int(inscrito) == int(chat_id):
                sql1 = "DELETE FROM users_registered WHERE chat_id = ('{}');".format(
                    chat_id)
                cursor = connection.cursor()
                cursor.execute(sql1)
                connection.commit()
                bot.sendMessage(chat_id, "Incrição cancelada")
                return
        bot.sendMessage(chat_id, 'Você não estava inscrito')
    except:
        bot.sendMessage(chat_id, 'falha ao remover inscrição')


def subscribe(chat_id):
    try:
        connection = sqlite3.connect('db.sqlite3')
        sql1 = "SELECT * from users_registered;"
        cursor = connection.cursor()
        cursor.execute(sql1)
        for id, inscrito in cursor.fetchall():
            if int(inscrito) == int(chat_id):
                bot.sendMessage(chat_id, "Ja esta inscrito")
                return
        sql = "INSERT INTO users_registered (chat_id) VALUES ('{}');".format(
            chat_id)
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        bot.sendMessage(chat_id, 'cadastrado com sucesso')
    except:
        bot.sendMessage(chat_id, 'falha ao se cadastrar')


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if msg['text'] == '/start' or msg['text'] == '/help':
        bot.sendMessage(chat_id, "Esse bot permite o compartilhamento de playlist através de uma aplicação django. Para se inscrever e receber dicas de playlist digite '/subscribe' para remover a inscrição '/unsubscribe'")
    elif msg['text'] == '/subscribe':
        subscribe(chat_id)
    elif msg['text'] == '/unsubscribe':
        unsubscribe(chat_id)
    else:
        bot.sendMessage(
            chat_id, 'fui mal programado, não sei o que você quer')


# TOKEN = sys.argv[1]  # get token from command-line

bot = telepot.Bot('864031082:AAFjeEoTiaUjOLn3nz07iu6pnkfZ_KQE3Js')
MessageLoop(bot, handle).run_as_thread()
print('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)
