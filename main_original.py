import sys

from PyQt6.QtWidgets import QApplication

from inventario.database.db import (
    criar_tabela,
    conectar_db
)

from inventario.services.backup_service import criar_backup
from inventario.services.estoque_service import EstoqueService

# IMPORTA A UI DO HENRIQUE
from inventario.frontend_henrique.projeto.main import SistemaInventario


def main():
    print("Iniciando integração frontend Henrique...")

    # Inicializa estrutura do banco
    criar_tabela()

    # Backup preventivo
    try:
        criar_backup()
        print("-> Backup criado com sucesso.")
    except Exception as e:
        print(f"-> Erro no backup: {e}")

    # QApplication
    app = QApplication(sys.argv)

    # Conexão banco
    conexao_db = conectar_db()

    # Service principal
    estoque_service = EstoqueService(
        conn=conexao_db
    )

    # Abre frontend Henrique
    window = SistemaInventario(
        estoque_service=estoque_service
    )

    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()