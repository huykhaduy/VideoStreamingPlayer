from PyQt5.QtCore import QSize, Qt
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtWidgets import QVBoxLayout
from qfluentwidgets import FluentStyleSheet, FluentIcon, PushButton
from qfluentwidgets.multimedia import MediaPlayerBase
from qfluentwidgets.multimedia.media_play_bar import MediaPlayBarBase, SimpleMediaPlayBar, MediaPlayBarButton, \
    StandardMediaPlayBar


class FullScreenButton(MediaPlayBarButton):
    def _postInit(self):
        super()._postInit()
        self.setIconSize(QSize(14, 14))
        self.setIcon(FluentIcon.FULL_SCREEN)


class PlayBar(SimpleMediaPlayBar):
    def __init__(self):
        super().__init__()
        self.preVideoState = None
        self.fullScreenButton = FullScreenButton()
        self.addButton(self.fullScreenButton)
        self.playButton.clicked.connect(self.togglePlay)
        FluentStyleSheet.MEDIA_PLAYER.apply(self)

    def togglePlay(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
        else:
            self.player.play()

    def setMediaPlayer(self, mediaPlayer: MediaPlayerBase):
        super().setMediaPlayer(mediaPlayer)
        self.progressSlider.sliderMoved.disconnect()
        self.progressSlider.sliderPressed.connect(self.__startChangePosition)
        self.progressSlider.sliderReleased.connect(self.__changePosition)

    def __startChangePosition(self):
        # self.player.positionChanged.disconnect(self._onPositionChanged)
        pass

    def __changePosition(self):
        self.player.setPosition(self.progressSlider.value())
        # self.player.positionChanged.connect(self._onPositionChanged)


class MyStandardMediaPlayBar(StandardMediaPlayBar):
    def __init__(self):
        super().__init__()
        self.__initWidgets()
        self.preVideoState = None
        # self.addButton(self.fullScreenButton)
        self.playButton.clicked.connect(self.togglePlay)
        FluentStyleSheet.MEDIA_PLAYER.apply(self)

    def __initWidgets(self):
        self.fullScreenButton = FullScreenButton()
        self.fullScreenButton.clicked.connect(self.toggleFullScreen)
        self.rightButtonLayout.addWidget(self.fullScreenButton)

    def togglePlay(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
        else:
            self.player.play()

    def toggleFullScreen(self):
        # Change current window size
        if self.parent().isFullScreen():
            self.parent().showNormal()
        else:
            self.parent().showFullScreen()

    def setMediaPlayer(self, mediaPlayer: MediaPlayerBase):
        super().setMediaPlayer(mediaPlayer)
        self.progressSlider.sliderMoved.disconnect()
        self.progressSlider.sliderPressed.connect(self.__startChangePosition)
        self.progressSlider.sliderReleased.connect(self.__changePosition)

    def __startChangePosition(self):
        # self.player.positionChanged.disconnect(self._onPositionChanged)
        pass

    def __changePosition(self):
        self.player.setPosition(self.progressSlider.value())
        # self.player.positionChanged.connect(self._onPositionChanged)




