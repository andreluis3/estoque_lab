from inventario.services.backup_service import BackupService


backup = BackupService()
arquivo = backup.criar_backup(
    "servidor"
)

print(
    arquivo
)

