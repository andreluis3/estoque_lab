from database.db import conectar_db


def inserir_item(item):
    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO itens (
            item, modelo, categoria, quantidade,
            local_caixa, local_slot, descricao, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        item["item"],
        item["modelo"],
        item["categoria"],
        item["quantidade"],
        item["local_caixa"],
        item["local_slot"],
        item.get("descricao", ""),
        ""
    ))

    conn.commit()
    conn.close()

def listar_itens():
    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM itens")
    rows = cursor.fetchall()

    conn.close()

    itens = []
    for row in rows:
        itens.append({
            "id": row[0],
            "item": row[1],
            "modelo": row[2],
            "categoria": row[3],
            "quantidade": row[4],
            "local_caixa": row[5],
            "local_slot": row[6],
            "descricao": row[7],
            "status": row[8],
        })

    return itens