from PyQt6.QtWidgets import QSpinBox


class QuantidadeSpinBox(QSpinBox):

    def __init__(
        self,
        minimum=0,
        maximum=999999,
        value=1,
        step=1,
        parent=None
    ):
        super().__init__(parent)

        self.setRange(minimum, maximum)
        self.setValue(value)
        self.setSingleStep(step)

        # Setinhas nativas do Qt
        self.setButtonSymbols(
            QSpinBox.ButtonSymbols.UpDownArrows
        )

        # Design e área de clique centralizados
        self.setStyleSheet("""
            QSpinBox {
                background: #222222;
                color: white;
                border: 1px solid #0078ff;
                padding: 4px 22px 4px 5px;
            }

            QSpinBox::up-button {
                subcontrol-origin: border;
                subcontrol-position: top right;
                width: 20px;
            }

            QSpinBox::down-button {
                subcontrol-origin: border;
                subcontrol-position: bottom right;
                width: 20px;
            }
        """)