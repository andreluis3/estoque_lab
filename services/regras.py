def calcular_status(quantidade: int) -> str:
    if quantidade == 0:   return "ZERADO"
    if quantidade < 5:    return "CRÍTICO"
    if quantidade < 10:   return "BAIXO"
    return "OK"