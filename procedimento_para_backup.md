# Procedimento para Restaurar o Database do Estoque_Lab

## Objetivo

Documentar o procedimento para substituir o banco de dados atual do sistema Estoque_Lab por um backup previamente gerado, permitindo recuperar os dados em caso de falhas, corrupção ou necessidade de restauração.

## 1. Localizar o backup desejado

Acessar uma das pastas de backup disponíveis:

* **Computador:** `C:\Users\andressluis\Desktop\Backup_estoque_lab`
* **Servidor:** `I:\LGE\operacao\Areas\CEM\software\EstoqueLab\backup`
* **GitHub:** Repositório destinado ao armazenamento dos backups.

Selecionar o arquivo `.db` correspondente à data desejada.

## 2. Preparar o sistema

Antes de realizar a substituição:

* Fechar completamente o sistema Estoque_Lab.
* Garantir que nenhum outro usuário esteja utilizando o banco de dados.
* Localizar o banco de dados original, `estoque.db`.
* Criar uma cópia de segurança do banco atual, caso ainda não exista.

## 3. Substituir o banco de dados

Localizar o arquivo `estoque.db` utilizado pelo sistema.

Realizar os seguintes procedimentos:

1. Renomear o banco atual para `estoque_antigo.db`, preservando os dados existentes.
2. Copiar o arquivo de backup selecionado para a pasta original do banco de dados.
3. Renomear o arquivo copiado para `estoque.db`.
4. Verificar se não existem arquivos auxiliares antigos (`estoque.db-wal` e `estoque.db-shm`) associados ao banco anterior.

**Importante:** não excluir definitivamente o banco antigo antes de confirmar que a restauração foi realizada corretamente.

## 4. Verificar a restauração

Após substituir o banco:

1. Inicializar o sistema Estoque_Lab.
2. Verificar se a aplicação abre normalmente.
3. Conferir os registros de estoque.
4. Verificar o histórico de movimentações e alterações.
5. Confirmar se os dados correspondem à data do backup selecionado.

Caso ocorram erros, fechar o sistema e avaliar a possibilidade de retornar ao banco anterior.

## 5. Cuidados importantes

* Nunca substituir o banco de dados enquanto o sistema estiver em execução.
* Sempre preservar uma cópia do banco original antes da restauração.
* Utilizar preferencialmente backups previamente verificados quanto à integridade.
* Considerar que a restauração recupera os dados existentes na data do backup, podendo descartar movimentações realizadas posteriormente.
* Em ambientes com múltiplos usuários, garantir que todos os acessos ao banco estejam interrompidos antes da substituição.

---

**Observação:** o arquivo de backup `.db` é uma cópia completa do banco SQLite e pode ser utilizado diretamente após a substituição, desde que seja válido e compatível com a estrutura esperada pelo sistema.
