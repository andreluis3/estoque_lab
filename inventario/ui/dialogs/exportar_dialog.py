"""
exportar_dialog.py — Interface de Exportação e Backup do sistema.

A UI não contém regra de negócio: apenas chama ExportService e BackupService,
que já centralizam toda a lógica de geração de planilhas e cópias de backup.
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from inventario.ui.theme.dialog_style import ESTILO_DIALOG
from inventario.ui.components.mensagem import Mensagem
from inventario.services.export_service import ExportService
from inventario.services.backup_service import BackupService


class ExportarDialog(QDialog):
    def __init__(self, estoque_service, parent=None):
        super().__init__(parent)

        # A UI só fia as dependências já existentes — nenhuma lógica nova aqui.
        self.export_service = ExportService(
            estoque_service.item_repo,
            estoque_service.hist_repo
        )
        self.backup_service = BackupService()

        self.setWindowTitle("Exportação e Backup")
        self.setFixedSize(380, 400)
        self.setStyleSheet(ESTILO_DIALOG)
        self._criar_interface()

    # ─── Interface ───────────────────────────────────────────────────────

    def _criar_interface(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(14)

        titulo = QLabel("Exportação e Backup")
        fonte_titulo = QFont()
        fonte_titulo.setPointSize(15)
        fonte_titulo.setBold(True)
        titulo.setFont(fonte_titulo)
        titulo.setStyleSheet("color: #0078ff;")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titulo)

        descricao = QLabel("Escolha a operação desejada.")
        descricao.setStyleSheet("color: #aaaaaa; font-size: 12px;")
        descricao.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(descricao)

        layout.addWidget(self._linha_divisoria())

        # ── Grupo 1: Exportar Planilhas ──
        grupo_exportar = QLabel("Exportar Planilhas")
        grupo_exportar.setStyleSheet("color: white; font-size: 13px; font-weight: bold;")
        layout.addWidget(grupo_exportar)

        botao_exportar_estoque = QPushButton("📄 Exportar Estoque")
        botao_exportar_estoque.clicked.connect(self._exportar_estoque)
        layout.addWidget(botao_exportar_estoque)

        botao_exportar_historico = QPushButton("📜 Exportar Histórico")
        botao_exportar_historico.clicked.connect(self._exportar_historico)
        layout.addWidget(botao_exportar_historico)

        layout.addWidget(self._linha_divisoria())

        # ── Grupo 2: Backup ──
        grupo_backup = QLabel("Backup")
        grupo_backup.setStyleSheet("color: white; font-size: 13px; font-weight: bold;")
        layout.addWidget(grupo_backup)

        botao_backup = QPushButton("💾 Criar Backup")
        botao_backup.setMinimumHeight(44)
        botao_backup.clicked.connect(self._criar_backup)
        layout.addWidget(botao_backup)

        layout.addWidget(self._linha_divisoria())
        layout.addStretch()

        botao_fechar = QPushButton("Fechar")
        botao_fechar.clicked.connect(self.close)
        layout.addWidget(botao_fechar)

    def _linha_divisoria(self) -> QFrame:
        linha = QFrame()
        linha.setFrameShape(QFrame.Shape.HLine)
        linha.setStyleSheet("background-color: #2a2a2a; border: none; max-height: 1px;")
        return linha

    # ─── Ações: Exportação ───────────────────────────────────────────────

    def _exportar_estoque(self):
        try:
            caminho = self.export_service.exportar_estoque_excel()
            Mensagem.sucesso(self, f"Planilha de estoque exportada com sucesso.\n\n{caminho}")
        except Exception as e:
            Mensagem.erro(self, str(e))

    def _exportar_historico(self):
        try:
            caminho = self.export_service.exportar_historico_excel()
            Mensagem.sucesso(self, f"Planilha de histórico exportada com sucesso.\n\n{caminho}")
        except Exception as e:
            Mensagem.erro(self, str(e))

    # ─── Ações: Backup ───────────────────────────────────────────────────

    def _criar_backup(self):
        try:
            self.backup_service.criar_backup()
            Mensagem.sucesso(self, "Backup criado com sucesso.")
        except Exception as e:
            Mensagem.erro(self, str(e))