from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QTimer
import webbrowser


# FUNÇÃO COMPRAR
def comprar_item(self, nome_item):

    # REMOVE A PARTE DO ALERTA
    nome_limpo = nome_item.split(
        "está com apenas"
    )[0].strip()

    # FORMATA PARA URL
    pesquisa = nome_limpo.replace(
        " ",
        "+"
    )

    # URL GOOGLE
    url = (
        f"https://www.google.com/search?q=comprar+{pesquisa}"
    )

    # ABRE NAVEGADOR
    webbrowser.open(url)
