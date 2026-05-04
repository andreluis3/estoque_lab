import sqlite3

conn = sqlite3.connect('database/estoque.db')
cursor = conn.cursor()

# Ver tabelas
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print('Tabelas:', tables)

# Reset autoincrement
cursor.execute("DELETE FROM sqlite_sequence WHERE name='itens'")
conn.commit()
print('Autoincrement resetado.')

conn.close()