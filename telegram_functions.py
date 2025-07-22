import os
import requests
from supabase import create_client, Client
from query_functions import save_expense, function_executor, process_query_result
from deepseek_functions import convert_text_to_function
telegram_token = os.environ['TELEGRAM_TOKEN']
BASE_URL = f"https://api.telegram.org/bot{telegram_token}"
SUPABASE_URL = os.environ['SUPABASE_URL']
SUPABASE_KEY = os.environ['SUPABASE_KEY']
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def send_message(chat_id, text):
    url = f"{BASE_URL}/sendMessage"
    payload = {'chat_id': chat_id, 'text': text}
    requests.post(url, data=payload)


def get_updates(offset=None):
    url = f"{BASE_URL}/getUpdates"
    params = {'timeout': 100, 'offset': offset}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    return None

def handle_message(message):
    text = message.get('text', '')
    text = text.lower()
    chat_id = message['chat']['id']

    if text.startswith('/save'):
        # Use save function
        print(f"Comando /save recibido en chat {chat_id} con mensaje: {text}")
        save_expense(text, supabase, chat_id)
    elif text.startswith('/check'):
        print(f"Comando /check recibido en chat {chat_id} con mensaje: {text}")
        curated_text = text[len('/check'):].strip()
        generated_code = convert_text_to_function(curated_text)
        query_result = function_executor(generated_code, supabase)
        telegram_message = process_query_result(query_result)
        send_message(chat_id, telegram_message)

    else:
        print(f"Mensaje recibido en chat {chat_id}: {text}")