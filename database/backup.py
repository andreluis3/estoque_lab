import shutil
from datetime import datetime

def criar_backup():
    origem = "estoque.db"

    data = datetime.now().strftime("%Y%m%d_%H%M%S")

    destino = f"backups/estoque_backup_{data}.db"

    shutil.copy2(origem, destino)

    print(f"Backup criado: {destino}")