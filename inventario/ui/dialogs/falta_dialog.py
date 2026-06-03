from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel
from inventario.frontend_henrique.projeto.JanelasSegundarias.janela_falta import JanelaItensFalta

class DialogFalta(JanelaItensFalta):
    """
    Herdando temporariamente do layout da JanelaItensFalta antiga para manter conformidade total,
    passando os dados limpos oriundos do Service do sistema principal.
    """
    def __init__(self, dados_alertas, parent=None):
        # Evita quebras injetando a lista esperada pela estrutura interna legada do Henrique
        super().__init__(dados_alertas)