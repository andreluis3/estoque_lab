from PyQt6.QtWidgets import QApplication
import sys

from inventario.database.db import criar_tabela, conectar_db
from inventario.services.backup_service import criar_backup
from inventario.services.estoque_service import EstoqueService
from inventario.ui.app import AppUI


def main():
    print("=" * 60)
    print("[MAIN] Iniciando Sistema de Estoque IPT")
    print("=" * 60)

    # Banco
    print("[MAIN] Criando/Verificando tabelas...")
    criar_tabela()
    print("[MAIN] Banco inicializado.")

    # Backup
    print("[MAIN] Verificando backup...")
    try:
        criar_backup()
        print("[MAIN] Backup criado com sucesso.")
    except Exception as e:
        print(f"[ERRO] Backup: {e}")

    # QApplication
    print("[MAIN] Criando QApplication...")
    app = QApplication(sys.argv)

    # Banco de dados
    print("[MAIN] Conectando ao banco...")
    conn = conectar_db()
    print("[MAIN] Conexão realizada.")

    # Service
    print("[MAIN] Criando EstoqueService...")
    service = EstoqueService(conn=conn)
    print("[MAIN] EstoqueService criado.")

    # Interface
    print("[MAIN] Abrindo AppUI...")
    ui = AppUI(service)
    ui.show()
    print("[MAIN] Interface exibida.")

    print("=" * 60)
    print("[MAIN] Sistema iniciado com sucesso.")
    print("=" * 60)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()