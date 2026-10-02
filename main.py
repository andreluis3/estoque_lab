import sys
import os

from PyQt6.QtWidgets import QApplication

from inventario.database.db import criar_tabela, conectar_db
from inventario.services.backup_service import BackupService
from inventario.services.estoque_service import EstoqueService
from inventario.ui.legacy.janela_principal import MainWindow


def main():

    print("=" * 60)
    print("INICIANDO APLICAÇÃO ESTOQUE LAB")
    print("=" * 60)


    # VER LOCAL ATUAL
    print("\n[DEBUG] Diretório atual:")
    print(os.getcwd())


    # BANCO
    print("\n[DEBUG] Criando tabela...")
    
    try:
        criar_tabela()
        print("[OK] Tabela criada/verificada")
    except Exception as e:
        print("[ERRO criar_tabela]")
        print(e)


    # BACKUP
    print("\n[DEBUG] Criando backup...")

    try:
        #criar_backup()
        print("[OK] Backup realizado")
    except Exception as e:
        print("[ERRO backup]")
        print(e)



    # QT
    print("\n[DEBUG] Inicializando PyQt")

    app = QApplication(sys.argv)



    # CONEXÃO
    print("\n[DEBUG] Abrindo conexão banco")

    try:

        conexao_db = conectar_db()

        print("[OK] Banco conectado")
        print("Objeto conexão:")
        print(conexao_db)

    except Exception as e:

        print("[ERRO conexão banco]")
        print(e)
        return



    # SERVICE
    print("\n[DEBUG] Criando EstoqueService")

    estoque_service = EstoqueService(
        conn=conexao_db
    )


    print("[OK] Service criado")



    # TELA
    print("\n[DEBUG] Abrindo janela")

    window = MainWindow(
        estoque_service=estoque_service
    )

    print("[OK] Janela criada")

    window.show()



    print("\nAPLICAÇÃO RODANDO")
    print("=" * 60)


    sys.exit(app.exec())



if __name__ == "__main__":
    main()