"""
resetar_banco.py — Apaga o banco corrompido e reimporta da planilha correta.

USE ESTE SCRIPT AGORA para resolver o banco inconsistente.

Uso:
    python resetar_banco.py
    python resetar_banco.py --caminho planilhas/minha_planilha.xlsx
    python resetar_banco.py --usuario andre
"""

import argparse
import os
import sys
import shutil
from datetime import datetime

# Ajusta o path para rodar da raiz do projeto
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.db import criar_tabela, conectar_db
from services.importador import importar_para_banco


def resetar_e_importar(caminho_planilha: str, usuario: str = "reset"):
    db_path = os.path.join(os.path.dirname(__file__), "database", "estoque.db")
    print(f"🧨 DB RESETADO: {db_path}")

    # 1. Faz backup do banco corrompido (por segurança)
    if os.path.exists(db_path):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup = db_path.replace(".db", f"_backup_{ts}.db")
        shutil.copy2(db_path, backup)
        print(f"💾 Backup salvo em: {backup}")

        os.remove(db_path)
        print(f"🗑️  Banco antigo removido.")

    # 2. Recria as tabelas do zero
    criar_tabela()
    print(f"✅ Banco criado do zero.")

    # 3. Importa da planilha como fonte da verdade
    if not os.path.exists(caminho_planilha):
        print(f"❌ Arquivo não encontrado: {caminho_planilha}")
        sys.exit(1)

    print(f"📥 Importando de: {caminho_planilha}")
    resultado = importar_para_banco(caminho_planilha, usuario=usuario, resetar=False)

    print("\n══════════════════════════════════")
    print("  RESULTADO DA IMPORTAÇÃO")
    print("══════════════════════════════════")
    print(f"  Total na planilha : {resultado['total_planilha']}")
    print(f"  Inseridos         : {resultado['inseridos']}")
    print(f"  Atualizados       : {resultado['atualizados']}")
    print(f"  Erros             : {len(resultado['erros'])}")

    if resultado["erros"]:
        print("\n  ⚠️  Erros encontrados:")
        for e in resultado["erros"]:
            print(f"     - {e['item']}: {e['erro']}")

    # 4. Confirma o total no banco
    conn = conectar_db()
    total_banco = conn.execute("SELECT COUNT(*) FROM itens").fetchone()[0]
    conn.close()
    print(f"\n  ✅ Total no banco agora: {total_banco} itens")
    print("══════════════════════════════════\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reseta o banco e reimporta da planilha.")
    parser.add_argument(
        "--caminho",
        default="planilhas/estoque_lab_formatada.xlsx",
        help="Caminho da planilha Excel (padrão: planilhas/estoque_lab_completa.xlsx)"
    )
    parser.add_argument(
        "--usuario",
        default="reset",
        help="Nome do usuário responsável (para o log)"
    )
    args = parser.parse_args()

    resetar_e_importar(args.caminho, args.usuario)