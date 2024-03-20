# import sys
#
# from PyQt5.QtWidgets import (
#     QApplication, QDialog, QMainWindow, QMessageBox
# )
# from PyQt5.uic import loadUi
#
# from main_window_ui import Ui_Form
#
# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.ui = Ui_Form()
#         self.ui.setupUi(self)
#
# def main():
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec_())
#
# if __name__ == "__main__":
#     main()
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QApplication, QMainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.StreamPlayback)

        self.videoWidget = QVideoWidget()

        self.setCentralWidget(self.videoWidget)

        self.mediaPlayer.setVideoOutput(self.videoWidget)

        url = 'https://web.lotuscdn.vn/2024/1/8/89a826e1b25444ed6901435f92388d26_1704675063636-vcsi47dfxd.mp4/360.m3u8'
        self.mediaPlayer.setMedia(QMediaContent(QUrl(url)))

        self.mediaPlayer.play()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())