from inventario.services.backup_service import BackupService


backup = BackupService()

arquivos = backup.criar_backup()


for arquivo in arquivos:
    print(arquivo)
    
#para executar esse arquivo utilize o comando:
# cd C:\Users\andressluis\Desktop\Algoritmos_IPT\estoque_lab        
#c:/Users/andressluis/Desktop/Algoritmos_IPT/estoque_lab/inventario/testes/teste_backup.py