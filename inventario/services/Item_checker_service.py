# services/item_checker_service.py

import re
import unicodedata
from inventario.utils.sinonimos_componentes import SINONIMOS

class ItemCheckerService:


    @staticmethod
    def normalizar_texto(valor):

        if not valor:
            return ""

        valor = str(valor).lower().strip()

        # Remove acentos
        valor = unicodedata.normalize("NFD", valor)
        valor = "".join(
            c for c in valor
            if unicodedata.category(c) != "Mn"
        )

        for antigo, novo in SINONIMOS.items():
            valor = valor.replace(
                antigo,
                novo.lower()
            )

        # Remove espaços repetidos
        valor = re.sub(r"\s+", " ", valor)

        return valor.strip()

    @classmethod
    def comparar_item(cls, item1, item2):

        campos = [

            "nome",
            "tipo",
            "modelo",
            "caixa",
            "localizacao",
            "slot"

        ]


        for campo in campos:

            valor1 = cls.normalizar_texto(
                item1.get(campo)
            )

            valor2 = cls.normalizar_texto(
                item2.get(campo)
            )


            if valor1 != valor2:
                return False


        return True
    
    
    @classmethod
    def gerar_chave_item(cls, item: dict) -> str:

        campos = [
            "nome",
            "tipo",
            "modelo",
            "caixa",
            "localizacao",
            "slot"
        ]

        chave = "_".join(
            cls.normalizar_texto(
                item.get(campo, "")
            )
            for campo in campos
        )

        return chave
    
    @classmethod
    def calcular_semelhanca(cls, item1, item2):
        """
        Calcula a semelhança entre dois itens.
        Retorna um valor entre 0 e 1, onde 1 significa que os itens são iguais.
        """
        campos = [
            "nome",
            "tipo",
            "modelo",
            "caixa",
            "localizacao",
            "slot"
        ]

        total_campos = len(campos)
        campos_iguais = 0

        for campo in campos:
            valor1 = cls.normalizar_texto(
            item1.get(campo)  )
            valor2 = cls.normalizar_texto(
                item2.get(campo)
            )

            if valor1 == valor2:
                campos_iguais += 1

        return campos_iguais / total_campos if total_campos > 0 else 0.0
    
    @classmethod
    def obter_diferencas(cls, item1, item2):
        """
        Retorna um dicionário com as diferenças entre dois itens.
        As chaves do dicionário são os campos que diferem, e os valores são tuplas
        contendo (valor_item1, valor_item2).
        """
        campos = [
            "nome",
            "tipo",
            "modelo",
            "caixa",
            "localizacao",
            "slot"
        ]

        diferencas = {}

        for campo in campos:
            valor1 = cls.normalizar_texto(
                item1.get(campo)
            )
            valor2 = cls.normalizar_texto(
                item2.get(campo)
            )

            if valor1 != valor2:
                diferencas[campo] = (valor1, valor2)

        return diferencas
    
    @classmethod
    def localizar_item_existente(cls, itens, dados_novo):

        melhor_item = None
        maior_semelhanca = 0


        for item in itens:

            semelhanca = cls.calcular_semelhanca(
                item,
                dados_novo
            )


            if semelhanca > maior_semelhanca:

                maior_semelhanca = semelhanca
                melhor_item = item


        if maior_semelhanca == 1:
            return melhor_item


        return None