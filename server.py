from flask import Flask, request

from bot_operations import add_user, get_companies_list, add_company, delete_company, set_notification_time, \
    show_trading_info
from database_operations import db_initialization
from config import *
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
            add_user(user_id, name)
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
            content = show_trading_info(text_list[1], "year")

        send_message(chat_id, content)

    return {"ok": True}


if __name__ == '__main__':
    db_initialization()
    set_webhook()
    app.run()
