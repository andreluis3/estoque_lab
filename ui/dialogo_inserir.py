from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit, QPushButton,
    QLabel, QMessageBox, QSpinBox, QComboBox
)
from PyQt6.QtCore import QStringListModel, QTimer, Qt
from PyQt6.QtWidgets import QCompleter


class DialogoInserir(QDialog):
    def __init__(self, crud):
        super().__init__()
        self.crud = crud
        self.setWindowTitle("➕ Adicionar Equipamento")
        self.setMinimumWidth(400)
        self._setup_ui()
        self._setup_autocomplete()
        self._setup_debounce()
        self._setup_signals()

    # ── UI ─────────────────────────────────────────────────────────────────

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        self.nome       = QLineEdit(); self.nome.setPlaceholderText("Nome do componente")
        self.tipo       = QLineEdit(); self.tipo.setPlaceholderText("Ex: Resistor, Capacitor...")
        self.modelo     = QLineEdit(); self.modelo.setPlaceholderText("Código/modelo")
        self.quantidade = QSpinBox();  self.quantidade.setRange(0, 100000)
        self.caixa      = QLineEdit(); self.caixa.setPlaceholderText("Caixa onde está guardado")
        self.localizacao= QLineEdit(); self.localizacao.setPlaceholderText("Ex: Armário, Mesa branca...")
        self.slot       = QLineEdit(); self.slot.setPlaceholderText("Slot (opcional)")

        campos = [
            ("Nome", self.nome),
            ("Tipo", self.tipo),
            ("Modelo", self.modelo),
            ("Quantidade", self.quantidade),
            ("Caixa", self.caixa),
            ("Localização", self.localizacao),
            ("Slot", self.slot),
        ]
        for label, widget in campos:
            layout.addWidget(QLabel(label))
            layout.addWidget(widget)

        self.botao_salvar = QPushButton("💾 Salvar")
        self.botao_salvar.clicked.connect(self._salvar)
        layout.addWidget(self.botao_salvar)

    def _setup_autocomplete(self):
        self.model_completer = QStringListModel()
        self.completer = QCompleter()
        self.completer.setModel(self.model_completer)
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        self.nome.setCompleter(self.completer)
        self.completer.activated.connect(self._ao_selecionar_nome)

    def _setup_debounce(self):
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.setInterval(200)
        self.timer.timeout.connect(self._atualizar_autocomplete)

    def _setup_signals(self):
        self.nome.textChanged.connect(self.timer.start)
        self.nome.textChanged.connect(self._auto_preencher)

    # ── Lógica ─────────────────────────────────────────────────────────────

    def _salvar(self):
        item = {
            "nome":       self.nome.text().strip(),
            "tipo":       self.tipo.text().strip(),
            "modelo":     self.modelo.text().strip(),
            "quantidade": int(self.quantidade.value()),
            "caixa":      self.caixa.text().strip(),
            "localizacao":self.localizacao.text().strip() or "Não informado",
            "slot":       self.slot.text().strip() or "Não informado",
        }

        # Validação básica antes de chamar o crud
        if not item["nome"]:
            QMessageBox.warning(self, "Atenção", "O campo Nome é obrigatório.")
            return
        if not item["tipo"]:
            QMessageBox.warning(self, "Atenção", "O campo Tipo é obrigatório.")
            return
        if not item["caixa"]:
            QMessageBox.warning(self, "Atenção", "O campo Caixa é obrigatório.")
            return

        resultado = self.crud.inserir_item(item, usuario="andre")

        if resultado["status"] == "ok":
            acao = resultado.get("acao", "processado")
            msg = "Item adicionado!" if acao == "inserido" else "Quantidade atualizada no item existente."
            QMessageBox.information(self, "Sucesso", msg)
            self.accept()
        else:
            QMessageBox.critical(self, "Erro", resultado["mensagem"])

    def _atualizar_autocomplete(self):
        texto = self.nome.text().strip()
        if len(texto) < 2:
            return

        resultados = self.crud.buscar_item(texto, "nome")
        nomes = [str(r[1]) for r in resultados]  # coluna 1 = nome
        self.model_completer.setStringList(nomes)

    def _auto_preencher(self, texto):
        """Preenche campos automaticamente ao digitar o nome."""
        texto = texto.strip().lower()
        if len(texto) < 3:
            return

        # Tenta encontrar padrão mais comum no banco
        padrao = self.crud.buscar_padrao_mais_comum(texto)
        if padrao:
            self._set_se_vazio(self.tipo,        padrao.get("tipo", ""))
            self._set_se_vazio(self.caixa,       padrao.get("caixa", ""))
            self._set_se_vazio(self.localizacao, padrao.get("localizacao", ""))
            self._set_se_vazio(self.slot,        padrao.get("slot", ""))

        # Preenchimento por palavra-chave como fallback
        kw = {
            "conector": ("Conector De Rf", "Maleta preta de conectores de RF", "Mesa branca"),
            "resistor": ("Resistor",        "Caixa de resistores",              "Armário"),
            "capacitor":("Capacitor",       "Caixa de capacitores",             "Armário"),
            "esp32":    ("Esp32",           "Caixa microcontroladores",         "Armário"),
            "led":      ("Led",             "Caixa dos LED",                    "Armário"),
            "diodo":    ("Diodo",           "Caixa de diodos",                  "Armário"),
            "transistor":("Semicondutor",   "Caixa de transistores e CI",       "Armário"),
            "display":  ("Display",         "Caixa dos displays",               "Armário"),
            "protoboard":("Protoboard",     "Caixa da protoboard preta",        "Armário"),
            "sensor":   ("Módulo",          "Caixa de módulos sensores",        "Armário"),
            "fusivel":  ("Fusível",         "Caixa de fusíveis",                "Armário"),
            "rele":     ("Relé",            "Caixa do relé",                    "Armário"),
        }
        for chave, (tipo_val, caixa_val, loc_val) in kw.items():
            if chave in texto:
                self._set_se_vazio(self.tipo,        tipo_val)
                self._set_se_vazio(self.caixa,       caixa_val)
                self._set_se_vazio(self.localizacao, loc_val)
                break

    def _ao_selecionar_nome(self, nome):
        """Chamado quando usuário seleciona sugestão do autocomplete."""
        item = self.crud.buscar_por_nome(nome)
        if not item:
            return
        self.nome.setText(item["nome"])
        self.tipo.setText(item["tipo"])
        self.caixa.setText(item["caixa"])
        self.localizacao.setText(item["localizacao"])
        self.slot.setText(item["slot"])

        # Bloqueia campos preenchidos automaticamente
        for campo in [self.tipo, self.caixa, self.localizacao, self.slot]:
            campo.setEnabled(False)

    def _set_se_vazio(self, field: QLineEdit, value: str):
        if not field.text().strip():
            field.setText(value)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Tab:
            self.completer.complete()
            return
        super().keyPressEvent(event)