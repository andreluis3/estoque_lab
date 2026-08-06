import sys

from PyQt6.QtWidgets import QApplication

from inventario.database.db import criar_tabela
from inventario.services.estoque_service import EstoqueService

from inventario.ui.app import AppUI


def main():

    # garante estrutura do banco
    criar_tabela()

    # instancia serviço principal
    service = EstoqueService()

    # inicia Qt
    app = QApplication(sys.argv)

    # inicia interface
    ui = AppUI(service)
    ui.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()