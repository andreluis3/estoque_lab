import os
import shutil
from datetime import datetime
from inventario.database.db import DB_PATH

BACKUP_DIR = os.path.join(os.path.dirname(DB_PATH), "backups")
os.makedirs(BACKUP_DIR, exist_ok=True)

def fazer_backup():
    if not os.path.exists(DB_PATH):
        return

    ts = datetime.now().strftime("%d%mY_%H%M%S")
    destino = os.path.join(BACKUP_DIR, f"backup_{ts}.db")

    shutil.copy2(DB_PATH, destino)

    return destino