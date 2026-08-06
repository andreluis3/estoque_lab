import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "..", "logs")

os.makedirs(LOG_DIR, exist_ok=True)


def _get_log_file():
    hoje = datetime.now().strftime("%Y-%m-%d")
    return os.path.join(LOG_DIR, f"log_{hoje}.txt")


def registrar_log(usuario: str, acao: str, detalhe: str = ""):
    caminho = _get_log_file()

    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    linha = f"[{agora}] | USER: {usuario} | AÇÃO: {acao} | DETALHE: {detalhe}\n"

    with open(caminho, "a", encoding="utf-8") as f:
        f.write(linha)