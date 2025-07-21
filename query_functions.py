import os
import ast

from datetime import datetime
from telegram_send_functions import send_message

def save_expense(text, supabase_client):
    # Text example: "/save comida 12.50 2025-07-21"
    try:
        parts = text.strip().split()
        # parts[0] = "/save"
        # parts[1] = tipo
        # parts[2] = total
        # parts[3] = fecha

        if len(parts) != 4:
            print("Error: Formato incorrecto. Usa /save tipo total fecha")
            return

        _, tipo, total_str, fecha_str = parts

        total = float(total_str)

        if len(fecha_str) != 8:
            print("Error: La fecha debe tener formato ddmmyyyy, ejemplo 21072025")
            return

        day = int(fecha_str[:2])
        month = int(fecha_str[2:4])
        year = int(fecha_str[4:8])

        fecha = datetime(year, month, day)

        response = supabase_client.table('gastos').insert({
            'tipo': tipo,
            'total': total,
            'created_at': fecha.isoformat()
        }).execute()

        if response:
            telegram_message = f"Gasto guardado: {tipo}, {total}, {fecha_str}"
            print(telegram_message)
            send_message(os.environ['CHAT_ID'],telegram_message)
            return True
        else:
            print(f"Error guardando gasto: {response.data}")

    except Exception as e:
        print(f"Error procesando save_expense: {e}")

def clean_code_block(text):
    # Remove markdown
    lines = text.strip().splitlines()
    if lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].startswith("```"):
        lines = lines[:-1]
    return "\n".join(lines)

def function_executor(generated_code, supabase_client):
    cleaned_code = clean_code_block(generated_code)
    #cleaned_code = ast.literal_eval(f'"{cleaned_code}"')
    local_vars = {"supabase": supabase_client, "datetime": __import__('datetime')}
    exec(cleaned_code, globals(), local_vars)
    response = local_vars.get("response")
    return response

def process_query_result(query_result):
    total_sumado = 0
    mensaje = ""

    for gasto in query_result.data:
        tipo = gasto['tipo']
        total = gasto['total']
        fecha = gasto['created_at']
        total_sumado += total
        mensaje += f"Tipo: {tipo}, Total: {total:.2f}, Fecha: {fecha}\n"

    mensaje += f"\nTotal acumulado: {total_sumado:.2f}"
    return mensaje