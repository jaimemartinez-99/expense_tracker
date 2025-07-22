# 📊 Expense Tracker Bot

Este proyecto es un **bot de Telegram conectado a Supabase** que permite registrar y consultar gastos personales de forma rápida y sencilla mediante comandos de texto. La consulta se
escribe en lenguaje natural y se traduce a lenguaje SQL gracias a la API de DeepSeek.

## 🚀 ¿Qué hace?

El bot escucha mensajes de Telegram y responde a dos comandos principales:

### `/save`
Permite registrar un nuevo gasto.

**Formato del mensaje:**

- `tipo`: Categoría del gasto (ej. comida, transporte, ocio…).
- `total`: Monto numérico (ej. `12.50`).
- `fecha`: En formato `ddmmyyyy` (ej. `21072025` para el 21 de julio de 2025).

**Ejemplo:**
/save comida 12.50 21072025

✅ Gasto guardado:
Tipo: comida
Total: 12.50€
Fecha: 21/07/2025

✅ El bot:
- Valida los datos.
- Convierte la fecha al formato adecuado.
- Inserta el gasto en la tabla `gastos` de Supabase.
- Muestra un mensaje de confirmación.

---

### `/check`
Consulta los gastos registrados y devuelve un resumen.

**Ejemplo:**

/check gastos en comida totales:

Tipo: comida, Total: 12.50, Fecha: 2025-07-21

Total acumulado: 12.50

---

## ⚙️ Estructura técnica

- **Telegram Bot API**: Escucha y procesa mensajes entrantes.
- **Supabase**: Almacena los datos de los gastos. Usa una tabla llamada `gastos` con las siguientes columnas:
  - `id`: Autogenerado
  - `tipo`: Tipo de gasto a guardar: restaurante, regalo, comida... (`text`)
  - `total`: Importe total del gasto (`numeric`)
  - `created_at`: Fecha y hora (`date`)
- **Deepseek**: Usado cuando el usuario manda `/check` para generar queries a partir de lenguaje natural.

---


# 📊 Expense Tracker Bot

This project is a **Telegram bot connected to Supabase** that allows users to quickly and easily log and query personal expenses using simple text commands. Queries are written in natural language and translated to SQL using the DeepSeek API.

## 🚀 What does it do?

The bot listens to Telegram messages and responds to two main commands:

### `/save`
Allows you to register a new expense.

**Message format:**

- `type`: Expense category (e.g. food, transport, leisure…).
- `total`: Numeric amount (e.g. `12.50`).
- `date`: Date in `ddmmyyyy` format (e.g. `21072025` for July 21, 2025).

**Example:**
/save food 12.50 21072025

✅ Expense saved:
Type: food
Total: 12.50€
Date: 21/07/2025


✅ The bot:
- Validates the data.
- Converts the date to the appropriate format.
- Inserts the expense into the `gastos` table in Supabase.
- Sends a confirmation message.

---

### `/check`
Queries the stored expenses and returns a summary.

**Example:**
✅ Expense saved:  
Type: food  
Total: €12.50  
Date: 21/07/2025

---

## ⚙️ Technical Structure

- **Telegram Bot API**: Listens for and processes incoming messages.
- **Supabase**: Stores the expense data. Uses a table called `gastos` with the following columns:
  - `id`: Auto-generated
  - `tipo`: Type of expense to be saved (e.g. restaurant, gift, food…) (`text`)
  - `total`: Total amount of the expense (`numeric`)
  - `created_at`: Date and time (`date`)
- **DeepSeek**: Used when the user sends `/check` to generate SQL queries from natural language.

---