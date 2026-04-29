from PyQt6.QtWidgets import (
    QCompleter, QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
)

from controllers import crud
from PyQt6.QtWidgets import QSpinBox
from PyQt6.QtCore import QStringListModel, QTimer, Qt
from services.cache import AutocompleteCache
from PyQt6.QtWidgets import QComboBox
from PyQt6.QtCore import QStringListModel

class DialogoInserir(QDialog):
    def __init__(self, service):
        super().__init__()

        self.service = service
        self.service = service
        self.crud = service.crud

        self.cache = AutocompleteCache()

        self.setWindowTitle("Adicionar Equipamento")

        self.setup_ui()
        self.setup_autocomplete()
        self.setup_debounce()
        self.setup_signals()

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
        self.model = QStringListModel()

        self.completer = QCompleter()
        self.completer.setModel(self.model)
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
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
        self.nome.textChanged.connect(self.auto_preencher_campos)
        
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

        nomes = []
        
        for item in dados:
            if isinstance(item, dict):
                nomes.append(item.get("nome",""))
            else:
                nomes.append(str(item[1]))  # nome_modelo

        self.model.setStringList(nomes)
        
    def auto_preencher_campos(self, texto):
        texto = texto.strip().lower()

        if len(texto) < 3:
            return

        item = self.service.buscar_por_nome(texto)
        padrao = self.service.buscar_padrao_mais_comum(texto)
        # ========================
        # 1. SE ENCONTROU NO BANCO
        # ========================
        if padrao:
            if not self.tipo.text():
                self.tipo.setText(padrao.get("tipo", ""))

            if not self.caixa.text():
                self.caixa.setText(padrao.get("caixa", ""))

            if not self.localizacao.text():
                self.localizacao.setText(padrao.get("localizacao", ""))

            if not self.slot.text():
                self.slot.setText(padrao.get("slot", ""))
                
        
    
        if item:
            if not self.tipo.text():
                self.tipo.setText(item.get("tipo", ""))

            if not self.caixa.text():
                self.caixa.setText(item.get("caixa", ""))

            if not self.localizacao.text():
                self.localizacao.setText(item.get("localizacao", ""))

            if not self.slot.text():
                self.slot.setText(item.get("slot", ""))

        def set_if_empty(field, value):
            if not field.text():
                field.setText(value)

        if "conector" in texto or "rf" in texto:
            set_if_empty(self.tipo, "Conector de RF")
            set_if_empty(self.caixa, "Maleta preta de conectores de RF")
            set_if_empty(self.localizacao, "Mesa branca")

        elif "resistor" in texto:
            set_if_empty(self.tipo, "Resistor")
            set_if_empty(self.caixa, "Caixa de resistores")
            set_if_empty(self.localizacao, "Armário")

        elif "esp32" in texto:
            set_if_empty(self.tipo, "ESP32")
            set_if_empty(self.caixa, "Caixa microcontroladores")
            set_if_empty(self.localizacao, "Armário")
            set_if_empty(self.slot, "ESP32")

        elif "capacitor" in texto:
            set_if_empty(self.tipo, "Capacitor")
            set_if_empty(self.caixa, "Caixa de capacitores")
            set_if_empty(self.localizacao, "Armário")

        elif "relé" in texto or "rele" in texto:
            set_if_empty(self.tipo, "Relé")
            set_if_empty(self.caixa, "Caixa do relé")
            set_if_empty(self.localizacao, "Armário")

        elif "led" in texto:
            set_if_empty(self.tipo, "LED")
            set_if_empty(self.caixa, "Caixa dos LED")
            set_if_empty(self.localizacao, "Armário")

        elif "diodo" in texto:
            set_if_empty(self.tipo, "Diodo")
            set_if_empty(self.caixa, "Caixa de diodos")
            set_if_empty(self.localizacao, "Armário")


        elif "transistor" in texto or "ci" in texto:
            set_if_empty(self.tipo, "Semicondutor")
            set_if_empty(self.caixa, "Caixa de transistores e CI")
            set_if_empty(self.localizacao, "Armário")

        elif "display" in texto:
            set_if_empty(self.tipo, "Display")
            set_if_empty(self.caixa, "Caixa dos displays")
            set_if_empty(self.localizacao, "Armário")


        elif "protoboard" in texto:
            set_if_empty(self.tipo, "Protoboard")
            set_if_empty(self.caixa, "Caixa da protoboard preta")
            set_if_empty(self.localizacao, "Armário")

    
        elif "modulo" in texto or "sensor" in texto:
            set_if_empty(self.tipo, "Módulo")
            set_if_empty(self.caixa, "Caixa de módulos sensores")
            set_if_empty(self.localizacao, "Armário")

        elif "fusivel" in texto:
            set_if_empty(self.tipo, "Fusível")
            set_if_empty(self.caixa, "Caixa de fusíveis")
            set_if_empty(self.localizacao, "Armário")
            
    
    def event_filter(self, obj, event):
        if obj == self.nome and event.type() == event.Type.KeyPress:
            if event.key() == Qt.Key.Key_Tab:
                self.completer.complete()
                return True
        return super().event_filter(obj, event)
    
    def ao_selecionar_nome(self, nome):
        item = self.service.buscar_por_nome(nome)

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
                    

           