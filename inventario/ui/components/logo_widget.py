from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from inventario.utils.paths import IMAGES_DIR

class LogoWidget(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.iniciar_ui()

    def iniciar_ui(self):
        caminho_logo = str(IMAGES_DIR / "Logo_IPT.png")
        pixmap_logo = QPixmap(caminho_logo)
        
        # Redimensionamento suave original
        pixmap_logo = pixmap_logo.scaled(
            120, 120,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.setPixmap(pixmap_logo)
        self.setFixedSize(120, 120)