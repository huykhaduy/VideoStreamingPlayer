from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QGraphicsView, QSlider, QStyle, QHBoxLayout, \
    QLineEdit
from qfluentwidgets import PushButton


class ChildLayout(QVBoxLayout):
    textChange = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.__initWidget()

    def __initWidget(self):
        self.textInput = QLineEdit()
        self.textInput.textChanged.connect(self.textChange.emit)
        self.addWidget(self.textInput)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ten ung dung")
        self.setGeometry(200, 100, 800, 200)
        self.__initWidget()

    def __initWidget(self):
        # Tạo layout chính cho ứng dụng
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.myText = ""

        # Khởi tạo left layout
        self.leftLayout = ChildLayout()
        self.leftLayout.textChange.connect(self.handleLeftTextChange)

        # Khởi tạo right layout
        self.rightLayout = ChildLayout()
        self.rightLayout.textChange.connect(self.handleRightTextChange)

        # Add left, right layout
        self.layout.addLayout(self.leftLayout)
        self.layout.addLayout(self.rightLayout)

    def handleLeftTextChange(self, text):
        self.rightLayout.textInput.setText(text)

    def handleRightTextChange(self, text):
        self.leftLayout.textInput.setText(text)

# Ví dụ đơn giản hơn
# class OtherWidget(QWidget):
#     dataChange = pyqtSignal(str)
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Ten ung dung 2")
#         self.setGeometry(200, 100, 800, 200)
#         self.__initWidget()
#
#     def __initWidget(self):
#         self.layout = QVBoxLayout()
#         self.setLayout(self.layout)
#
#         self.input = QLineEdit()
#         self.input.textChanged.connect(self.dataChange.emit)
#         self.layout.addWidget(self.input)
#
# class MainWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Ten ung dung")
#         self.setGeometry(200, 100, 800, 200)
#         self.__initWidget()
#
#     def __initWidget(self):
#         self.layout = QVBoxLayout()
#         self.setLayout(self.layout)
#
#         self.button = PushButton("Click me!")
#         self.button.clicked.connect(self.handleButtonClick)
#         self.layout.addWidget(self.button)
#
#     def handleButtonClick(self):
#         self.otherWidget = OtherWidget()
#         self.otherWidget.dataChange.connect(self.handleDataChange)
#         self.otherWidget.show()
#
#     def handleDataChange(self, data):
#         print(data)




