import os
import requests
from supabase import create_client, Client
from supabase_functions.query_functions import save_expense, save_entry, function_executor, process_query_result
from deepseek_functions import convert_text_to_function
from graph_functions.df_functions import generate_final_dataframe
from graph_functions.graph_functions import create_graph

telegram_token = os.environ['TELEGRAM_TOKEN']
BASE_URL = f"https://api.telegram.org/bot{telegram_token}"
SUPABASE_URL = os.environ['SUPABASE_URL']
SUPABASE_KEY = os.environ['SUPABASE_KEY']
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def send_message(chat_id, text):
    url = f"{BASE_URL}/sendMessage"
    payload = {'chat_id': chat_id, 'text': text}
    requests.post(url, data=payload)

def send_graph(chat_id, option, graph):
    if option == "balance":
        caption = "Gráfico de Balance"
    elif option == "gastos":
        caption = "Gráfico de Gastos"
    else:
        caption = "Gráfico de Ingresos"

    url = f"{BASE_URL}/sendPhoto"

    files = {
        'photo': ('grafico.png', graph, 'image/png')
    }
    data = {
        'chat_id': chat_id,
        'caption': caption
    }
    requests.post(url, files=files, data=data)

def get_updates(offset=None):
    url = f"{BASE_URL}/getUpdates"
    params = {
        'timeout': 600,
        'offset': offset
    }

    try:
        response = requests.get(url, params=params, timeout=610)
        if response.status_code == 200:
            return response.json()

    except requests.exceptions.RequestException as e:
        print("Error de conexión con Telegram:", e)

    return None

def handle_message(message):
    text = message.get('text', '')
    text = text.lower()
    chat_id = message['chat']['id']

    if text.startswith('/savexpense'):
        # Use save function
        print(f"Comando /savexpense recibido en chat {chat_id} con mensaje: {text}")
        save_expense(text, supabase, chat_id)

    elif text.startswith('/saventry'):
        print(f"Comando /saventry recibido en chat {chat_id} con mensaje: {text}")
        save_entry(text, supabase, chat_id)

    elif text.startswith('/check'):
        print(f"Comando /check recibido en chat {chat_id} con mensaje: {text}")
        curated_text = text[len('/check'):].strip()
        generated_code = convert_text_to_function(curated_text)
        query_result = function_executor(generated_code, supabase)
        telegram_message = process_query_result(query_result)
        send_message(chat_id, telegram_message)

    elif text.startswith('/graph'):
        print(f"Comando /graph recibido en chat {chat_id} con mensaje: {text}")
        option, df = generate_final_dataframe(text, supabase)
        graph = create_graph(option, df)
        send_graph(chat_id, option, graph)
    else:
        print(f"Mensaje recibido en chat {chat_id}: {text}")