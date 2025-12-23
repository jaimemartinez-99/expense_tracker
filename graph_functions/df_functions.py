import pandas as pd
from datetime import datetime

def generate_dataframe_for_graph(text, supabase):
    option, month, year = filter_text(text)

    if option in ["gastos", "balance"]:
        resp_g = supabase.table("gastos").select("*").execute()
        df_g = pd.DataFrame(resp_g.data)
        if not df_g.empty:
            df_g["created_at"] = pd.to_datetime(df_g["created_at"])
            df_g["total"] = df_g["total"]

    if option in ["ingresos", "balance"]:
        resp_i = supabase.table("ingresos").select("*").execute()
        df_i = pd.DataFrame(resp_i.data)
        if not df_i.empty:
            df_i["created_at"] = pd.to_datetime(df_i["created_at"])

    def filter_by_date(df):
        if df.empty:
            return df
        df = df[df["created_at"].dt.year == year]
        if month:
            df = df[df["created_at"].dt.month == month]
        return df

    if option == "gastos":
        df = filter_by_date(df_g)
        return option, df
    elif option == "ingresos":
        df = filter_by_date(df_i)
        return option, df
    elif option == "balance":
        df_g_filtered = filter_by_date(df_g)
        df_g_filtered["total"] = -df_g_filtered["total"]
        df_i_filtered = filter_by_date(df_i)
        df_i_filtered["total"] = df_i_filtered["total"]
        df = pd.concat([df_g_filtered, df_i_filtered], ignore_index=True)
        return option, df

    else:
        return pd.DataFrame(columns=["created_at", "total"])

def filter_text(text):
    parts = text.split()
    option = parts[1].lower()

    month = None
    year = None

    for part in parts[2:]:
        if part.startswith("m"):
            try:
                month = int(part[1:])
            except:
                pass
        elif part.startswith("y"):
            try:
                year = int(part[1:])
            except:
                pass

    if year is None:
        year = datetime.now().year

    return option, month, year

def generate_final_dataframe(text, supabase):
    option, df = generate_dataframe_for_graph(text, supabase)
    if option == "balance":
        if df.empty:
            return pd.DataFrame({"tipo": ["Ingresos", "Gastos"], "total": [0, 0]})

        ingresos_total = df[df["total"] > 0]["total"].sum()
        gastos_total = df[df["total"] < 0]["total"].sum()

        df_final = pd.DataFrame({
            "tipo": ["Ingresos", "Gastos"],
            "total": [ingresos_total, abs(gastos_total)]
        })
        return option, df_final
    else :
        if df.empty:
            return pd.DataFrame(columns=["tipo", "total"])

        df_final = df.groupby("tipo")["total"].sum().reset_index()
        return option, df_final