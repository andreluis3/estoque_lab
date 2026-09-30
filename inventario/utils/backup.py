
import os
import shutil
import sqlite3

from datetime import datetime

from inventario.database.db import DB_PATH


# ============================================================
# CONFIGURAÇÕES
# ============================================================

# Backup no computador
BACKUP_LOCAL = r"C:\Users\andressluis\Desktop\Backup_estoque_lab"

# Backup no servidor
BACKUP_SERVIDOR = (
    r"I:\LGE\operacao\Areas\CEM\software\EstoqueLab\backup"
)


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def verificar_integridade(caminho):
    """
    Verifica se o banco SQLite está íntegro.
    """

    try:
        conexao = sqlite3.connect(caminho)

        resultado = conexao.execute(
            "PRAGMA quick_check"
        ).fetchone()

        conexao.close()

        return resultado is not None and resultado[0] == "ok"

    except sqlite3.Error:
        return False


def criar_backup_sqlite(destino):
    """
    Cria uma cópia consistente utilizando o mecanismo
    de backup nativo do SQLite.
    """

    temporario = destino + ".tmp"

    try:

        origem = sqlite3.connect(DB_PATH)
        copia = sqlite3.connect(temporario)

        with copia:
            origem.backup(copia)

        copia.close()
        origem.close()

        if not verificar_integridade(temporario):
            raise sqlite3.DatabaseError(
                "O backup gerado não passou na verificação."
            )

        # Substitui o destino somente após validar
        os.replace(temporario, destino)

        return True

    except Exception as erro:

        print(f"[BACKUP] Erro ao criar backup: {erro}")

        if os.path.exists(temporario):
            os.remove(temporario)

        return False


def copiar_para_destino(origem, destino):
    """
    Copia um backup existente para outro destino,
    validando a cópia antes de considerá-la concluída.
    """

    temporario = destino + ".tmp"

    try:

        shutil.copy2(origem, temporario)

        if not verificar_integridade(temporario):
            raise sqlite3.DatabaseError(
                "A cópia não passou na verificação."
            )

        os.replace(temporario, destino)

        return True

    except Exception as erro:

        print(f"[BACKUP] Erro ao copiar para {destino}: {erro}")

        if os.path.exists(temporario):
            os.remove(temporario)

        return False


# ============================================================
# BACKUP PRINCIPAL
# ============================================================

def fazer_backup():

    if not os.path.exists(DB_PATH):
        print("[BACKUP] Banco de dados não encontrado.")
        return None

    agora = datetime.now()

    data = agora.strftime("%Y-%m-%d")

    nome_arquivo = f"estoque_{data}.db"

    # Pastas organizadas por data
    pasta_local = os.path.join(BACKUP_LOCAL, data)

    pasta_servidor = os.path.join(BACKUP_SERVIDOR, data)

    # Arquivos finais
    arquivo_local = os.path.join(pasta_local, nome_arquivo)

    arquivo_servidor = os.path.join(
        pasta_servidor,
        nome_arquivo
    )

    print("=" * 60)
    print("[BACKUP] Verificando backup diário...")
    print("=" * 60)

    # --------------------------------------------------------
    # 1. CRIAR OU REUTILIZAR BACKUP LOCAL
    # --------------------------------------------------------

    os.makedirs(pasta_local, exist_ok=True)

    if os.path.exists(arquivo_local):

        if verificar_integridade(arquivo_local):

            print("[BACKUP] Já existe backup local válido hoje.")

        else:

            print("[BACKUP] Backup local inválido. Gerando novamente.")

            if not criar_backup_sqlite(arquivo_local):
                return None

    else:

        print("[BACKUP] Primeiro backup do dia.")

        if not criar_backup_sqlite(arquivo_local):
            return None

        print("[BACKUP] Backup local criado com sucesso.")

    # --------------------------------------------------------
    # 2. ENVIAR PARA O SERVIDOR
    # --------------------------------------------------------

    try:

        os.makedirs(pasta_servidor, exist_ok=True)

        if os.path.exists(arquivo_servidor):

            if verificar_integridade(arquivo_servidor):

                print("[BACKUP] Servidor já possui backup válido hoje.")

            else:

                print("[BACKUP] Backup do servidor inválido. Atualizando.")

                if copiar_para_destino(
                    arquivo_local,
                    arquivo_servidor
                ):
                    print("[BACKUP] Servidor atualizado.")

        else:

            if copiar_para_destino(
                arquivo_local,
                arquivo_servidor
            ):
                print("[BACKUP] Backup enviado ao servidor.")

    except Exception as erro:

        print("[BACKUP] Servidor indisponível.")
        print(f"[BACKUP] Detalhes: {erro}")

    # --------------------------------------------------------
    # 3. RESULTADO
    # --------------------------------------------------------

    print("=" * 60)
    print("[BACKUP] Processo finalizado.")
    print(f"[BACKUP] Local: {arquivo_local}")
    print("=" * 60)

    return arquivo_local