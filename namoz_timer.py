import schedule
import requests
from bs4 import BeautifulSoup as BS

CHAT_IDS = []
TOKEN = "5560382012:AAFrRvuazQQGiC23ch0vT94v4u4KPLry254"
counter = 0

########## users ni id lari olingan qismi ###########
from database import Database
db = Database("namoz_db.db")
db_users = db.get_user_by_id()
for user_id in db_users:
    CHAT_IDS.append(user_id['user_id'])
#####################################################

region = requests.get(f'https://islom.uz/')
html_t = BS(region.content, 'html.parser')

Namoz_time = []

for i in range(len(html_t.select('.p_clock'))):
    time = html_t.select('.p_clock b')
    Namoz_time.append(time[i].text)

p_title = html_t.select('.title_prayer')[0].text

def send_text(token:str, chat_id_list: list, text: str):
    for chat_id in chat_id_list:
        requests.post(
            url=f'https://api.telegram.org/bot{token}/sendMessage',
            data={'chat_id': chat_id, 'text': text}
        )



def bomdod():
    global counter
    send_text(TOKEN, CHAT_IDS, f"🕋 🕘: {Namoz_time[0]}, Bomdod Namoz vaqti bo'ldi! 🤲")
    counter += 1

def quyosh():
    global counter
    send_text(TOKEN, CHAT_IDS, f"🕋 🕝: {Namoz_time[1]}, Quyosh vaqti bo'ldi! 🤲")
    counter += 1


def peshin():
    global counter
    send_text(TOKEN, CHAT_IDS, f"🕋 🕖: {Namoz_time[2]}, Peshin Namoz vaqti bo'ldi! 🤲")
    counter += 1


def asr():
    global counter
    send_text(TOKEN, CHAT_IDS, f"🕋 🕣: {Namoz_time[3]}, Asr Namoz vaqti bo'ldi! 🤲")
    counter += 1


def shom():
    global counter
    send_text(TOKEN, CHAT_IDS, f"🕋 🕒: {Namoz_time[4]}, Shom Namoz vaqti bo'ldi! 🤲")
    counter += 1


def xufton():
    global counter
    send_text(TOKEN, CHAT_IDS, f"🕋 🕔: {Namoz_time[5]}, Xufton Namoz vaqti bo'ldi! 🤲")
    counter += 1


def set_namoz_time(b, q, p, a, sh, x):
    schedule.every().day.at(b).do(bomdod)
    schedule.every().day.at(q).do(quyosh)
    schedule.every().day.at(p).do(peshin)
    schedule.every().day.at(a).do(asr)
    schedule.every().day.at(sh).do(shom)
    schedule.every().day.at(x).do(xufton)

    while counter < 6:
        schedule.run_pending()

set_namoz_time(b = Namoz_time[0], q = Namoz_time[1], p = Namoz_time[2], a = Namoz_time[3], sh = Namoz_time[4], x = Namoz_time[5])