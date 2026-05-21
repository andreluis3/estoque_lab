from datetime import datetime
import re

def senha_valida(senha_digitada: str) -> bool:
    senha = senha_digitada.strip()

    hoje = datetime.now()
    senha_formatada = hoje.strftime("%d/%m/%y")   
    senha_numerica  = hoje.strftime("%d%m%y")     

    # remove tudo que não é número
    senha_limpa = re.sub(r"\D", "", senha)
    return senha == senha_formatada or senha_limpa == senha_numerica


def autenticar(usuario: str, senha: str) -> bool:
    if not usuario.strip():
        return False

    if not senha_valida(senha):
        return False

    return True