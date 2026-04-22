import sys
from PyQt6.QtWidgets import QApplication

from database.db import criar_tabela
from ui.janela_principal import MainWindow
from services.importador import importar_para_banco
from repositories.item_repository import listar_itens


def main():
    print("Iniciando aplicação...")

    app = QApplication(sys.argv)

    criar_tabela()  # 🔥 SEMPRE PRIMEIRO

    # ⚠️ DESCOMENTA SÓ UMA VEZ
    #importar_para_banco("planilhas/estoque_lab_completa.xlsx")

    itens = listar_itens()
    print("Itens no banco:", len(itens))

    window = MainWindow()
    window.tabela.carregar_dados(itens)

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()