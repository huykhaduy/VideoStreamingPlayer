from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from qfluentwidgets import setTheme, Theme
from qfluentwidgets.multimedia import VideoWidget


class PlayerInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.vBoxLayout = QVBoxLayout(self)
        self.videoWidget = VideoWidget(self)

        self.videoWidget.setVideo(QUrl(
            'https://web.lotuscdn.vn/2024/1/8/89a826e1b25444ed6901435f92388d26_1704675063636-vcsi47dfxd.mp4/720.m3u8'))
        self.videoWidget.play()

        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.addWidget(self.videoWidget)
        self.setObjectName("playerInterface")

