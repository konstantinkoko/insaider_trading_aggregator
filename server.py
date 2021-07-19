from flask import Flask, request
import requests

from database_operations import *
from parcer import show_trading_info
import config, messages

app = Flask(__name__)

def get_api_url(method):
    api_url = f"https://api.telegram.org/bot{config.TELEGRAM_TOKEN}/{method}"
    return api_url

def send_message(chat_id, content):
    method = "sendMessage"
    url = get_api_url(method)
    data = {"chat_id": chat_id, "text": content}
    requests.post(url, data=data)

@app.route('/', methods=["POST"])
def message():
    id = request.json["message"]["from"]["id"]
    name = request.json["message"]["from"]["first_name"]
    chat_id = request.json["message"]["chat"]["id"]

    if "text" in request.json["message"]:
        text = request.json["message"]["text"]
        text_list = text.split()

        content = "неправильный ввод, для справки /help"
        if text_list[0] == "/help":
            content = messages.help_message
        elif text_list[0] == "/start":
            add_user(id, name)
            content = messages.welcome_message
        elif text_list[0] == "/companies":
            content = get_companies_list(id)
        elif text_list[0] == "/add" and len(text_list) > 1:
            content = add_company(id, text_list[1])
        elif text_list[0] == "/del" and len(text_list) > 1:
            content = delete_company(id, text_list[1])
        elif text_list[0] == "/time" and len(text_list) > 1:
            content = set_notification_time(text_list[1])
        elif text_list[0] == "/show" and len(text_list) > 1:
            content = show_trading_info(text_list[1])

        send_message(chat_id, content)

    return {"ok": True}

if __name__ == '__main__':
    app.run()