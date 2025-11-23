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
    - detalle (texto): descripción del gasto
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
    
    Si se indica que se quiere el total agrupado por tipo, se ha de llamar a gastos_agrupados_por_mes_y_year y añadir como parametro el año elegido por el usuario
    """
    optimized_prompt = f"""
    Estoy utilizando DeepSeek para convertir un texto en lenguaje natural proporcionado por el usuario en una consulta SQL ejecutada mediante el cliente de Supabase en Python.
    
    La tabla se llama **gastos** y tiene las siguientes columnas:
    - id (autogenerado)
    - tipo (texto)
    - detalle (texto)
    - total (numérico)
    - created_at (fecha con formato 'YYYY-MM-DD')
    
    Quiero que DeepSeek genere **solo el fragmento de código Python** que construya la consulta usando el cliente oficial de Supabase.  
    No debe incluir imports, conexión, prints, variables adicionales ni explicaciones: únicamente la línea o bloque correspondiente al `response = ...`.
    
    Reglas importantes:
    1. Si el usuario no indica el año, debe usarse el año actual: **2025**.
    2. Para filtrar por mes/año, **no usar `.eq("created_at", ...)`**. Siempre usar rangos de fechas (`.gte()` y `.lte()`).
    3. No usar `ilike`. Los nombres de columnas siempre coinciden con lo que pide el usuario.
    4. La tabla siempre es `gastos` y la consulta se hace con `.from_("gastos")`.
    5. Si el usuario pide resultados **agrupados por tipo**, se debe llamar al RPC: gastos_agrupados_por_year, enviando como parámetro el año solicitado **year**, si no se especifica, **2025**.
    6. La respuesta generada debe consistir EXCLUSIVAMENTE en el código Python que asigna la variable `response`.
    Finalmente, convierte **{text}** en el código Python correspondiente cumpliendo estas reglas. La salida debe ser solamente el fragmento de código del `response`.
    """
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": optimized_prompt}],
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