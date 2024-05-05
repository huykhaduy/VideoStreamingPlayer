
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWidgets import QWidget, QFrame, QFileDialog, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QLineEdit, \
    QApplication, QSizePolicy, QMessageBox
from qfluentwidgets import (LineEdit, SpinBox, DoubleSpinBox, TimeEdit, DateTimeEdit, DateEdit,PushSettingCard,
                            TextEdit, FolderValidator, PasswordLineEdit, StrongBodyLabel, DisplayLabel, MessageBoxBase, SubtitleLabel, ConfigItem, qconfig, QConfig)

from qfluentwidgets import (ScrollArea, PushButton, ToolButton, FluentIcon)
from pytube import YouTube
from queue import Queue
import threading
import os
import subprocess
import sys

from app.common.communication import Communication
from app.common.config import cfg
import re


class DownloadInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName('downloadInterface')
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setSpacing(30)
        self.vBoxLayout.setAlignment(Qt.AlignCenter)
        self.vBoxLayout.setContentsMargins(36, 20, 36, 36)
        self.download_queue = Queue()
        threading.Thread(target=self._process_download_queue, daemon=True).start()
        self.__initWidget()
        Communication.instance.downloadCompleted.connect(self._onDownloadCompleted)
        Communication.instance.downloadStarted.connect(self._changeLabelDownloadStarted)
        Communication.instance.addVideoToQueue.connect(self._addToQueue)

    def __initWidget(self):
        self.lineEdit = LineEdit(self)
        self.lineEdit.setText(self.tr(''))
        self.lineEdit.setPlaceholderText(self.tr('Nhập link video'))
        self.lineEdit.setClearButtonEnabled(True)
        self.lineEdit.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Fixed)

        example_card = DownloadCard(
            title=self.tr("Tải xuống video từ YouTube"),
            widget=self.lineEdit,
            parent_window=self.window()  # Truyền tham chiếu đến cửa sổ chính
        )

        self.vBoxLayout.addWidget(example_card, 0, Qt.AlignTop)
        self.label = StrongBodyLabel()
        self.vBoxLayout.addWidget(self.label, 0, Qt.AlignCenter)

    def _onDownloadCompleted(self, link, location):
        print(f"Download completed: {link} -> {location}")
        if sys.platform == "win32":
            os.startfile(location)
        else:
            try:
                subprocess.run(['xdg-open', location])
            except Exception as e:
                QMessageBox.information(None, "Tải thành công", "Địa chỉ: " + location)
        self.label.setText("")

    def _addToQueue(self, link, folder, download_type):
        self.download_queue.put((link, folder, download_type))

    def _changeLabelDownloadStarted(self, link):
        self.label.setText(f"Đang tải xuống video: {link}")

    def _process_download_queue(self):
        while True:
            # Get the next download task from the queue
            link, folder, download_type = self.download_queue.get()

            Communication.instance.downloadStarted.emit(link)

            # Download the video
            file_path = self.download(link, folder, download_type)

            # Mark the task as done
            self.download_queue.task_done()
            Communication.instance.downloadCompleted.emit(link, file_path)

    def download(self, link, location, download_type):
        if download_type == "youtube":
            youtubeObject = YouTube(link)
            youtubeObject = youtubeObject.streams.get_highest_resolution()
            path = youtubeObject.download(location)
            print("Download is completed successfully")
            return path
        elif download_type == "m3u8":
            self.download_m3u8(link, location)


