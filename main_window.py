from PyQt5 import uic
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QGraphicsView, QSlider, QStyle
from qfluentwidgets import PushButton

# 3. Tạo màn hình video với pyqt5
# Tài liệu: https://stackoverflow.com/questions/57842104/how-to-play-videos-in-pyqt

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("designer.ui", self)

        # Lấy các widget từ ui
        self.videoWidget = self.findChild(QVideoWidget, "widget")
        self.playButton = self.findChild(PushButton, "playButton")

        self.nextButton = self.findChild(PushButton, "nextButton")
        self.prevButton = self.findChild(PushButton, "prevButton")
        self.slider = self.findChild(QSlider, "slider")

        self.playButton.clicked.connect(self.play)

        # Media player là một class dùng để play video, không có giao diện
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        # Set link video
        self.mediaPlayer.setMedia(QMediaContent(
            QUrl("https://web.lotuscdn.vn/2024/1/8/89a826e1b25444ed6901435f92388d26_1704675063636-vcsi47dfxd.mp4/720.m3u8")))
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)

        self.slider.sliderMoved.connect(self.changeSiderValue)

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def changeSiderValue(self):
        print("Sider change"+str(self.slider.value()))
        self.mediaPlayer.setPosition(self.slider.value())

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay))

    def positionChanged(self, position):
        self.slider.setValue(position)

    def durationChanged(self, duration):
        self.slider.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def handleError(self):
        self.playButton.setEnabled(False)




