from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QHBoxLayout, QSizePolicy
from qfluentwidgets import ScrollArea, SubtitleLabel, StrongBodyLabel, PushButton, FluentIcon, LineEdit, ImageLabel
import os


class LocalVideoInterface(ScrollArea):
    def __init__(self):
        super().__init__()
        self.setObjectName("localVideoInterface")
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.view = QWidget()
        self.setWidget(self.view)
        self.vBoxLayout = QVBoxLayout(self.view)
        self.setWidgetResizable(True)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setAlignment(Qt.AlignTop)
        self.setStyleSheet("""
                   background-color: transparent; 
                   color: #FFFFFF; 
                   border: none;
               """)

        self.__initWidget()

    def __initWidget(self):
        self.title = SubtitleLabel("Video trong máy của bạn")
        self.title.setContentsMargins(10, 10, 0, 10)
        self.vBoxLayout.addWidget(self.title, 0, Qt.AlignTop)
        self.__mediaInFolder("D:/Download")

    def __mediaInFolder(self, folder):
        files = os.listdir(folder)
        allowedExtensions = ["mp4", "mkv", "avi", "flv", "wmv", "mov", "ts"]
        files = [file for file in files if file.split(".")[-1] in allowedExtensions]
        for file in files:
            widget = LocalVideoWidget(file, os.path.join(folder, file))
            self.vBoxLayout.addWidget(widget, 0, Qt.AlignTop)

class LocalVideoWidget(QWidget):
    def __init__(self, title, path):
        super().__init__()
        self.path = path
        self.__initWidget()

    def __initWidget(self):
        self.vBoxLayout = QVBoxLayout()
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setAlignment(Qt.AlignTop)
        self.setLayout(self.vBoxLayout)

        self.image = ImageLabel(":/images/no-image.jpg")
        self.image.setFixedSize(200, 150)
        self.title = StrongBodyLabel("Title")
        self.vBoxLayout.addWidget(self.image, 0, Qt.AlignTop)
        self.vBoxLayout.addWidget(self.title, 0, Qt.AlignTop)

