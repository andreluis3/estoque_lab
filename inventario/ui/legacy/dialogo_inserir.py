from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit, QPushButton,
    QLabel, QMessageBox, QSpinBox
)
from PyQt6.QtCore import QStringListModel, QTimer, Qt
from PyQt6.QtWidgets import QCompleter

class DialogoInserir(QDialog):
    def __init__(self, estoque_service):
        super().__init__()
        # Agora a UI recebe e conhece APENAS o service orchestrator
        self.estoque_service = estoque_service
        
        self.setWindowTitle("➕ Adicionar Equipamento")
        self.setMinimumWidth(400)
        self._setup_ui()
        self._setup_autocomplete()
        self._setup_debounce()
        self._setup_signals()

    # ── UI LAYOUT (Responsabilidade Única: Renderizar) ─────────────────────

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        self.nome         = QLineEdit(); self.nome.setPlaceholderText("Nome do componente")
        self.tipo         = QLineEdit(); self.tipo.setPlaceholderText("Ex: Resistor, Capacitor...")
        self.modelo       = QLineEdit(); self.modelo.setPlaceholderText("Código/modelo")
        self.quantidade   = QSpinBox();  self.quantidade.setRange(0, 100000)
        self.caixa        = QLineEdit(); self.caixa.setPlaceholderText("Caixa onde está guardado")
        self.localizacao  = QLineEdit(); self.localizacao.setPlaceholderText("Ex: Armário, Mesa branca...")
        self.slot         = QLineEdit(); self.slot.setPlaceholderText("Slot (opcional)")

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

    # ── CAPTURA E FLUXO (UI Pura) ──────────────────────────────────────────

    def _coletar_dados(self) -> dict:
        """[CHECKLIST] Extrai os dados crus digitados na tela em formato de dicionário."""
        return {
            "nome":        self.nome.text(),
            "tipo":        self.tipo.text(),
            "modelo":      self.modelo.text(),
            "quantidade":  int(self.quantidade.value()),
            "caixa":       self.caixa.text(),
            "localizacao": self.localizacao.text(),
            "slot":        self.slot.text(),
        }

    def _salvar(self):
        # Captura os dados brutos usando a função centralizada
        dados_item = self._coletar_dados()

        try:
            # Envia para a camada de serviço processar tudo.
            # O usuário "andre" pode ser dinâmico depois.
            resultado = self.estoque_service.registrar_item(dados_item, usuario="andre")
            
            if resultado.get("acao") == "atualizado":
                msg = "Quantidade acumulada e atualizada no item existente!"
            else:
                msg = "Novo item inserido com sucesso no estoque!"
                
            QMessageBox.information(self, "Sucesso", msg)
            self.accept()

        except ValueError as e:
            # Captura erros de validação disparados pelo service/validador externo
            QMessageBox.warning(self, "Aviso de Validação", str(e))
        except Exception as e:
            # Qualquer outra falha de banco ou sistema
            QMessageBox.critical(self, "Erro Operacional", f"Falha ao salvar: {str(e)}")

    def _atualizar_autocomplete(self):
        texto = self.nome.text().strip()
        if len(texto) < 2:
            return

        # Busca delegada ao serviço
        nomes = self.estoque_service.obter_sugestoes_por_termo(texto)
        self.model_completer.setStringList(nomes)

    def _auto_preencher(self, texto):
        if len(texto.strip()) < 3:
            return

        # Pede a previsão de atributos ao serviço (que consulta o ItemRules internamente)
        sugestao = self.estoque_service.prever_atributos_por_nome(texto)

        self._set_se_vazio(self.tipo, sugestao.get("tipo", ""))
        self._set_se_vazio(self.caixa, sugestao.get("caixa", ""))
        self._set_se_vazio(self.localizacao, sugestao.get("localizacao", ""))
        self._set_se_vazio(self.slot, sugestao.get("slot", ""))

    def _ao_selecionar_nome(self, nome):
        """Preenche o formulário se o item já existir no histórico do banco."""
        item = self.estoque_service.buscar_detalhes_por_nome(nome)
        if not item:
            return
            
        self.nome.setText(item.get("nome", ""))
        self.tipo.setText(item.get("tipo", ""))
        self.caixa.setText(item.get("caixa", ""))
        self.localizacao.setText(item.get("localizacao", ""))
        self.slot.setText(item.get("slot", ""))

        # Trava os campos estruturais para manter a consistência do item original
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