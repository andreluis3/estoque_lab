from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QFrame
)

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

class JanelaBase(QWidget):
    def __init__(self, titulo="Título", subtitulo=""):
        super().__init__()

        # JANELA
        self.resize(1400, 900)
        self.setWindowTitle(titulo)

        self.setStyleSheet("""
            QWidget {
                background-color: #050505;
                color: white;
                font-family: Segoe UI;
            }
        """)

        # CONTAINER PRINCIPAL
        self.container = QFrame(self)

        self.container.setGeometry(
            15,
            15,
            1370,
            860
        )

        self.container.setStyleSheet("""
            QFrame {
                background-color: #0b0b0b;
                border: 2px solid #0078ff;
                border-radius: 22px;
            }
        """)

        # ====================================
        # CABEÇALHO
        # ====================================

        # ÍCONE
        self.icone = QLabel(self.container)

        self.icone.setGeometry(
            35,
            35,
            90,
            90
        )

        self.icone.setStyleSheet("""
            background-color: #111111;
            border-radius: 45px;
            border: 2px solid #0078ff;
        """)

        self.icone.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.icone.setText("📋")

        # TÍTULO
        self.label_titulo = QLabel(
            titulo,
            self.container
        )

        self.label_titulo.setGeometry(
            150,
            35,
            700,
            50
        )

        self.label_titulo.setStyleSheet("""
            color: white;
            font-size: 42px;
            font-weight: bold;
            border: none;
        """)

        # SUBTÍTULO
        self.label_subtitulo = QLabel(
            #subtitulo,
            self.container
        )

        self.label_subtitulo.setGeometry(
            150,
            90,
            700,
            40
        )

        self.label_subtitulo.setStyleSheet("""
            color: #a0a0a0;
            font-size: 24px;
            border: none;
        """)

        # BOTÃO FECHAR
        self.botao_fechar = QPushButton(
            "✕",
            self.container
        )

        self.botao_fechar.setGeometry(
            1240,
            40,
            80,
            80
        )

        self.botao_fechar.setStyleSheet("""
            QPushButton {
                background-color: #161616;
                color: white;
                border-radius: 20px;
                border: 2px solid #2d2d2d;
                font-size: 28px;
            }

            QPushButton:hover {
                background-color: #ff3b3b;
                border: 2px solid #ff5555;
            }
        """)

        self.botao_fechar.clicked.connect(
            self.close
        )

        # LINHA SUPERIOR
        self.linha_topo = QFrame(self.container)

        self.linha_topo.setGeometry(
            20,
            160,
            1330,
            2
        )

        self.linha_topo.setStyleSheet("""
            background-color: #0078ff;
            border: none;
        """)

        # ====================================
        # ÁREA DE CONTEÚDO
        # ====================================

        self.area_conteudo = QFrame(
            self.container
        )

        self.area_conteudo.setGeometry(
            35,
            190,
            1300,
            500
        )

        self.area_conteudo.setStyleSheet("""
            QFrame {
                background-color: #111111;
                border-radius: 22px;
                border: 1px solid #1f1f1f;
            }
        """)

        # ====================================
        # ÁREA INFERIOR
        # ====================================

        self.linha_inferior = QFrame(
            self.container
        )

        self.linha_inferior.setGeometry(
            20,
            720,
            1330,
            2
        )

        self.linha_inferior.setStyleSheet("""
            background-color: #0078ff;
            border: none;
        """)

        # BOTÃO CANCELAR
        self.botao_cancelar = QPushButton(
            "Cancelar",
            self.container
        )

        self.botao_cancelar.setGeometry(
            900,
            750,
            180,
            60
        )

        self.botao_cancelar.setStyleSheet("""
            QPushButton {
                background-color: #1a1a1a;
                color: white;
                border-radius: 18px;
                border: 1px solid #2d2d2d;
                font-size: 22px;
            }

            QPushButton:hover {
                background-color: #303030;
            }
        """)

        self.botao_cancelar.clicked.connect(
            self.close
        )

        # BOTÃO SALVAR
        self.botao_salvar = QPushButton(
            "Salvar",
            self.container
        )

        self.botao_salvar.setGeometry(
            1110,
            750,
            180,
            60
        )

        self.botao_salvar.setStyleSheet("""
            QPushButton {
                background-color: #0078ff;
                color: white;
                border-radius: 18px;
                font-size: 22px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #3399ff;
            }

            QPushButton:pressed {
                background-color: #005ed1;
            }
        """)