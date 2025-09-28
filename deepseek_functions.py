import os
import requests
from loguru import logger
from fastapi import HTTPException

DEEPSEEK_API_KEY = os.environ["DEEPSEEK_API_KEY"]

if not DEEPSEEK_API_KEY:
    raise ValueError("Deepseek key is not defined.")

DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

def convert_text_to_function(text):
    logger.info(f"Convirtiendo texto a query")
    prompt = f"""
    Estoy utilizando DeepSeek para transformar un texto proporcionado por el usuario en una consulta (query) que extraiga información específica de una tabla llamada gastos en una base de datos Supabase.

    La tabla tiene las siguientes columnas:
    - id (autogenerado)
    - tipo (texto): indica el tipo de gasto (por ejemplo, restaurante, cena, regalo, perfume, etc.)
    - total (numérico): coste total del gasto
    - created_at (fecha): fecha en formato 'YYYY-MM-DD' cuando se realizó el gasto

    El objetivo es que, dado un texto descriptivo como "gastos en restaurantes del mes de julio", DeepSeek genere una consulta SQL para PostgreSQL que recupere la información solicitada desde la tabla.

    La respuesta que quiero debe ser únicamente el código en Python que, usando el cliente oficial de Supabase, ejecute esa consulta y devuelva los resultados correspondientes. No des información adicional, solo el código en Python.

    Lsa respuestas deben contener solo el fragmento de código en Python que use supabase client para obtener esos datos. La conexión a supabase la ejecuto yo y no te tienes que preocupar de eso, solo de la parte de la query a supabase
    
    Ahora, sabiendo esta informacion, convierte {text} al código en Python. Solo debes generar la parte del response sin ningún tipo de import o impresión por pantalla.
    
    En caso de no indicarse el año, debe ser el año actual.
    
    La tabla se llama gastos.
    
    No uses ilike, el nombre de columna que se da siempre es el correcto. Debes usar from.
    
    Para filtrar por la columna created_at por un mes y año concretos, no uses .eq("created_at", año, month: mes) porque eso no es válido. En su lugar, usa un rango de fechas
    
    Es muy importante no incluir mas parte de codigo que lo respectivo al response.
    
    Si no se indica lo contrario, las búsquedas para la columna created_at deben ser para el año actual, es decir, 2025
    
    
    """

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
    }

    response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data)
    if response.status_code != 200:
        logger.error(f"Error en DeepSeek API: {response.status_code} - {response.text}")
        raise HTTPException(status_code=500, detail="Error con la API de DeepSeek")
    logger.info("Respuesta recibida de DeepSeek")

    response_json = response.json()
    # Suponiendo que la respuesta está en response_json["choices"][0]["message"]["content"]
    generated_code = response_json.get("choices", [{}])[0].get("message", {}).get("content", "")

    logger.debug(f"Código generado por DeepSeek:\n{generated_code}")

    # Opcional: devolver el código para que lo uses o ejecutes después
    return generated_code