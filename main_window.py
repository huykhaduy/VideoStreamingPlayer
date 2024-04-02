from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from qfluentwidgets import PushButton, TitleLabel, setTheme, Theme


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        setTheme(Theme.LIGHT)
        self.setGeometry(100, 100, 800, 600)
        self.button = PushButton("Click me")
        self.button.clicked.connect(self.click_button)

        self.label = TitleLabel("Hello")
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

    def click_button(self):
        print("Button clicked")