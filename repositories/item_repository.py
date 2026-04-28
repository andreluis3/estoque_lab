from database.db import conectar_db


def inserir_item(item):
    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO itens (
            nome, tipo, modelo, quantidade,
            caixa, localizacao, slot
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        item["nome"],
        item["tipo"],
        item["modelo"],
        item["quantidade"],
        item["caixa"],
        item["localizacao"],
        item["slot"],
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

def atualizar_item(item_id, dados):
    query = """
        UPDATE itens
        SET nome = ?,
            tipo = ?,
            modelo = ?,
            quantidade = ?,
            caixa = ?,
            localizacao = ?,
            slot = ?
        WHERE id = ?
    """
    conn = conectar_db()
    conn.execute(query, (
        dados["nome"],
        dados["tipo"],
        dados["modelo"],
        dados["quantidade"],
        dados["caixa"],
        dados["localizacao"],
        dados["slot"],
        item_id
    ))

    conn.commit()

    return {"status": "ok"}