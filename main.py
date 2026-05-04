import sys
from PyQt6.QtWidgets import QApplication

from database.db import criar_tabela
from ui.janela_principal import MainWindow
from controllers.crud import Crud

from utils.comparador import comparar_planilha_banco
from services.sincronizador import sincronizar_planilha_banco


def main():
    print("Iniciando aplicação...")

    app = QApplication(sys.argv)

    criar_tabela()

    # 📥 SINCRONIZAÇÃO REMOVIDA (agora manual via botão)
    # sincronizar_planilha_banco("planilhas/estoque_lab_completa.xlsx")

    crud = Crud()
    itens = crud.listar_itens()

    print("Itens no banco:", len(itens))

    window = MainWindow()
    window.tabela.carregar_dados(itens)

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()