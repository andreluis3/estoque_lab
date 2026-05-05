import sys
from PyQt6.QtWidgets import QApplication

from database.db import criar_tabela
from ui.janela_principal import MainWindow


def main():
    print("Iniciando aplicação...")

    criar_tabela()  # garante que as tabelas existem antes de qualquer coisa

    app = QApplication(sys.argv)

    window = MainWindow()  # MainWindow já cria o Crud e carrega a tabela internamente
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main() 
    
    