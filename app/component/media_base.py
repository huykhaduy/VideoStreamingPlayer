from PyQt5.QtCore import pyqtSignal
from qfluentwidgets.multimedia import MediaPlayerBase


class MediaBase(MediaPlayerBase):
    bufferStatusChanged = pyqtSignal(int)