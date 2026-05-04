import re

def normalizar(texto):
    if not texto:
        return ""

    texto = str(texto)

    # remove espaços invisíveis
    texto = texto.replace("\xa0", " ")

    # remove múltiplos espaços
    texto = re.sub(r"\s+", " ", texto)

    return texto.strip().lower()