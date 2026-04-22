import sys
from PyQt6.QtWidgets import QApplication

from ui.janela_principal import MainWindow
from services.importador import importar_excel


def main():
    app = QApplication(sys.argv)

    window = MainWindow()

    # 👇 carrega dados
    itens = importar_excel("planilhas/estoque_lab_completa.xlsx")
    window.tabela.carregar_dados(itens)

    window.show()
    sys.exit(app.exec())

from services.importador import importar_para_banco

importar_para_banco("planilhas/estoque_lab_completa.xlsx")

if __name__ == "__main__":
    main()