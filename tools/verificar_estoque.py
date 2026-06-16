import os
import sys

ROOT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

print("ROOT:", ROOT_DIR)
print("PATH:", sys.path[0])

from inventario.database.db import conectar_db
from inventario.services.lista_compras_service import adicionar_item

LIMITE_ESTOQUE = 10


def verificar_estoque_baixo():

    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            nome,
            modelo,
            quantidade
        FROM itens
        WHERE quantidade < ?
        ORDER BY quantidade ASC
    """, (LIMITE_ESTOQUE,))

    resultados = cursor.fetchall()

    conn.close()

    print("\n==============================")
    print(" ITENS COM ESTOQUE BAIXO")
    print("==============================\n")

    if not resultados:
        print("Nenhum item encontrado.")
        return

    adicionados = 0

    for item_id, nome, modelo, quantidade in resultados:

        print(
            f"{nome} | "
            f"{modelo} | "
            f"Qtd: {quantidade}"
        )

        inseriu = adicionar_item(
            item_id=item_id,
            nome=nome,
            modelo=modelo,
            quantidade_atual=quantidade
        )

        if inseriu:
            adicionados += 1

    print("\n------------------------------")
    print(f"{adicionados} itens adicionados à lista de compras.")
    print("------------------------------")


if __name__ == "__main__":
    verificar_estoque_baixo()