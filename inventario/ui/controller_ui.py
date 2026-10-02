class UIController:
    def __init__(self, service):
        self.service = service
        self.janelas_abertas = []

    def abrir_itens_falta(self):
        from inventario.ui.pages.janela_itens_falta import JanelaItensFalta

        janela = JanelaItensFalta(self.service.get_alertas())
        janela.show()

        self.janelas_abertas.append(janela)