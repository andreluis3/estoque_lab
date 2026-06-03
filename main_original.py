from PyQt6.QtWidgets import QApplication
import sys

from inventario.database.db import criar_tabela, conectar_db
from inventario.services.backup_service import criar_backup
from inventario.services.estoque_service import EstoqueService

from inventario.ui.app import AppUI


def main():
    print("Iniciando sistema...")

    criar_tabela()

    try:
        criar_backup()
    except Exception as e:
        print("backup erro:", e)

    app = QApplication(sys.argv)

    conn = conectar_db()
    service = EstoqueService(conn=conn)

    ui = AppUI(service)
    ui.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()