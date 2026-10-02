import re


class ItemRules:
    print(" [DOMÍNIO] ITEM RULES CARREGADO COM SUCESSO")

    # Mapeamento estrito de padrões (RegEx) para preenchimento inteligente de domínio
    REGRAS_MAPEADAS = {
        "conectores_rf_transparente": {
            "padroes": [r"rf.*transparente", r"conector.*transparente"],
            "valores": {
                "tipo": "Conectores de RF",
                "caixa": "Conectores de rf transparente",
                "localizacao": "Mesa branca",
                "slot": "Geral"
            }
        },
        "conectores_rf_diario": {
            "padroes": [r"conector\s+n\b", r"conector\s+sma\b", r"\brf\b", r"atenuador\s+rf", r"\bsma\b"],
            "valores": {
                "tipo": "Conectores de RF",
                "caixa": "Maleta preta de conectores de RF",
                "localizacao": "Mesa branca",
                "slot": "Slot Geral Único"
            }
        },
        "resistores": {
            "padroes": [r"\bresistor\b", r"\bohm\b", r"Ω", r"\bpotenciometro\b"],
            "valores": {
                "tipo": "Resistor",
                "caixa": "Caixa de resistores",
                "localizacao": "Armário",
                "slot": "Geral"
            }
        },
        "capacitores": {
            "padroes": [r"\bcapacitor\b", r"\bcap\b", r"\beletrolitico\b", r"\bceramico\b"],
            "valores": {
                "tipo": "Capacitor",
                "caixa": "Caixa de capacitores",
                "localizacao": "Armário",
                "slot": "Geral"
            }
        },
        "diodos": {
            "padroes": [r"\bdiodo\b", r"\bzener\b", r"\b1n4148\b", r"\b1n4007\b", r"\b1n5406\b"],
            "valores": {
                "tipo": "Diodo",
                "caixa": "Caixa de diodos",
                "localizacao": "Armário",
                "slot": "Geral"
            }
        },
        "fusiveis": {
            "padroes": [r"\bfusivel\b", r"\bfusível\b"],
            "valores": {
                "tipo": "Fusível",
                "caixa": "Caixa de fusíveis",
                "localizacao": "Armário",
                "slot": "Geral"
            }
        },
        "reguladores": {
            "padroes": [r"regulador\s+de\s+tenso\b", r"regulador\s+de\s+tensao\b", r"\blm78", r"\bams1117\b"],
            "valores": {
                "tipo": "Regulador de Tensão",
                "caixa": "Caixa de reguladores de tensão",
                "localizacao": "Armário",
                "slot": "Geral"
            }
        },
        "leds": {
            "padroes": [r"\bled\b", r"\bleds\b", r"led\s+difuso"],
            "valores": {
                "tipo": "LED",
                "caixa": "Caixa de leds",
                "localizacao": "Armário",
                "slot": "Geral"
            }
        },
        "microcontroladores": {
            "padroes": [r"\besp32\b", r"\barduino\b", r"\bstm32\b", r"\bnode_mcu\b", r"\bpic\b"],
            "valores": {
                "tipo": "Microcontrolador",
                "caixa": "Caixa microcontroladores",
                "localizacao": "Armário",
                "slot": "Gaveta Principal"
            }
        },
        "modulos": {
            "padroes": [r"\bmodulo\b", r"\bmódulo\b"],
            "valores": {
                "tipo": "Módulo",
                "caixa": "Caixa de módulo",
                "localizacao": "Armário",
                "slot": "Geral"
            }
        },
        "circuitos_integrados": {
            "padroes": [r"\bci\b", r"\bne555\b", r"\blm358\b", r"circuito\s+integrado", r"amplificador\s+operacional"],
            "valores": {
                "tipo": "Circuito Integrado",
                "caixa": "Caixa de transistores e dos cis",
                "localizacao": "Armário",
                "slot": "Geral"
            }
        },
        "transistores": {
            "padroes": [r"\btransistor\b", r"\bmosfet\b", r"\bbc547\b", r"\bbc548\b", r"\btip41\b", r"\b2n3904\b"],
            "valores": {
                "tipo": "Transistor",
                "caixa": "Caixa de transistores azul",
                "localizacao": "Armário",
                "slot": "Geral"
            }
        },
        "sensores": {
            "padroes": [r"\bsensor\b", r"\bmlx90614\b", r"\bldr\b", r"\bultrassonico\b", r"\bdht11\b"],
            "valores": {
                "tipo": "Sensor",
                "caixa": "CX-SENSORES",
                "localizacao": "Armário Vertical A",
                "slot": "Gaveta B"
            }
        },
        "displays": {
            "padroes": [r"\bdisplay\b", r"\blcd\b", r"\boled\b", r"\btft\b"],
            "valores": {
                "tipo": "Display",
                "caixa": "CX-DISPLAYS",
                "localizacao": "Bancada Principal",
                "slot": "Organizador 01"
            }
        }
    }

    @classmethod
    def aplicar_regras(cls, item_parcial: dict) -> dict:
        """
        Analisa textualmente o nome do item usando RegEx e infere a melhor 
        combinação de Tipo, Caixa, Localização e Slot para o laboratório.
        """
        nome_alvo = str(item_parcial.get("nome", "")).lower().strip()
        
        sugestao = {
            "tipo": "",
            "caixa": "",
            "localizacao": "",
            "slot": ""
        }

        if not nome_alvo:
            return sugestao

        # Varre as chaves ordenadas. Note que 'conectores_rf_transparente' vem ANTES 
        # de 'conectores_rf_diario' para capturar a regra mais específica primeiro!
        for categoria, configuracao in cls.REGRAS_MAPEADAS.items():
            for padrao in configuracao["padroes"]:
                if re.search(padrao, nome_alvo):
                    valores_alvo = configuracao["valores"]
                    
                    sugestao["tipo"] = valores_alvo["tipo"]
                    sugestao["caixa"] = valores_alvo["caixa"]
                    sugestao["localizacao"] = valores_alvo["localizacao"]
                    sugestao["slot"] = valores_alvo["slot"]
                    
                    return sugestao 

        return sugestao