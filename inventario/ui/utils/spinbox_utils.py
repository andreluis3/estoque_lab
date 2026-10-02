from PyQt6.QtWidgets import QSpinBox


def configure_quantity_spinbox(
    spinbox: QSpinBox,
    minimum: int,
    maximum: int,
    value: int,
    step: int = 1,
    enabled: bool = True,
    read_only: bool = False,
) -> None:
    spinbox.setRange(minimum, maximum)
    spinbox.setValue(value)
    spinbox.setSingleStep(step)
    spinbox.setButtonSymbols(QSpinBox.ButtonSymbols.UpDownArrows)
    spinbox.setEnabled(enabled)
    spinbox.setReadOnly(read_only)