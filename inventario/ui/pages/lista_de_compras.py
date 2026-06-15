def carregar_lista_compras(self):

    self.tree.delete(*self.tree.get_children())

    dados = listar_itens()

    for item in dados:

        self.tree.insert(
            "",
            "end",
            values=(
                item[0],  # id
                item[2],  # nome
                item[3],  # modelo
                item[5],  # statusdef adicionar_manual(self):

    adicionar_item(
        item_id=None,
        nome=self.entry_nome.get(),
        modelo=self.entry_modelo.get(),
        quantidade_atual=0,
        observacao=self.entry_obs.get(),
        usuario="André"
    )

    self.carregar_lista_compras()
                item[8]   # data
            )
        )
        
