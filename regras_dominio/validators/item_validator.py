class ItemValidator:

    @staticmethod
    def validar(item):

        erros = []

        if not item.get("nome"):
            erros.append("Nome obrigatório.")

        if not item.get("tipo"):
            erros.append("Tipo obrigatório.")

        if item.get("quantidade", 0) < 0:
            erros.append("Quantidade inválida.")

        return erros