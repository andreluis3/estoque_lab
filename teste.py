# test_timestamp.py — execute na raiz do projeto
from datetime import datetime
import sqlite3
from inventario.database.db import DB_PATH  # ou use o path do seu db

print("Horário Python (local):", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()
# Inserir registro de teste:
cur.execute("INSERT INTO movimentacoes (item_id, tipo, quantidade, usuario, data) VALUES (?, ?, ?, ?, ?)",
            (0, 'teste', 1, 'teste', datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
conn.commit()
row = cur.execute("SELECT id, tipo, usuario, data FROM movimentacoes ORDER BY id DESC LIMIT 1").fetchone()
print("Horário salvo no SQLite:", row[3])
conn.close()