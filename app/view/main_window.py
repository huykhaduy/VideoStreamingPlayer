from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import pyqtSlot, Qt
from qfluentwidgets import PushButton, FluentWindow, ImageLabel, NavigationInterface, NavigationItemPosition, \
    SplitFluentWindow, setFont
from app.view.home_interface import HomeInterface
from qfluentwidgets import FluentIcon as FIF

from app.view.player_interface import PlayerInterface


class MainWindow(FluentWindow):
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
        self.addSubInterface(self.playerInterface, FIF.PLAY, "Media", NavigationItemPosition.SCROLL)
