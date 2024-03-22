import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QLabel, QSizePolicy
from qfluentwidgets import ScrollArea, PushButton, ImageLabel, TextWrap, FlowLayout

from app.common.style_sheet import StyleSheet
import app.view.main_window as main


class VideoCard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.__initWidget()

    def __initWidget(self):
        # Init
        self.imageLabel = ImageLabel("app/resources/images/video.jpg")
        self.titleLabel = QLabel("Video nay cute qua")
        self.subtitleLabel = QLabel("Xoooos")
        self.vBoxLayout = QVBoxLayout(self)
        # Custom
        self.imageLabel.setMinimumSize(250, 140)

        self.imageLabel.setObjectName('imageLabel')
        self.imageLabel.setBorderRadius(10, 10, 10, 10)

        self.titleLabel.setObjectName('titleLabel')
        self.subtitleLabel.setObjectName('subtitleLabel')
        self.vBoxLayout.setObjectName('vBoxLayout')
        self.setObjectName('videoCard')

        self.vBoxLayout.setContentsMargins(5, 5, 5, 5)
        self.vBoxLayout.setSpacing(5)
        self.vBoxLayout.addWidget(self.imageLabel)
        self.vBoxLayout.addWidget(self.titleLabel)
        self.vBoxLayout.addWidget(self.subtitleLabel)

        self.setCursor(QCursor(Qt.PointingHandCursor))
        # self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.imageLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # self.clicked.connect(self.__onClicked)

    def mousePressEvent(self, event):
        main.MainWindow.instance.openVideoPlayer()


class HomeInterface(ScrollArea):
    def __init__(self):
        super().__init__()
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        StyleSheet.HOME_INTERFACE.apply(self)

        self.__initWget()

    def __initWget(self):
        self.view = QWidget(self)
        self.layout = FlowLayout(self.view)
        self.setWidget(self.view)
        self.setWidgetResizable(True)

        self.view.setObjectName('view')
        self.setObjectName('browseInterface')

        for i in range(0, 10):
            self.videoCard = VideoCard()
            self.layout.addWidget(self.videoCard)


