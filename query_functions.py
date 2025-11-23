from datetime import datetime
from telegram_send_functions import send_message

def save_expense(text, supabase_client, chat_id):
    try:
        parts = text.strip().split()

        if len(parts) != 5:
            error_message = "❌ Formato incorrecto. Usa: /save tipo total fecha (ej. /save comida 12.50 21072025)"
            print(error_message)
            send_message(chat_id, error_message)
            return

        _, tipo, detalle, total_str, fecha_str = parts

        try:
            total = float(total_str)
            if total <= 0:
                raise ValueError("El total debe ser mayor que 0")
        except ValueError:
            error_message = "❌ Total inválido. Debe ser un número mayor que 0 (ej. 12.50)"
            print(error_message)
            send_message(chat_id, error_message)
            return

        if len(fecha_str) != 8 or not fecha_str.isdigit():
            error_message = "❌ Fecha inválida. Usa formato ddmmyyyy (ej. 21072025)"
            print(error_message)
            send_message(chat_id, error_message)
            return

        try:
            day = int(fecha_str[:2])
            month = int(fecha_str[2:4])
            year = int(fecha_str[4:8])
            fecha = datetime(year, month, day)
        except ValueError:
            error_message = "❌ Fecha inválida. Revisa si el día o el mes son correctos."
            print(error_message)
            send_message(chat_id, error_message)
            return

        response = supabase_client.table('gastos').insert({
            'tipo': tipo,
            'detalle': detalle,
            'total': total,
            'created_at': fecha.isoformat()
        }).execute()

        if response.data:
            confirmation = f"✅ Gasto guardado:\nTipo: {tipo}\nDetalle: {detalle}\nTotal: {total:.2f}€\nFecha: {fecha.strftime('%d/%m/%Y')}"
            print(confirmation)
            send_message(chat_id, confirmation)
            return True
        else:
            error_message = f"❌ Error guardando gasto. Respuesta: {response}"
            print(error_message)
            send_message(chat_id, error_message)

    except Exception as e:
        error_message = f"❌ Error inesperado en save_expense: {e}"
        print(error_message)
        send_message(chat_id, error_message)

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
    local_vars = {
        "supabase": supabase_client,
        "datetime": datetime
    }
    exec(cleaned_code, globals(), local_vars)
    response = local_vars.get("response")
    return response

def process_query_result(query_result):
    total_sumado = 0
    mensaje = ""
    try:
        if not query_result or not query_result.data:
            return "No se encontraron resultados."

        for gasto in query_result.data:
            tipo = gasto.get('tipo', 'Desconocido')
            detalle = gasto.get('detalle', 'Sin detalle')
            total = gasto.get('total', 0)
            fecha = gasto.get('created_at', 'Sin fecha')
            total_sumado += total
            mensaje += f"Tipo: {tipo}, Detalle: {detalle}, Total: {total:.2f}, Fecha: {fecha}\n"

        mensaje += f"\nTotal acumulado: {total_sumado:.2f}"

    except Exception as e:
        mensaje = f"La query ha generado un error: {str(e)}"

    return mensaje

    mensaje += f"\nTotal acumulado: {total_sumado:.2f}"
    return mensaje