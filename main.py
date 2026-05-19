import sys
from PyQt6.QtWidgets import QApplication

from database.db import criar_tabela, conectar_db
from database.backup import criar_backup
from services.estoque_service import EstoqueService
from ui.janela_principal import MainWindow


def main():
    print("Iniciando aplicação Estoque Lab...")

    # 1. Garante tabelas estruturadas e executa o backup preventivo
    criar_tabela()
    try:
        criar_backup()
        print("-> Backup preventivo inicializado com sucesso.")
    except Exception as e:
        print(f"-> Aviso: Não foi possível realizar o backup inicial: {e}")

    app = QApplication(sys.argv)

    # 2. Inicia conexão única do Banco e injeta na camada de Serviço
    conexao_db = conectar_db()
    estoque_service = EstoqueService(conn=conexao_db)

    # 3. Passa o serviço central para a janela inicial
    window = MainWindow(estoque_service=estoque_service)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()