from PyQt5.QtCore import Qt, QStandardPaths
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame
from qfluentwidgets import TitleLabel, BodyLabel, StrongBodyLabel, SubtitleLabel, PushButton, SettingCardGroup, \
    FolderListSettingCard, PushSettingCard, FluentIcon

from app.common.config import cfg


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
        self.vBoxLayout.addWidget(self.title, 0, Qt.AlignTop)
        self.setLayout(self.vBoxLayout)

        self.downloadFolderCard = PushSettingCard(
            self.tr('Chọn thư mục tải về'),
            FluentIcon.DOWNLOAD,
            self.tr("Chỗ lưu video tải về"),
            cfg.get(cfg.downloadFolder),
            # self.musicInThisPCGroup
        )

        self.musicFolderCard = FolderListSettingCard(
            cfg.musicFolders,
            self.tr("Vị trí chứa video trên máy tính"),
            directory=QStandardPaths.writableLocation(
                QStandardPaths.MusicLocation),
        )
        self.musicFolderCard.addFolderButton.setText("Thêm thư mục nhạc")

        self.vBoxLayout.addWidget(self.downloadFolderCard, 0, Qt.AlignTop)
        self.vBoxLayout.addWidget(self.musicFolderCard, 0, Qt.AlignTop)
