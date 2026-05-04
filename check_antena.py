import sqlite3

conn = sqlite3.connect('database/estoque.db')
cursor = conn.cursor()
cursor.execute("SELECT id, nome, quantidade FROM itens WHERE nome LIKE '%antena lora%' LIMIT 5")
rows = cursor.fetchall()
for row in rows:
    print(f'ID: {row[0]}, Nome: {row[1]}, Quantidade: {row[2]}')
conn.close()