import os
import uvicorn
import requests
from fastapi import FastAPI, Request
from pydantic import BaseModel
from supabase import create_client, Client
from query_functions import save_expense, function_executor, process_query_result
from deepseek_functions import convert_text_to_function

TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
SUPABASE_URL = os.environ['SUPABASE_URL']
SUPABASE_KEY = os.environ['SUPABASE_KEY']
BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()

def send_message(chat_id, text):
    url = f"{BASE_URL}/sendMessage"
    payload = {'chat_id': chat_id, 'text': text}
    requests.post(url, data=payload)

def handle_message(message):
    text = message.get('text', '').lower()
    chat_id = message['chat']['id']

    if text.startswith('/save'):
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

@app.post("/webhook")
async def telegram_webhook(req: Request):
    body = await req.json()
    if 'message' in body:
        handle_message(body['message'])
    return {"ok": True}

@app.get("/")
def root():
    return {"message": "Bot is running!"}

if __name__ == "__main__":
    uvicorn.run("telegram_functions:app", host="0.0.0.0", port=8000, reload=True)