class DownloadCard(QWidget):
    def __init__(self, title, widget: QWidget, stretch=1, parent_window=None):
        super().__init__(parent=parent_window)  # Sử dụng parent_window làm parent
        self.widget = widget
        self.stretch = stretch
        self.parent_window = parent_window  # Lưu tham chiếu đến cửa sổ chính

        self.titleLabel = StrongBodyLabel(title, self)
        self.card = QFrame(self)
        self.sourceWidget = QFrame(self.card)
        self.downloadButton = PushButton(
            self.tr('Tải về ngay'), self, FluentIcon.DOWNLOAD)
        # self.watchVideoButton = PushButton(
        #     self.tr('Xem ngay'), self, FluentIcon.VIDEO)

        self.vBoxLayout = QVBoxLayout(self)
        self.cardLayout = QVBoxLayout(self.card)
        self.topLayout = QHBoxLayout()
        self.bottomLayout = QHBoxLayout(self.sourceWidget)

        self.__initWidget()

    def __initWidget(self):
        self.card.setObjectName('card')
        self.sourceWidget.setObjectName('sourceWidget')
        self.setStyleSheet("""
            DownloadCard {
                background-color: transparent;
                color: white;
            }
            #card {
                border: 1px solid rgb(36, 36, 36);
                border-radius: 10px;
                background-color: rgba(0, 0, 0, 0.1795);
            }
            """)
        
        self.downloadButton.clicked.connect(self.onDownloadClicked)

        self.__initLayout()

    def checkDownloadLink(self, link):
        if self.is_youtube_link(link):
            return 'youtube'
        elif self.is_m3u8_link(link):
            return 'm3u8'
        return ''

    def onDownloadClicked(self):
        # Check download link
        link = self.widget.text()
        download_type = self.checkDownloadLink(link)
        if download_type == "":
            QMessageBox.information(None, "Lỗi", "Link không hợp lệ")
            return

        # If this is the first time the user has downloaded a video
        folder = None
        if cfg.get(cfg.isFirstDownload):
            folder = QFileDialog.getExistingDirectory(
                self, self.tr("Chọn thư mục tải xuống"))
            cfg.set(cfg.isFirstDownload, False)
            cfg.set(cfg.downloadFolder, folder)
        else:
            folder = cfg.get(cfg.downloadFolder)

        Communication.instance.addVideoToQueue.emit(link, folder, download_type)

    def is_youtube_link(self, url):
        # Regular expression pattern for YouTube video URLs
        pattern = r"(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})"

        # Match the pattern against the URL
        match = re.match(pattern, url)

        # If a match is found, it's a valid YouTube link
        return bool(match)

    def is_m3u8_link(self, url):
        # Regular expression pattern for M3U8 playlist URLs
        pattern = r"^(https?|ftp)://[^\s/$.?#].[^\s]*\.m3u8(?:$|\s)"

        # Match the pattern against the URL
        match = re.match(pattern, url)

        # If a match is found, it's a valid M3U8 link
        return bool(match)


    def __initLayout(self):
        self.vBoxLayout.setSizeConstraint(QVBoxLayout.SetMinimumSize)
        self.cardLayout.setSizeConstraint(QVBoxLayout.SetMinimumSize)
        self.topLayout.setSizeConstraint(QHBoxLayout.SetMinimumSize)

        self.vBoxLayout.setSpacing(12)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.topLayout.setContentsMargins(12, 12, 12, 12)
        self.bottomLayout.setContentsMargins(18, 18, 18, 18)
        self.cardLayout.setContentsMargins(0, 0, 0, 0)

        self.vBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignTop)
        self.vBoxLayout.addWidget(self.card, 0, Qt.AlignTop)
        self.vBoxLayout.setAlignment(Qt.AlignTop)

        self.cardLayout.setSpacing(0)
        self.cardLayout.setAlignment(Qt.AlignTop)
        self.cardLayout.addLayout(self.topLayout, 1)
        self.cardLayout.addWidget(self.sourceWidget, 0, Qt.AlignBottom)

        self.widget.setParent(self.card)
        self.topLayout.addWidget(self.widget)
        self.cardLayout.setStretchFactor(self.topLayout, self.stretch)
        if self.stretch == 0:
            self.topLayout.addStretch(1)

        self.widget.show()
        self.bottomLayout.addStretch(3)
        self.bottomLayout.addWidget(self.downloadButton, 0, Qt.AlignCenter)
        self.bottomLayout.addStretch(1)
        # self.bottomLayout.addWidget(self.watchVideoButton, 0, Qt.AlignCenter)
        self.bottomLayout.addStretch(3)
        self.bottomLayout.setAlignment(Qt.AlignCenter)
