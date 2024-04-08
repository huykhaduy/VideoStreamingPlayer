from PyQt5.QtCore import QUrl, QIODevice
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QWidget, QGraphicsView, QVBoxLayout
from qfluentwidgets.multimedia import VideoWidget, StandardMediaPlayBar, MediaPlayer, MediaPlayerBase, \
    SimpleMediaPlayBar
from qfluentwidgets.multimedia.media_play_bar import MediaPlayBarBase

from app.component.play_bar import PlayBar, FullScreenButton, MyStandardMediaPlayBar


class VideoInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("videoInterface")
        self.__initWidget()

    def __initWidget(self):
        # self.setMinimumSize(800, 600)
        self.layout = QVBoxLayout()

        self.videoWidget = QVideoWidget()
        self.mediaPlayer = MediaPlayer(self)
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.mediaPlayer.setMedia(QMediaContent(
            QUrl("https://web.lotuscdn.vn/2024/1/8/89a826e1b25444ed6901435f92388d26_1704675063636-vcsi47dfxd.mp4/720.m3u8")))

        self.playBar = PlayBar()
        self.playBar.setMediaPlayer(self.mediaPlayer)

        self.mediaPlayer.setPlaybackRate(1.0)

        self.layout.addWidget(self.videoWidget)
        self.layout.addWidget(self.playBar)
        self.setLayout(self.layout)
        self.mediaPlayer.play()