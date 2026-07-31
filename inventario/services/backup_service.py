import os
import shutil
from datetime import datetime


# ===============================
# Configuração temporária
# depois vem do config.json
# ===============================


SERVIDOR = r"I:\LGE\operacao\Areas\CEM\software\EstoqueLab"

LOCAL = r"C:\Users\Public\Documents\EstoqueLab"


BANCO_ORIGEM = os.path.join(
    "database",
    "estoque.db"
)


class BackupService:


    def __init__(self):

        self.database_path = BANCO_ORIGEM



    # ==================================
    # Descobre onde salvar backup
    # ==================================

    def _criar_pasta_backup(
        self,
        destino
    ):


        pasta = os.path.join(
            destino,
            "backup"
        )


        os.makedirs(
            pasta,
            exist_ok=True
        )


        return pasta



    # ==================================
    # Criar backup
    # ==================================

    def criar_backup(
        self,
        destino="servidor"
    ):


        data = datetime.now().strftime(
            "%d_%m_%Y_%H_%M"
        )


        nome_backup = (
            f"estoque_backup_{data}.db"
        )



        if destino == "servidor":


            if not os.path.exists(SERVIDOR):

                raise Exception(
                    "Servidor indisponível"
                )


            pasta_backup = (
                self._criar_pasta_backup(
                    SERVIDOR
                )
            )



        else:


            pasta_backup = (
                self._criar_pasta_backup(
                    LOCAL
                )
            )



        caminho_backup = os.path.join(
            pasta_backup,
            nome_backup
        )



        shutil.copy2(
            self.database_path,
            caminho_backup
        )



        return caminho_backup