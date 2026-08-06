from PyQt6.QtWidgets import QStackedWidget

class Router:
    def __init__(self):
        self.stack = QStackedWidget()
        self.routes = {}

    def register(self, name: str, widget):
        self.routes[name] = widget
        self.stack.addWidget(widget)

    def go(self, name: str):
        if name in self.routes:
            self.stack.setCurrentWidget(self.routes[name])