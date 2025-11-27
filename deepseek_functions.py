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
    optimized_prompt = f"""
    Estoy utilizando DeepSeek para convertir un texto en lenguaje natural proporcionado por el usuario en una consulta SQL ejecutada mediante el cliente de Supabase en Python.
    Existen dos tablas en la base de datos: **gastos** e **ingresos**.
    La primera tabla se llama **gastos** y tiene las siguientes columnas:
    - id (autogenerado)
    - tipo (texto)
    - detalle (texto)
    - total (numérico)
    - created_at (fecha con formato 'YYYY-MM-DD')
    
    La segunda tabla se llama **ingresos** y tiene las siguientes columnas:
    - id (autogenerado)
    - tipo (texto)
    - detalle (texto)
    - total (numérico)
    - created_at (fecha con formato 'YYYY-MM-DD')
    
    Por el contexto del mensaje, el usuario se podra referir a cualquiera de las dos tablas.
    Quiero que DeepSeek genere **solo el fragmento de código Python** que construya la consulta usando el cliente oficial de Supabase.  
    No debe incluir imports, conexión, prints, variables adicionales ni explicaciones: únicamente la línea o bloque correspondiente al `response = ...`.
    
    Reglas importantes:
    1. Si el usuario no indica el año, debe usarse el año actual: **2025**.
    2. Para filtrar por mes/año, **no usar `.eq("created_at", ...)`**. Siempre usar rangos de fechas (`.gte()` y `.lte()`).
    3. No usar `ilike`. Los nombres de columnas siempre coinciden con lo que pide el usuario.
    4. Si el usuario pide gastos la tabla siempre sera `gastos` y la consulta se hace con `.from_("gastos")`.
    5. Si el usuario pide ingresos o beneficios la tabla siempre sera `ingresos` y la consulta se hace con `.from_("ingresos")`.
    6. Si el usuario pide gastos **agrupados por tipo**, se debe llamar al RPC: gastos_agrupados_por_year, enviando como parámetro el año solicitado **year**, si no se especifica, **2025**.
    7. Si el usuario pide ingresos **agrupados por tipo**, se debe llamar al RPC: ingresos_agrupados_por_year, enviando como parámetro el año solicitado **year**, si no se especifica, **2025**.
    8. La respuesta generada debe consistir EXCLUSIVAMENTE en el código Python que asigna la variable `response`.
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