class ItemRules:
    print("ITEM RULES CARREGADO")
    MAPA_REGRAS = {

        "conector n": {
            "tipo": "Conectores de RF",
            "caixa": "Maleta preta de conectores de RF",
            "localizacao": "Mesa branca",
            "slot": "Slot Geral Único"
        },

        "conector sma": {
            "tipo": "Conectores de RF",
            "caixa": "Maleta preta de conectores de RF",
            "localizacao": "Mesa branca",
            "slot": "Slot Geral Único"
        },

        "resistor": {
            "tipo": "Resistor",
            "caixa": "Caixa de resistores",
            "localizacao": "Armário",
            "slot": ""
        },

        "capacitor": {
            "tipo": "Capacitor",
            "caixa": "Caixa de capacitores",
            "localizacao": "Armário",
            "slot": ""
        },

        "esp32": {
            "tipo": "Microcontrolador",
            "caixa": "Caixa microcontroladores",
            "localizacao": "Armário",
            "slot": ""
        },
    }

    @classmethod
    def aplicar_regras(cls, item):

        nome = item.get("nome", "").lower()

        for chave, regras in cls.MAPA_REGRAS.items():

            if chave in nome:

                for campo, valor in regras.items():

                    if not item.get(campo):
                        item[campo] = valor

                break

        return item