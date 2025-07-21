import os
import requests

telegram_token = os.environ['TELEGRAM_TOKEN']
BASE_URL = f"https://api.telegram.org/bot{telegram_token}"

def send_message(chat_id, text):
    url = f"{BASE_URL}/sendMessage"
    payload = {'chat_id': chat_id, 'text': text}
    requests.post(url, data=payload)