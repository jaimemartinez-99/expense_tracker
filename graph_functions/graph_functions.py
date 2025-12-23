import matplotlib.pyplot as plt
from io import BytesIO

def create_graph(option, df_final ):
    if df_final.empty:
        raise ValueError("El DataFrame está vacío, no se puede generar gráfico.")

    if option == "gastos":
        colors = ["red"] * len(df_final)
    elif option == "ingresos":
        colors = ["blue"] * len(df_final)
    elif option == "balance":
        colors = ["blue" if t == "Ingresos" else "red" for t in df_final["tipo"]]
    else:
        colors = ["gray"] * len(df_final)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(df_final["tipo"], df_final["total"], color=colors)

    ax.set_xlabel("Tipo")
    ax.set_ylabel("Total")
    ax.set_title(f"Gráfico de {option.capitalize()}")

    for i, val in enumerate(df_final["total"]):
        ax.text(i, val + max(df_final["total"]) * 0.01, f"{val}", ha='center', va='bottom')

    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    plt.close(fig)

    return buffer