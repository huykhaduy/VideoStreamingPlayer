from typing import Self

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QGraphicsView, QSlider, QStyle, QHBoxLayout, \
    QLineEdit, QPushButton
from qfluentwidgets import PushButton
import resources

# Cách dùng resources: https://www.pythonguis.com/tutorials/qresource-system/


class ChildLayout(QVBoxLayout):
    def __init__(self, communication):
        super().__init__()
        self.communication = communication
        self.__initWidget()

    def __initWidget(self):
        self.textInput = QLineEdit()
        self.textInput.textChanged.connect(
            lambda text: self.communication.textChange.emit(text)
        )
        self.addWidget(self.textInput)


class MainWindow(QWidget):
    def __init__(self, communication):
        super().__init__()
        self.communication = communication
        self.setWindowTitle("Ten ung dung")
        self.setGeometry(200, 100, 800, 200)
        self.__initWidget()

    def __initWidget(self):
        # Tạo layout chính cho ứng dụng
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.button = PushButton("Click me")
        icon = QIcon(":/icons/cat.png")
        self.button.setIcon(icon)
        self.layout.addWidget(self.button)

        # Khởi tạo left layout
        self.leftLayout = ChildLayout(self.communication)

        # Khởi tạo right layout
        self.rightLayout = ChildLayout(self.communication)

        # Add left, right layout
        self.layout.addLayout(self.leftLayout)
        self.layout.addLayout(self.rightLayout)
        self.communication.textChange.connect(self.handleTextChange)

    def handleTextChange(self, text):
        self.leftLayout.textInput.setText(text)
        self.rightLayout.textInput.setText(text)



