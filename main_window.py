from typing import Self

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QGraphicsView, QSlider, QStyle, QHBoxLayout, \
    QLineEdit
from qfluentwidgets import PushButton


class ChildLayout(QVBoxLayout):
    def __init__(self, communication):
        super().__init__()
        self.communication = communication
        self.previousText = ""
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



