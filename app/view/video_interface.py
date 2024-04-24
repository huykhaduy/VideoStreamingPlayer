from PyQt5.QtCore import QUrl, QIODevice
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QWidget, QGraphicsView, QVBoxLayout
from qfluentwidgets.multimedia import VideoWidget, StandardMediaPlayBar, MediaPlayer, MediaPlayerBase, \
    SimpleMediaPlayBar
from qfluentwidgets.multimedia.media_play_bar import MediaPlayBarBase

from app.component.play_bar import PlayBar


class VideoInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("videoInterface")
        self.__initWidget()

    def __initWidget(self):
        self.layout = QVBoxLayout()
        
        self.videoWidget = QVideoWidget()   
        self.mediaPlayer = MediaPlayer(self)
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        # self.mediaPlayer.setMedia(QMediaContent(
        #     QUrl("https://d3l1s92l55csfd.cloudfront.net/test/music_video.m3u8")))

        self.playBar = PlayBar()
        # self.playBar.setMediaPlayer(self.mediaPlayer)

        # self.mediaPlayer.setPlaybackRate(1.0)

        self.layout.addWidget(self.videoWidget)
        self.layout.addWidget(self.playBar)
        self.setLayout(self.layout)
        # self.mediaPlayer.play()

    def setVideoModel(self, video=None):
        if video is None:
            return
        self.mediaPlayer.setMedia(QMediaContent(QUrl(video.url)))
        self.playBar.setMediaPlayer(self.mediaPlayer)
        self.mediaPlayer.setPlaybackRate(1.0)
        self.mediaPlayer.play()
