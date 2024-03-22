from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import pyqtSlot, Qt
from qfluentwidgets import PushButton, FluentWindow, ImageLabel, NavigationInterface, NavigationItemPosition, \
    SplitFluentWindow, setFont
from app.view.home_interface import HomeInterface
from qfluentwidgets import FluentIcon as FIF

from app.view.player_interface import PlayerInterface


class MainWindow(FluentWindow):
    instance = None

    def __init__(self):
        super().__init__()
        self.initWindow()
        self.homeInterface = HomeInterface()
        self.playerInterface = PlayerInterface()
        self.__initNavigation()

    def initWindow(self):
        self.setWindowTitle('Music video app')
        self.resize(1140, 780)
        self.setMinimumWidth(860)
        self.navigationInterface.setMenuButtonVisible(True)

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)
        self.show()
        QApplication.processEvents()

    def __initNavigation(self):
        self.addSubInterface(self.homeInterface, FIF.HOME, "Home", NavigationItemPosition.SCROLL)
        self.stackedWidget.addWidget(self.playerInterface)

    def openVideoPlayer(self):
        self.playerInterface.setVideo("https://web.lotuscdn.vn/2024/1/8/89a826e1b25444ed6901435f92388d26_1704675063636-vcsi47dfxd.mp4/720.m3u8")
        self.switchTo(self.playerInterface)

