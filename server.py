import requests
import schedule

from time import sleep
from threading import Thread
from flask import Flask, request

from bot_operations import add_user, get_companies_list, add_company, delete_company, set_notification_time, \
    show_trading_info, notification_info
from config import set_webhook, TELEGRAM_TOKEN, DEFAULT_NOTIFICATION_TIME
from database_operations import db_initialization, db_get_users_list
import messages


app = Flask(__name__)


def get_api_url(method):
    api_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/{method}"
    return api_url


def send_message(chat_id, content):
    method = "sendMessage"
    if type(content) is list:
        _content = '\n'.join(content)
    else:
        _content = content
    url = get_api_url(method)
    data = {"chat_id": chat_id, "text": _content}
    requests.post(url, data=data)


def send_notification_message(chat_id, content):
    send_message(chat_id, content)
    return schedule.CancelJob


def send_notifications():
    schedule.every().day.at("01:10").do(notification_schedule)

    while True:
        schedule.run_pending()
        sleep(10)


def notification_schedule():
    users_list = db_get_users_list()
    for user in users_list:
        content = notification_info(user[0])
        schedule.every().day.at(user[2]).do(send_notification_message, chat_id=user[3], content=content)


@app.route('/', methods=["POST"])
def message():
    user_id = request.json["message"]["from"]["id"]
    name = request.json["message"]["from"]["first_name"]
    chat_id = request.json["message"]["chat"]["id"]

    if "text" in request.json["message"]:
        text = request.json["message"]["text"]
        text_list = text.split()

        content = "неправильный ввод, для справки /help"
        if text_list[0] == "/help":
            content = messages.help_message
        elif text_list[0] == "/start":
            add_user(user_id, name, DEFAULT_NOTIFICATION_TIME, chat_id)
            content = messages.welcome_message
        elif text_list[0] == "/companies":
            content = get_companies_list(user_id)
        elif text_list[0] == "/add" and len(text_list) > 1:
            content = add_company(user_id, text_list[1])
        elif text_list[0] == "/del" and len(text_list) > 1:
            content = delete_company(user_id, text_list[1])
        elif text_list[0] == "/time" and len(text_list) > 1:
            content = set_notification_time(user_id, text_list[1])
        elif text_list[0] == "/show" and len(text_list) > 1:
            period = "year"
            content = show_trading_info(text_list[1], period)

        send_message(chat_id, content)

    return {"ok": True}


if __name__ == '__main__':

    set_webhook()

    db_initialization()

    notification_thread = Thread(target=send_notifications)
    notification_thread.start()

    app.run()
