"""
editar_lista_dialog.py — Edição de um item existente da Lista de Compras.

Herda o layout do AdicionarListaDialog e apenas pré-preenche os campos,
evitando duplicar formulário.
"""

from PyQt6.QtCore import pyqtSignal

from inventario.ui.dialogs.adicionar_lista_dialog import AdicionarListaDialog
from inventario.ui.components.mensagem import Mensagem


class EditarListaDialog(AdicionarListaDialog):

    item_editado = pyqtSignal(int, dict)

    def __init__(self, item: dict, parent=None):
        self.item = item
        super().__init__(parent)
        self._preencher_campos()

    def _titulo(self) -> str:
        return "Editar Item da Lista de Compras"

    def _texto_botao_salvar(self) -> str:
        return "Salvar Alterações"

    def _preencher_campos(self):
        self.campo_nome.setText(str(self.item.get("nome") or ""))
        self.campo_tipo.setText(str(self.item.get("tipo") or ""))
        self.campo_modelo.setText(str(self.item.get("modelo") or ""))
        self.campo_quantidade.setValue(int(self.item.get("quantidade") or 1))
        self.campo_observacao.setText(str(self.item.get("observacao") or ""))

    def _salvar(self):
        dados = self._coletar_dados()

        if not dados["nome"]:
            Mensagem.erro(self, "O campo 'Nome' é obrigatório.")
            return

        self.item_editado.emit(int(self.item["id"]), dados)
        self.accept()