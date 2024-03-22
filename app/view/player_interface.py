from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from qfluentwidgets import setTheme, Theme
from qfluentwidgets.multimedia import VideoWidget, StandardMediaPlayBar
from PyQt5.QtCore import QTimer


class MyVideoWidget(VideoWidget):
    """ My custom video widget """

    def __init__(self, parent=None):
        super().__init__(parent)
        # self.isHover = False
        # self.timer = QTimer(self)
        # self.timer.setInterval(3000)  # 3 seconds
        # self.timer.timeout.connect(self.hidePlayBar)

    # def enterEvent(self, event):
    #     """ This function is called when the mouse enters the widget """
    #     self.isHover = True
    #     self.playBar.fadeIn()
    #     self.timer.start()
    #     print("Enter")
    #     super().enterEvent(event)
    #
    # def leaveEvent(self, event):
    #     """ This function is called when the mouse leaves the widget """
    #     self.isHover = False
    #     self.playBar.fadeOut()
    #     self.timer.stop()
    #     super().leaveEvent(event)
    #
    # def mouseMoveEvent(self, event):
    #     """ This function is called when the mouse moves over the widget """
    #     self.timer.start()  # Restart the timer
    #     super().mouseMoveEvent(event)
    #
    # def hidePlayBar(self):
    #     """ This function is called when the timer times out """
    #     if self.isHover:  # Only hide the playbar if the mouse is still over the widget
    #         self.playBar.fadeOut()


class PlayerInterface(QWidget):
    def __init__(self, url=None):
        super().__init__()
        self.vBoxLayout = QVBoxLayout(self)
        self.videoWidget = MyVideoWidget(self)

        if url is not None:
            self.videoWidget.setVideo(QUrl(url))
        # self.videoWidget.setVideo(QUrl(
        #     'https://web.lotuscdn.vn/2024/1/8/89a826e1b25444ed6901435f92388d26_1704675063636-vcsi47dfxd.mp4/720.m3u8'))
        # self.videoWidget.play()

        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.addWidget(self.videoWidget)
        self.setObjectName("playerInterface")

    def setVideo(self, url):
        self.videoWidget.pause()
        self.videoWidget.setVideo(QUrl(url))
        self.videoWidget.player.mediaStatusChanged.connect(self.startVideo)

    def startVideo(self, status):
        if status == QMediaPlayer.LoadedMedia:
            self.videoWidget.player.setPosition(0)
            self.videoWidget.player.play()


