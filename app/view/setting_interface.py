from PyQt5.QtCore import Qt, QStandardPaths
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame
from qfluentwidgets import TitleLabel, BodyLabel, StrongBodyLabel, SubtitleLabel, PushButton, SettingCardGroup, \
    FolderListSettingCard, PushSettingCard

from app.common.config import cfg
from qfluentwidgets import FluentIcon as FIF


class SettingInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("settingInterface")

        self.__initWidget()

    def __initWidget(self):
        self.title = SubtitleLabel("Cài đặt ứng dụng")
        self.title.setContentsMargins(10, 10, 0, 10)
        self.vBoxLayout = QVBoxLayout()
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setAlignment(Qt.AlignTop)
        self.vBoxLayout.addWidget(self.title, Qt.AlignTop)
        self.setLayout(self.vBoxLayout)

        self.selectLocationLayout = QHBoxLayout()
        self.selectLocationLabel = BodyLabel("Chọn thư mục hiển thị video")
        self.selectLocationLabel.setContentsMargins(10, 10, 5, 10)
        self.buttonSelectLocation = PushButton("Chọn thư mục video")
        self.buttonSelectLocation.setMaximumWidth(200)
        self.selectLocationLayout.addWidget(self.selectLocationLabel, Qt.AlignLeft)
        self.selectLocationLayout.addWidget(self.buttonSelectLocation, Qt.AlignRight)

        self.selectDownloadLocationLayout = QHBoxLayout()
        self.selectDownloadLocationLabel = BodyLabel("Thư mục tải xuống video")
        self.selectDownloadLocationLabel.setContentsMargins(10, 5, 5, 10)
        self.buttonSelectDownloadLocation = PushButton("Chọn thư mục tải xuống")
        self.buttonSelectDownloadLocation.setMaximumWidth(200)
        self.selectDownloadLocationLayout.addWidget(self.selectDownloadLocationLabel)
        self.selectDownloadLocationLayout.addWidget(self.buttonSelectDownloadLocation, Qt.AlignRight)

        self.vBoxLayout.addLayout(self.selectLocationLayout)
        self.vBoxLayout.addLayout(self.selectDownloadLocationLayout)

        # music folders
        # self.musicInThisPCGroup = SettingCardGroup(self.tr("Music on this PC"))
        #
        # self.musicFolderCard = FolderListSettingCard(
        #     cfg.musicFolders,
        #     self.tr("Local music library"),
        #     directory=QStandardPaths.writableLocation(
        #         QStandardPaths.MusicLocation),
        # )
        # self.vBoxLayout.addWidget(self.musicFolderCard, Qt.AlignTop)
        # self.downloadFolderCard = PushSettingCard(
        #     self.tr('Choose folder'),
        #     FIF.DOWNLOAD,
        #     self.tr("Download directory"),
        #     cfg.get(cfg.downloadFolder),
        #     self.musicInThisPCGroup
        # )
