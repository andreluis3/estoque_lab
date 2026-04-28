# utils/excel_utils.py

import pandas as pd
from database.db import conectar_db

def exportar_para_excel():
    try:
        conn = conectar_db()
        df = pd.read_sql_query("SELECT * FROM itens", conn)

        df.to_excel("planilhas/estoque_lab_completa.xlsx", index=False)

        conn.close()
    except Exception as e:
        print("Erro ao exportar:", e)