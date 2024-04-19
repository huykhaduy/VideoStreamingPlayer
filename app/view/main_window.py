from PyQt5.QtGui import QIcon, QResizeEvent
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QVBoxLayout
from qfluentwidgets import (NavigationAvatarWidget, NavigationItemPosition, MessageBox, FluentWindow,
                            SplashScreen)
from PyQt5.QtWidgets import QApplication

from PyQt5.QtCore import QUrl, QSize


from app.view.video_interface import VideoInterface
from app.view.download_interface import DownloadInterface

from qfluentwidgets import FluentIcon as FIF

class MainWindow(FluentWindow):
    def __init__(self, communication):
        super().__init__()
        self.communication = communication
        self.initWindow()


        self.videoInterface = VideoInterface()
        self.downloadInterface = DownloadInterface()


        # enable acrylic effect
        self.navigationInterface.setAcrylicEnabled(True)
        self.navigationInterface.setCollapsible(False)
        self.navigationInterface.setExpandWidth(200)


        self.__initWidget()

        self.splashScreen.finish()


    def initWindow(self):
        # self.resize(960, 780)
        self.setMinimumWidth(760)
        self.__setTitlebar()


        # create splash screen
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(106, 106))
        self.splashScreen.raise_()

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)
        self.show()
        QApplication.processEvents()

    def __initWidget(self):
        pos = NavigationItemPosition.SCROLL
        self.addSubInterface(self.videoInterface, FIF.VIDEO,"Video Interface", pos)
        self.addSubInterface(self.downloadInterface, FIF.DOWNLOAD,"Download Interface", pos)



    def __setTitlebar(self):
        self.setWindowTitle("Your Video Player")
        self.setWindowIcon(QIcon(":/icons/app-icon.png"))

