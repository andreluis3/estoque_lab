from PyQt6.QtWidgets import (
    QCompleter, QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
)

from controllers import crud
from PyQt6.QtWidgets import QSpinBox
from PyQt6.QtCore import QTimer, Qt
from services.cache import AutocompleteCache
from PyQt6.QtWidgets import QComboBox

class DialogoInserir(QDialog):
    def __init__(self, crud):
        super().__init__()

        self.crud = crud
        self.cache = AutocompleteCache()

        self.setWindowTitle("Adicionar Equipamento")

        self.setup_ui()
        self.setup_autocomplete()
        self.setup_debounce()
        self.setup_signals()
        self.crud = crud

    def setup_ui(self):
        layout = QVBoxLayout()

        self.nome = QLineEdit()
        self.tipo = QLineEdit()
        self.modelo = QLineEdit()
        self.quantidade = QSpinBox()
        self.quantidade.setRange(0, 100000)
        self.caixa = QLineEdit()
        self.localizacao = QLineEdit()
        self.slot = QLineEdit()

        self.botao_salvar = QPushButton("Salvar")
        self.botao_salvar.clicked.connect(self.salvar)

        self.filtro_busca = QComboBox()
        self.filtro_busca.addItems(["nome", "modelo", "nome_modelo"])

        layout.addWidget(QLabel("Nome"))
        layout.addWidget(self.nome)

        layout.addWidget(QLabel("Tipo"))
        layout.addWidget(self.tipo)

        layout.addWidget(QLabel("Modelo"))
        layout.addWidget(self.modelo)

        layout.addWidget(QLabel("Quantidade"))
        layout.addWidget(self.quantidade)

        layout.addWidget(QLabel("Caixa"))
        layout.addWidget(self.caixa)

        layout.addWidget(QLabel("Localização"))
        layout.addWidget(self.localizacao)

        layout.addWidget(QLabel("Slot"))
        layout.addWidget(self.slot)

        layout.addWidget(self.filtro_busca)
        layout.addWidget(self.botao_salvar)

        self.setLayout(layout)
        
    def setup_autocomplete(self):
        self.completer = QCompleter([])
        self.completer.setCaseSensitivity(False)
        self.completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)

        self.nome.setCompleter(self.completer)

        self.completer.activated.connect(self.ao_selecionar_nome)
        
    def setup_debounce(self):
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.setInterval(200)
        self.timer.timeout.connect(self.atualizar_autocomplete)
        
    def setup_signals(self):
        self.nome.textChanged.connect(self.timer.start)
        self.filtro_busca.currentTextChanged.connect(self.atualizar_autocomplete)
        
    def get_dados(self):
        return {
            "nome": self.nome.text(),
            "tipo": self.tipo.text(),
            "modelo": self.modelo.text(),
            "quantidade": int(self.quantidade.value()),
            "caixa": self.caixa.text(),
            "localizacao": self.localizacao.text(),
            "slot": self.slot.text(),
        }

    def salvar(self):
        item = {
            "nome": self.nome.text(),
            "tipo": self.tipo.text(),
            "modelo": self.modelo.text(),
            "quantidade": int(self.quantidade.value()),
            "caixa": self.caixa.text(),
            "localizacao": self.localizacao.text(),
            "slot": self.slot.text(),
        }

        resultado = self.service.inserir_item(item)

        if resultado["status"] == "ok":
            QMessageBox.information(self, "Sucesso", "Item salvo!")
            self.accept()
        else:
            QMessageBox.critical(self, "Erro", resultado["mensagem"])
            
    def configurar_autocomplete(self):
        self.completer = QCompleter([])
        self.completer.setCaseSensitivity(False)
        self.completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)

        self.nome.setCompleter(self.completer)

        self.completer.activated.connect(self.ao_selecionar_nome)
        
        
        
    def atualizar_autocomplete(self):
        texto = self.nome.text().strip()

        if len(texto) < 2:
            return

        filtro = self.filtro_busca.currentText()

        cache_key = f"{filtro}:{texto}"
        cache = self.cache.get(cache_key)

        if cache:
            dados = cache
        else:
            dados = self.crud.buscar_item(texto, filtro)
            self.cache.set(cache_key, dados)

        nomes = [item[1] for item in dados]  # coluna nome

        self.completer.model().setStringList(nomes)
            
    def event_filter(self, obj, event):
        if obj == self.input_nome and event.type() == event.Type.KeyPress:
            if event.key() == Qt.Key.Key_Tab:
                self.completer.complete()
                return True
        return super().event_filter(obj, event)
    
    def ao_selecionar_nome(self, nome):
        item = self.crud.buscar_por_nome(nome)

        if not item:
            return

        # 🔥 preenchimento automático
        self.nome.setText(item["nome"])
        self.tipo.setText(item["tipo"])
        self.caixa.setText(item["caixa"])
        self.localizacao.setText(item["localizacao"])
        self.slot.setText(item["slot"])

        # 🚀 deixar só esses editáveis
        self.tipo.setEnabled(False)
        self.caixa.setEnabled(False)
        self.localizacao.setEnabled(False)
        self.slot.setEnabled(False)
        
    def on_nome_changed(self, text):
        if text.strip() == "":
            self.limpar_campos()
            
    def limpar_campos(self):
        self.tipo.clear()
        self.modelo.clear()
        self.caixa.clear()
        self.localizacao.clear()
        self.slot.clear()

        self.tipo.setEnabled(True)
        self.caixa.setEnabled(True)
        self.localizacao.setEnabled(True)
        self.slot.setEnabled(True)
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Tab:
            self.completer.complete()
            return

        super().keyPressEvent(event)
                    
           