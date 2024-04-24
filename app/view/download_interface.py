
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWidgets import QWidget,QFrame ,QFileDialog, QHBoxLayout,QVBoxLayout, QLabel, QPushButton, QLineEdit, QApplication, QSizePolicy
from qfluentwidgets import (LineEdit, SpinBox, DoubleSpinBox, TimeEdit, DateTimeEdit, DateEdit,PushSettingCard,
                            TextEdit, FolderValidator, PasswordLineEdit, StrongBodyLabel, MessageBoxBase, SubtitleLabel, ConfigItem, qconfig, QConfig)

from qfluentwidgets import (ScrollArea, PushButton, ToolButton, FluentIcon)
from pytube import YouTube
from queue import Queue
import threading
import os
import subprocess


class DownloadInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName('downloadInterface')
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setSpacing(30)
        self.vBoxLayout.setAlignment(Qt.AlignCenter)
        self.vBoxLayout.setContentsMargins(36, 20, 36, 36)
    
        self.__initWidget()


    def __initWidget(self):
        lineEdit = LineEdit(self)
        lineEdit.setText(self.tr(''))
        lineEdit.setPlaceholderText(self.tr('Nhập link video'))
        lineEdit.setClearButtonEnabled(True)
        lineEdit.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Fixed)

        example_card = ExampleCard(
            title=self.tr("Tải xuống hoặc xem video"),
            widget=lineEdit,
            parent_window=self.window()  # Truyền tham chiếu đến cửa sổ chính
        )

        self.vBoxLayout.addWidget(example_card, 0, Qt.AlignTop)

class ExampleCard(QWidget):
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
        self.watchVideoButton = PushButton(
            self.tr('Xem ngay'), self, FluentIcon.VIDEO)

        self.vBoxLayout = QVBoxLayout(self)
        self.cardLayout = QVBoxLayout(self.card)
        self.topLayout = QHBoxLayout()
        self.bottomLayout = QHBoxLayout(self.sourceWidget)

        self.__initWidget()

    def __initWidget(self):
        self.card.setObjectName('card')
        self.sourceWidget.setObjectName('sourceWidget')
        self.setStyleSheet("""
            ExampleCard {
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

    def onDownloadClicked(self):

        dialog = CustomMessageBox(parent= self.parent_window, link = self.widget.text())  
        dialog.exec_()
        

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
        self.bottomLayout.addWidget(self.watchVideoButton, 0, Qt.AlignCenter)
        self.bottomLayout.addStretch(3)
        self.bottomLayout.setAlignment(Qt.AlignCenter)

class CustomMessageBox(MessageBoxBase):
    """ Custom message box """

    def __init__(self, parent=None, link = None):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel(self.tr('Chọn thư mục lưu trữ'), self)
        self.link = link

        self.downloadFolderCard = PushSettingCard(
            self.tr('Choose folder'),
            FluentIcon.DOWNLOAD,
            self.tr("Download directory"),
            cfg.get(cfg.downloadFolder),
            # self.musicInThisPCGroup
        )

        # add widget to view layout
        self.viewLayout.addWidget(self.titleLabel)

        self.viewLayout.addWidget(self.downloadFolderCard)

        # change the text of button
        self.yesButton.setText(self.tr('Open'))
        self.cancelButton.setText(self.tr('Cancel'))

        self.widget.setMinimumWidth(360)
        # self.yesButton.setDisabled(True)
        # self.urlLineEdit.textChanged.connect(self._validateUrl)
        self.yesButton.clicked.connect(self.downLoadYTB)
        self.downloadFolderCard.clicked.connect(self.__onDownloadFolderCardClicked)

        # Create a queue to hold download tasks
        self.download_queue = Queue()

        # Start a separate thread to process download tasks
        threading.Thread(target=self.process_download_queue, daemon=True).start()

    def _validateUrl(self, text):
        self.yesButton.setEnabled(QUrl(text).isValid())

    def __onDownloadFolderCardClicked(self):
        """ download folder card clicked slot """
        folder = QFileDialog.getExistingDirectory(
            self, self.tr("Choose folder"), "./")
        if not folder or cfg.get(cfg.downloadFolder) == folder:
            return

        cfg.set(cfg.downloadFolder, folder)
        self.downloadFolderCard.setContent(folder)

    def download_m3u8(self, link, location):
        location = os.path.join(location, "video.mp4")
        command = f"ffmpeg -i {link} -c copy -bsf:a aac_adtstoasc {location}"
        subprocess.run(command, shell=True)

    def downloadFromLink(self, link, location):
        try:
            if "youtube" in link:
                youtubeObject = YouTube(link)
                youtubeObject = youtubeObject.streams.get_highest_resolution()
                youtubeObject.download(location)
                print("Download is completed successfully")
            elif "m3u8" in link:
                self.download_m3u8(link, location)


        except Exception as e:
            print(f"An error has occurred: {e}")



    def downLoadYTB(self):
        # Add the download task to the queue
        self.download_queue.put((self.link, cfg.get(cfg.downloadFolder)))

    def process_download_queue(self):
        while True:
            # Get the next download task from the queue
            link, location = self.download_queue.get()

            # Download the video
            self.downloadFromLink(link, location)

            # Mark the task as done
            self.download_queue.task_done()

class Config(QConfig):
    """ Config of application """
    downloadFolder = ConfigItem(
        "Folders", "Download", "app/download", FolderValidator())
cfg = Config()
