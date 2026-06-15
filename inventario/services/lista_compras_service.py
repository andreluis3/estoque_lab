from inventario.database.db import conectar_db


def adicionar_item(
    item_id,
    nome,
    modelo,
    quantidade_atual,
    usuario="Sistema",
    observacao=""
):
    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id
        FROM lista_compras
        WHERE item_id = ?
        AND status = 'PENDENTE'
    """, (item_id,))

    existente = cursor.fetchone()

    if existente:
        conn.close()
        return False

    cursor.execute("""
        INSERT INTO lista_compras (
            item_id,
            nome,
            modelo,
            quantidade_atual,
            usuario,
            observacao
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        item_id,
        nome,
        modelo,
        quantidade_atual,
        usuario,
        observacao
    ))

    conn.commit()
    conn.close()

    return True


def listar_itens():
    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM lista_compras
        ORDER BY criado_em DESC
    """)

    dados = cursor.fetchall()

    conn.close()

    return dados


def remover_item(id_lista):
    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM lista_compras
        WHERE id = ?
    """, (id_lista,))

    conn.commit()
    conn.close()


def marcar_comprado(id_lista):
    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE lista_compras
        SET status = 'COMPRADO'
        WHERE id = ?
    """, (id_lista,))

    conn.commit()
    conn.close()