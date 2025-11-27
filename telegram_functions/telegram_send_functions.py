import os
import requests

telegram_token = os.environ['TELEGRAM_TOKEN']
BASE_URL = f"https://api.telegram.org/bot{telegram_token}"

def send_message(chat_id, text):
    url = f"{BASE_URL}/sendMessage"
    payload = {'chat_id': chat_id, 'text': text}
    requests.post(url, data=payload)

def setCommands():
    commands = [
        {"command": "savexpense", "description": "Guardar un gasto: /saveExpense producto burbujas 2.99 24112025"},
        {"command": "saventry", "description": "Guardar un beneficio: /saveEntry perfume tygar 35 25062025"},
        {"command": "check", "description": "Consultar tus gastos: /check {pregunta en lenguaje natural}"}
    ]

    response = requests.post(f"{BASE_URL}/setMyCommands", json={"commands": commands})
    print(response.json())


