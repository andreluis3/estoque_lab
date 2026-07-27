from PyQt6.QtWidgets import QMessageBox


class Mensagem:


    @staticmethod
    def sucesso(parent, texto):

        msg = QMessageBox(parent)

        msg.setWindowTitle(
            "Sucesso"
        )

        msg.setText(
            texto
        )

        msg.setIcon(
            QMessageBox.Icon.Information
        )

        msg.exec()


    @staticmethod
    def erro(parent, texto):

        msg = QMessageBox(parent)

        msg.setWindowTitle(
            "Erro"
        )

        msg.setText(
            texto
        )

        msg.setIcon(
            QMessageBox.Icon.Critical
        )

        msg.exec()


    @staticmethod
    def aviso(parent, texto):

        msg = QMessageBox(parent)

        msg.setWindowTitle(
            "Atenção"
        )

        msg.setText(
            texto
        )

        msg.setIcon(
            QMessageBox.Icon.Warning
        )

        msg.exec()