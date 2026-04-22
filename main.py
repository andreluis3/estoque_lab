import sys
from PyQt6.QtWidgets import QApplication

from ui.main_window import MainWindow
from utils.importador import importar_excel


def main():
    app = QApplication(sys.argv)

    window = MainWindow()

    # 👇 carrega dados
    itens = importar_excel("sua_planilha.xlsx")
    window.tabela.carregar_dados(itens)

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()