import os
import sqlite3
import json
from datetime import datetime


class BackupService:


    def __init__(self):

        self.base_dir = os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )


        self.database_path = os.path.join(
            self.base_dir,
            "database",
            "estoque.db"
        )


        self.config = self._carregar_config()



    def _carregar_config(self):

        caminho = os.path.join(
            self.base_dir,
            "config",
            "config.json"
        )


        with open(
            caminho,
            "r",
            encoding="utf-8"
        ) as arquivo:

            return json.load(arquivo)



    def _criar_pasta_backup(self, destino):

        pasta = os.path.join(
            destino,
            "backup"
        )


        os.makedirs(
            pasta,
            exist_ok=True
        )


        return pasta



    def _gerar_backup(self, pasta):

        data = datetime.now().strftime(
            "%d_%m_%Y_%H_%M"
        )


        nome = (
            f"estoque_backup_{data}.db"
        )


        caminho_backup = os.path.join(
            pasta,
            nome
        )


        origem = sqlite3.connect(
            self.database_path
        )


        destino = sqlite3.connect(
            caminho_backup
        )


        with destino:

            origem.backup(
                destino
            )


        origem.close()
        destino.close()


        return caminho_backup



    def criar_backup(self):

        caminhos = self.config["caminhos"]

        backups = []
        # ======================
        # 1 - Backup no projeto
        # ======================

        projeto = os.path.join(
            self.base_dir,
            caminhos["backup_projeto"]
        )


        backups.append(
            self._gerar_backup(
                self._criar_pasta_backup(projeto)
            )
        )



        # ======================
        # 2 - Backup servidor
        # ======================

        servidor = caminhos["servidor"]


        backups.append(
            self._gerar_backup(
                self._criar_pasta_backup(servidor)
            )
        )



        # ======================
        # 3 - Backup local
        # ======================

        local = caminhos["backup_local"]


        backups.append(
            self._gerar_backup(
                self._criar_pasta_backup(local)
            )
        )



        return backups