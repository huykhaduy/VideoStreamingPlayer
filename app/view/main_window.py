from PyQt5.QtGui import QIcon, QResizeEvent
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QVBoxLayout
from qfluentwidgets import (NavigationAvatarWidget, NavigationItemPosition, MessageBox, FluentWindow,
                            SplashScreen)
from PyQt5.QtWidgets import QApplication

from PyQt5.QtCore import QUrl, QSize

from app.common.communication import Communication
from app.model.Video import Video
from app.view.setting_interface import SettingInterface
from app.view.download_interface import DownloadInterface
from app.view.list_video_interface import ListVideoInterface
from app.view.livestream_interface import LivestreamInterface

from qfluentwidgets import FluentIcon as FIF

from app.view.upload_interface import UploadInterface
from app.view.video_interface import VideoInterface


class MainWindow(FluentWindow):
    def __init__(self):
        super().__init__()
        self.initWindow()

        self.downloadInterface = DownloadInterface()
        self.listVideoInterface = ListVideoInterface()
        self.settingInterface = SettingInterface()
        self.videoInterface = VideoInterface()
        self.livestreamInterface = LivestreamInterface()
        self.uploadInterface = UploadInterface()
        # self.localVideoInterface = LocalVideoInterface()


        # enable acrylic effect
        self.navigationInterface.setAcrylicEnabled(True)
        self.navigationInterface.setExpandWidth(180)
        self.navigationInterface.setCollapsible(False)

        self.__initWidget()

        self.splashScreen.finish()

        Communication.instance.videoFullScreenToggle.connect(self.toggleFullScreen)
        Communication.instance.openVideoChanged.connect(self.videoChange)

    def initWindow(self):
        # self.resize(960, 780)
        self.setMinimumWidth(860)
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
        bottom = NavigationItemPosition.BOTTOM
        self.addSubInterface(self.listVideoInterface, FIF.HOME, "Trang chủ", pos)
        self.addSubInterface(self.downloadInterface, FIF.DOWNLOAD, "Tải xuống", pos)
        self.addSubInterface(self.videoInterface, FIF.VIDEO, "Đang xem", pos)
        self.addSubInterface(self.livestreamInterface, FIF.CONNECT, "Streaming", pos)
        self.addSubInterface(self.uploadInterface, FIF.UP, "Upload", pos)

        self.addSubInterface(self.settingInterface, FIF.SETTING, "Cài đặt", bottom)


    def __setTitlebar(self):
        self.setWindowTitle("DP Player")
        # TODO: Fix icon bị lỗi không hiển thị
        self.setWindowIcon(QIcon(":/icons/app-icon.png"))

    def toggleFullScreen(self):
        self.showFullScreen() if not self.isFullScreen() else self.showNormal()

    def videoChange(self, video_id):
        video = Video.getVideoDetail(video_id)
        self.switchToVideo(video)

    def addSubVideoInterface(self, interface):
        self.stackedWidget.addWidget(interface)
        self.stackedWidget.currentChanged.connect(self.onVideoExit)

    def onVideoExit(self, index):
        video_index = self.stackedWidget.indexOf(self.videoInterface)
        if index != video_index:
            self.videoInterface.mediaPlayer.stop()

    def switchToVideo(self, video):
        self.videoInterface.setVideoModel(video)
        self.switchTo(self.videoInterface)
        self.repaint()


