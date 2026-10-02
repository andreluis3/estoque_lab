class ItemNormalizer:

    @staticmethod
    def normalizar(item):

        item["nome"] = item["nome"].strip().title()
        item["tipo"] = item["tipo"].strip().title()
        item["modelo"] = item["modelo"].strip().upper()

        return item