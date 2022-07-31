from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import BotCommand, KeyboardButton, ReplyKeyboardMarkup, ChatAction, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
import os
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from namoz_haqida import text

ADMIN_ID = 696959110
# TOKEN = "5560382012:AAFrRvuazQQGiC23ch0vT94v4u4KPLry254"
TOKEN = "5358957794:AAGjOAwGD1cAsFTD470LsbypxhsqjMv4DSM"
from database import Database
db = Database("namoz_db.db")
count = 0

def job():
    os.system('python namoz_timer.py')

scheduler = BackgroundScheduler()
trigger = CronTrigger(
    year="2022", month="07", day="31", hour="07", minute="03", second="50"
)
scheduler.add_job(job, trigger=trigger)
scheduler.start()
# scheduler.shutdown()

def start_command(update, context):
    global count
    buttons = [
           [KeyboardButton(text="🕋 Namoz haqida ma'lumot")],
       ]
    user = update.message.from_user
    db_user = db.get_user_by_chat_id(user.id)
    if not db_user:
        db.create_user(user.id)
        # print(user_info)
        # command_list = [
        #     BotCommand(command="start", description="botni ishga tushirish"),
        #     BotCommand(command="info", description="bot haqida ma'lumot"),
        # ]
        # context.bot.set_my_commands(commands=command_list)
        update.message.reply_text(text=f"🕋 Assalomu alaykum {update.message.from_user.first_name}, "
                                       f"Bot sizga Namoz vaqtlarini o'z vaqtida eslatib turadi !!!",
                                  reply_markup=ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True))

        if user.id:
            count += 1
            context.bot.send_message(
                chat_id=ADMIN_ID,
                text=f"👤 New user:\n\n"
                     f"First name: {user['first_name']}\n"
                     f"Last name: {user['last_name']}\n"
                     f"Username: {user['username']}\n"
                     f"ID: {user['id']}\n"
                     f"Bot: {user['is_bot']}\n\n"
                     f"👤 Botda ro'yxatdan o'tgan odamlar {count} ta bo'ldi."
            )
    else:
        update.message.reply_text(text="Bot sizga Namoz vaqtlarini o'z vaqtida eslatib turadi !!!",
                                 reply_markup=ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True))

def info_command(update, context):
    update.message.reply_text(text=f"{update.message.from_user.first_name}, "
                                   f"bu bot sizga Namoz vaqtini eslatib turish uchun xizmat qiladi!")

def message_handler(update, context):
    message = update.message.text
    update.message.reply_chat_action(action=ChatAction.TYPING)
    if message == "🕋 Namoz haqida ma'lumot":
        update.message.reply_text(
            text=f"<b>{text}</b>",
            parse_mode="HTML"
        )
    else:
        update.message.reply_text(
            text=f"<b>Bot sizga yoqayotgan bo'lsa xursandmiz 😊</b>",
            parse_mode="HTML"
        )


def main():
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start_command))
    dispatcher.add_handler(CommandHandler('info', info_command))
    dispatcher.add_handler(MessageHandler(Filters.text, message_handler))

    updater.start_polling()
    updater.idle()
if __name__ == '__main__':
    main()
