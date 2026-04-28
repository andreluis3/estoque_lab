import sys
from PyQt6.QtWidgets import QApplication

from database.db import criar_tabela
from ui.janela_principal import MainWindow
from ui.tabela_estoque import TabelaEstoque
from controllers.crud import Crud
from services.importador import importar_para_banco


def main():
    print("Iniciando aplicação...")

    app = QApplication(sys.argv)

    criar_tabela()  # 🔥 SEMPRE PRIMEIRO


    #importar_para_banco("planilhas/estoque_lab_completa.xlsx")

    crud = Crud()
    itens = crud.listar_itens()
    print("Itens no banco:", len(itens))

    window = MainWindow()
    window.tabela.carregar_dados(itens)

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()