import schedule
import requests
from bs4 import BeautifulSoup as BS

CHAT_IDS = []
TOKEN = ""
counter = 0

########## users ni id lari olingan qismi ###########
from database import Database
db = Database("namoz_db.db")
db_users = db.get_user_by_id()
for user_id in db_users:
    CHAT_IDS.append(user_id['user_id'])
# print(CHAT_IDS)
#####################################################


# url = "https://dailyprayer.abdulrcs.repl.co/api/tashkent"
# response = requests.get(url)
# data = response.json()
# today = data['today']

region = requests.get(f'https://islom.uz/')
html_t = BS(region.content, 'html.parser')

Namoz_time = []
# Namoz_text = []

for i in range(len(html_t.select('.p_clock'))):
    time = html_t.select('.p_clock b')
    Namoz_time.append(time[i].text)
    # text = html_t.select('.p_v')
    # Namoz_text.append(text[i].text)

# print(Namoz_time)
# print(Namoz_text)
p_title = html_t.select('.title_prayer')[0].text

def send_text(token:str, chat_id_list: list, text: str):
    for chat_id in chat_id_list:
        requests.post(
            url=f'https://api.telegram.org/bot{token}/sendMessage',
            data={'chat_id': chat_id, 'text': text}
        )



def bomdod():
    global counter
    send_text(TOKEN, CHAT_IDS, f"🕋 Soat: {Namoz_time[0]}, Bomdod vaqti bo'ldi!")
    counter += 1
    # print("ids:", CHAT_IDS, "Type:", type(CHAT_IDS))

def quyosh():
    global counter
    send_text(TOKEN, CHAT_IDS, f"🕋 Soat: {Namoz_time[1]}, Quyosh vaqti bo'ldi!")
    counter += 1


def peshin():
    global counter
    send_text(TOKEN, CHAT_IDS, f"🕋 Soat: {Namoz_time[2]}, Peshin vaqti bo'ldi!")
    counter += 1


def asr():
    global counter
    send_text(TOKEN, CHAT_IDS, f"🕋 Soat: {Namoz_time[3]}, Asr vaqti bo'ldi!")
    counter += 1


def shom():
    global counter
    send_text(TOKEN, CHAT_IDS, f"🕋 Soat: {Namoz_time[4]}, Shom vaqti bo'ldi!")
    counter += 1


def xufton():
    global counter
    send_text(TOKEN, CHAT_IDS, f"🕋 Soat: {Namoz_time[5]}, Xufton vaqti bo'ldi!")
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

# set_namoz_time(b=today['Sunrise'], p=today['Dhuhr'], a=today['Asr'], sh=today['Maghrib'], x=today["Isha'a"])
# set_namoz_time(b='22:55', q='22:56', p='19:45', a='15:59', sh='15:47', x='15:48')

set_namoz_time(b = Namoz_time[0], q = Namoz_time[1], p = Namoz_time[2], a = Namoz_time[3], sh = Namoz_time[4], x = Namoz_time[5])