import sys
from PyQt6.QtWidgets import QApplication

from inventario.database.db import criar_tabela, conectar_db
from inventario.services.backup_service import criar_backup
from inventario.services.estoque_service import EstoqueService
from inventario.ui.janela_principal import MainWindow


def main():
    print("Iniciando aplicação Estoque Lab...")

    # 1. Banco e backup
    criar_tabela()

    try:
        criar_backup()
        print("-> Backup preventivo inicializado com sucesso.")
    except Exception as e:
        print(f"-> Aviso: Não foi possível realizar o backup inicial: {e}")

    # 2. App Qt
    app = QApplication(sys.argv)

    # 3. Banco + service
    conexao_db = conectar_db()
    estoque_service = EstoqueService(conn=conexao_db)

    # 4. UI principal (ANTIGA, ESTÁVEL)
    window = MainWindow(estoque_service=estoque_service)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()