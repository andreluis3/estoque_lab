
from pathlib import Path

from PyQt6.QtWidgets import (
    QWidget,
    QFrame,
    QLineEdit,
    QPushButton,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QSizePolicy,
)

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QPainter, QColor


class BarraBuscaWidget(QWidget):

    buscar_clicado = pyqtSignal(str)
    texto_alterado = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.iniciar_ui()

    def iniciar_ui(self):

        # Widget responsivo
        self.setMinimumHeight(80)
        self.setMinimumWidth(650)
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed
        )

        # ==========================================
        # LAYOUT PRINCIPAL
        # ==========================================

        layout_principal = QHBoxLayout(self)
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.setSpacing(12)

        # ==========================================
        # GRUPO UNIFICADO DE BUSCA
        # ==========================================

        self.grupo_busca = QFrame(self)
        self.grupo_busca.setObjectName("grupoBusca")

        self.grupo_busca.setMinimumHeight(70)

        self.grupo_busca.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed
        )

        layout_grupo = QHBoxLayout(self.grupo_busca)

        layout_grupo.setContentsMargins(
            20, 0, 16, 0
        )

        layout_grupo.setSpacing(15)

        # ==========================================
        # ÍCONE DA LUPA
        # ==========================================

        self.icone_busca = QLabel()

        self.icone_busca.setFixedSize(22, 22)

        self.icone_busca.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.carregar_icone()

        # ==========================================
        # CAMPO DE TEXTO
        # ==========================================

        self.input_busca = QLineEdit()

        self.input_busca.setObjectName("inputBusca")

        self.input_busca.setPlaceholderText(
            "Digite o nome do componente..."
        )

        self.input_busca.setMinimumHeight(54)

        self.input_busca.setFrame(False)

        self.input_busca.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )

        # Busca automática ao digitar
        self.input_busca.textChanged.connect(
            self.emitir_texto_alterado
        )

        # Feedback visual de foco
        self.input_busca.installEventFilter(self)

        # ==========================================
        # ADICIONANDO AO GRUPO
        # ==========================================

        layout_grupo.addWidget(self.icone_busca)
        layout_grupo.addWidget(self.input_busca, 1)

        # ==========================================
        # BOTÃO BUSCAR
        # ==========================================

        self.botao_busca = QPushButton("Buscar")

        self.botao_busca.setObjectName("botaoBusca")

        self.botao_busca.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.botao_busca.setMinimumSize(100, 60)

        self.botao_busca.clicked.connect(
            self.emitir_busca
        )

        # ==========================================
        # LAYOUT FINAL
        # ==========================================

        layout_principal.addWidget(
            self.grupo_busca,
            1
        )

        layout_principal.addWidget(
            self.botao_busca
        )

        # ==========================================
        # ESTILIZAÇÃO
        # ==========================================

        self.aplicar_estilo()

    # ==========================================
    # CARREGAR E COLORIR ÍCONE
    # ==========================================

    def carregar_icone(self):

        caminho_icone = (
            Path(__file__).resolve().parents[1]
            / "assets"
            / "lupa.png"
        )

        pixmap = QPixmap(str(caminho_icone))

        if pixmap.isNull():
            print(
                f"[BarraBuscaWidget] Ícone não encontrado: "
                f"{caminho_icone}"
            )
            self.icone_busca.setText("⌕")
            self.icone_busca.setStyleSheet(
                "color: #1c7ed6; font-size: 24px;"
            )
            return

        # Redimensionamento
        pixmap = pixmap.scaled(
            22,
            22,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        # Aplicar cor azul preservando transparência
        pixmap_colorido = QPixmap(pixmap.size())
        pixmap_colorido.fill(Qt.GlobalColor.transparent)

        painter = QPainter(pixmap_colorido)

        painter.drawPixmap(0, 0, pixmap)

        painter.setCompositionMode(
            QPainter.CompositionMode.CompositionMode_SourceIn
        )

        painter.fillRect(
            pixmap_colorido.rect(),
            QColor("#1c7ed6")
        )

        painter.end()

        self.icone_busca.setPixmap(pixmap_colorido)

    # ==========================================
    # ESTILO VISUAL
    # ==========================================

    def aplicar_estilo(self):

        self.setStyleSheet("""

            /* =================================
               GRUPO DE BUSCA
            ================================= */

            QFrame#grupoBusca {

                background-color: #1e1e24;

                border: 1px solid #2e2e38;

                border-radius: 10px;
            }

            /* =================================
               CAMPO DE TEXTO
            ================================= */

            QLineEdit#inputBusca {

                background-color: transparent;

                color: #ffffff;

                border: none;

                outline: none;

                font-family: "Segoe UI";

                font-size: 15px;

                padding: 0px;
            }

            QLineEdit#inputBusca::placeholder {

                color: #777780;
            }

            /* =================================
               BOTÃO BUSCAR
            ================================= */

            QPushButton#botaoBusca {

            background-color: #0866c6;

            color: #ffffff;

            border: 1px solid #0078ff;

            border-radius: 10px;

            font-family: "Segoe UI";

            font-size: 15px;

            font-weight: bold;

            padding: 0px 16px;
        }

        QPushButton#botaoBusca:hover {

            background-color: #0078ff;

            border: 1px solid #3399ff;
        }

        QPushButton#botaoBusca:pressed {

            background-color: #0052a3;

            border: 1px solid #004080;
        }

            QPushButton#botaoBusca:disabled {

                background-color: #333340;

                color: #777780;
            }

        """)

        self.atualizar_estado_foco(False)

    # ==========================================
    # FEEDBACK VISUAL DE FOCO
    # ==========================================

    def eventFilter(self, obj, event):

        if obj == self.input_busca:

            if event.type() == event.Type.FocusIn:

                self.atualizar_estado_foco(True)

            elif event.type() == event.Type.FocusOut:

                self.atualizar_estado_foco(False)

        return super().eventFilter(obj, event)

    def atualizar_estado_foco(self, focado):

        if focado:

            self.grupo_busca.setStyleSheet("""

                QFrame#grupoBusca {

                    background-color: #1e1e24;

                    border: 1px solid #1c7ed6;

                    border-radius: 10px;
                }

            """)

        else:

            self.grupo_busca.setStyleSheet("""

                QFrame#grupoBusca {

                    background-color: #1e1e24;

                    border: 1px solid #2e2e38;

                    border-radius: 10px;
                }

            """)

    # ==========================================
    # SINAIS
    # ==========================================

    def emitir_busca(self):

        texto = self.input_busca.text().strip()

        self.buscar_clicado.emit(texto)

    def emitir_texto_alterado(self, texto):

        print("[BarraBusca] Digitando:", texto)

        self.texto_alterado.emit(texto)