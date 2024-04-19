from PyQt5.QtCore import QSize, Qt
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtWidgets import QVBoxLayout, QLabel
from qfluentwidgets import FluentStyleSheet, FluentIcon, PushButton
from qfluentwidgets.multimedia import MediaPlayerBase
from qfluentwidgets.multimedia.media_play_bar import MediaPlayBarBase, SimpleMediaPlayBar, MediaPlayBarButton, \
    StandardMediaPlayBar

from app.common.communication import Communication
from app.component.media_base import MediaBase


class FullScreenButton(MediaPlayBarButton):
    def _postInit(self):
        super()._postInit()
        self.setIconSize(QSize(14, 14))
        self.setIcon(FluentIcon.FULL_SCREEN)


class PlayBar(SimpleMediaPlayBar):
    def __init__(self):
        super().__init__()
        # self.hBoxLayout.removeWidget(self.progressSlider)
        # self.hBoxLayout.removeWidget(self.volumeButton)
        #
        self.currentTimerLabel = QLabel("00:00")
        self.endTimerLabel = QLabel("00:00")
        self.currentTimerLabel.setStyleSheet("color: white")
        self.endTimerLabel.setStyleSheet("color: white")
        self.fullScreenButton = FullScreenButton()
        self.fullScreenButton.clicked.connect(self._toggleFullScreen)

        self.hBoxLayout.addWidget(self.currentTimerLabel, 0)
        self.hBoxLayout.addWidget(self.progressSlider, 1)
        self.hBoxLayout.addWidget(self.endTimerLabel, 0)
        self.hBoxLayout.addWidget(self.volumeButton, 0)

        self.addButton(self.fullScreenButton)
        self.playButton.clicked.connect(self.togglePlay)
        FluentStyleSheet.MEDIA_PLAYER.apply(self)

    def togglePlay(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
        else:
            self.player.play()

    def setMediaPlayer(self, mediaPlayer: MediaBase):
        super().setMediaPlayer(mediaPlayer)

        self.player.durationChanged.connect(self._onDurationChanged)
        self.player.positionChanged.connect(self._onPositionChanged)
        self.progressSlider.sliderMoved.disconnect()
        self.progressSlider.sliderPressed.connect(self._startChangePosition)
        self.progressSlider.sliderReleased.connect(self._changePosition)


    def _toggleFullScreen(self):
        Communication.instance.videoFullScreenToggle.emit()

    def _onDurationChanged(self, duration: int):
        self.progressSlider.setMaximum(duration)
        self.endTimerLabel.setText(self._formatTime(duration))

    def _startChangePosition(self):
        self.player.pause()
        self.player.positionChanged.disconnect(self._onPositionChanged)

    def _changePosition(self):
        self.player.setPosition(self.progressSlider.value())
        self.player.positionChanged.connect(self._onPositionChanged)
        self.player.play()

    def _onPositionChanged(self, position: int):
        super()._onPositionChanged(position)
        self.currentTimerLabel.setText(self._formatTime(position))
        print("Position changed", str(position))

    def _startChangePosition(self):
        self.player.pause()

    def _changePosition(self):
        self.player.setPosition(self.progressSlider.value())
        self.player.play()

    def _formatTime(self, time: int):
        time = int(time / 1000)
        s = time % 60
        m = int(time / 60)
        h = int(time / 3600)
        return f'{h}:{m:02}:{s:02}'


# class MyStandardMediaPlayBar(StandardMediaPlayBar):
#     def __init__(self):
#         super().__init__()
#         self.__initWidgets()
#         self.preVideoState = None
#         FluentStyleSheet.MEDIA_PLAYER.apply(self)
#
#     def __initWidgets(self):
#         self.fullScreenButton = FullScreenButton()
#         self.fullScreenButton.clicked.connect(self.toggleFullScreen)
#         self.rightButtonLayout.addWidget(self.fullScreenButton)
#
#     def togglePlay(self):
#         if self.player.state() == QMediaPlayer.PlayingState:
#             self.player.pause()
#         else:
#             self.player.play()
#
#     def toggleFullScreen(self):
#         # Change current window size
#         if self.parent().isFullScreen():
#             self.parent().showNormal()
#         else:
#             self.parent().showFullScreen()
#
#     def setMediaPlayer(self, mediaPlayer: MediaPlayerBase):
#         super().setMediaPlayer(mediaPlayer)
#         self.progressSlider.sliderMoved.disconnect()
#         self.progressSlider.sliderPressed.connect(self.__startChangePosition)
#         self.progressSlider.sliderReleased.connect(self.__changePosition)
#
#
#     def __startChangePosition(self):
#         # self.player.positionChanged.disconnect(self._onPositionChanged)
#         pass
#
#     def __changePosition(self):
#         self.player.setPosition(self.progressSlider.value())
#         # self.player.positionChanged.connect(self._onPositionChanged)
