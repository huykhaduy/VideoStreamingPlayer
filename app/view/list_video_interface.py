from PyQt5.QtCore import QUrl, QIODevice, Qt, QFile, QStandardPaths
from PyQt5.QtGui import QResizeEvent, QFont, QColor, QPixmap, QMouseEvent, QIcon
from PyQt5.QtWidgets import QWidget, QScrollArea,QFrame ,QFileDialog, QGridLayout,QHBoxLayout,QVBoxLayout, QLabel, QPushButton, QLineEdit, QApplication, QSizePolicy
from qfluentwidgets import (LineEdit, ExpandLayout,SpinBox, DoubleSpinBox, TimeEdit, DateTimeEdit, DateEdit,PushSettingCard,
                            TextEdit, FolderValidator, PasswordLineEdit, StrongBodyLabel, MessageBoxBase, SubtitleLabel, ConfigItem, qconfig, QConfig)

from qfluentwidgets import (ScrollArea, PushButton, ToolButton, FluentIcon, ImageLabel)
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
import requests

from app.common.communication import Communication
from app.model.Video import Video

class ListVideoInterface(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName('listVideoInterface')
        self.view = QWidget(self)

        self.vBoxLayout = QVBoxLayout(self.view)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.vBoxLayout.setAlignment(Qt.AlignTop)
        self.vBoxLayout.setContentsMargins(36, 20, 36, 36)
        self.setStyleSheet("""
            background-color: transparent; 
            color: #FFFFFF; 
            border: none;
        """)
        self._loadData()
        self.__initWidget()
        no_image = QPixmap("app/resources/icons/no-image.png")
        # print(QIcon(":/icons/default_video.jpg"))
        # print(":/icons/app-icon.png")
        VideoCard.no_image = no_image

    def __initWidget(self):
        self.lineEdit = LineEdit(self)
        self.lineEdit.setClearButtonEnabled(True)
        # self.lineEdit.setPlaceholderText(self.tr('Tên video, mô tả, ...'))
        self.lineEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # self.reloadButton = PushButton(FluentIcon.SYNC, "Refresh")
        self.searchButton = PushButton(
            self.tr('Tìm kiếm'), self, FluentIcon.SEARCH)
        
        # Create a horizontal layout
        self.searchWidget = QWidget()
        hBoxLayout = QHBoxLayout()
        hBoxLayout.addWidget(self.lineEdit)
        # hBoxLayout.addWidget(self.reloadButton)
        hBoxLayout.addWidget(self.searchButton)
        
        # Add the horizontal layout to the vertical layout
        self.searchWidget.setLayout(hBoxLayout)
        self.vBoxLayout.addWidget(self.searchWidget, 0, Qt.AlignTop)

        self.liveVideoWidget = QWidget()
        self.liveVBoxLayout = QVBoxLayout()

        self.titleLabel = StrongBodyLabel("Phát sóng trực tiếp", self)
        self.liveVBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignTop)

        self.gridLayout = QGridLayout()
        self.gridLayout.setSpacing(10)
        
        self.liveVBoxLayout.addLayout(self.gridLayout)

        self.showMoreButton = PushButton("Hiển thị thêm", self)
        self.showMoreButton.clicked.connect(self.toggleShowMore)
        self.liveVBoxLayout.addWidget(self.showMoreButton)

        self.liveVideoWidget.setLayout(self.liveVBoxLayout)
        self.vBoxLayout.addWidget(self.liveVideoWidget, 0, Qt.AlignTop)

        # Set initial state
        self.showStates = {'showMore': False, 'showMore2': False}
        self.numRows = 1  # Initial number of rows to display

        self.resizeEvent = self.onResize

        self.vodVideoWidget = QWidget()
        self.vodVBoxLayout = QVBoxLayout()

        self.titleLabel2 = StrongBodyLabel("Các video có sẵn", self)
        self.vodVBoxLayout.addWidget(self.titleLabel2, 0, Qt.AlignTop)
        # self.vodVBoxLayout.addStretch(12)

        self.gridLayout2 = QGridLayout()
        self.gridLayout2.setSpacing(10)
        self.vodVBoxLayout.addLayout(self.gridLayout2)

        self.showMoreButton2 = PushButton("Hiển thị thêm", self)
        self.showMoreButton2.clicked.connect(self.toggleShowMore2)
        self.vodVBoxLayout.addWidget(self.showMoreButton2)

        self.vodVideoWidget.setLayout(self.vodVBoxLayout)
        self.vBoxLayout.addWidget(self.vodVideoWidget, 0, Qt.AlignTop)

        self.searchButton.clicked.connect(self._onSearch)
        # self.reloadButton.clicked.connect(self._onReload)

    def _loadData(self, search=""):
        videos = Video.getListVideo(search)
        self.streaming_videos = [video for video in videos if video.is_streaming]
        self.vod_videos = [video for video in videos if not video.is_streaming]

    def _onReload(self):
        self._loadData("")
        self.updateGridLayouts()

    def _onSearch(self):
        self._loadData(self.lineEdit.text())
        self.updateGridLayouts()

    def toggleShowMore(self):
        self.toggleState('showMore')

    def toggleShowMore2(self):
        self.toggleState('showMore2')

    def toggleState(self, key):
        self.showStates[key] = not self.showStates[key]
        self.updateGridLayouts()

    def updateGridLayouts(self):
        print("Updating grid layouts")
        self.updateGridDisplay()
        self.updateGridLayout(self.gridLayout, self.streaming_videos, 'showMore')
        self.updateGridLayout(self.gridLayout2, self.vod_videos, 'showMore2')
        self.updateShowMoreButton()

    def updateGridDisplay(self):
        if len(self.streaming_videos) > 0:
            self.liveVideoWidget.show()
        else:
            self.liveVideoWidget.hide()

        if len(self.vod_videos) > 0:
            self.vodVideoWidget.show()
        else:
            self.vodVideoWidget.hide()

        self.update()

    def updateGridLayout(self, grid_layout, video_cards_data, show_key):
        self.clearGridLayout(grid_layout)
        # Adjust the number of columns based on the available width
        available_width = self.width() - grid_layout.contentsMargins().left() - grid_layout.contentsMargins().right()
        num_columns = max(1, available_width // 250)  # Minimum width for VideoCard is 250
        available_width -= num_columns * 250
        max_width = 200 + available_width // num_columns
        # print(max_width)
        row = 0
        col = 0
        num_cards = len(video_cards_data)
        max_rows = self.numRows if not self.showStates[show_key] else (num_cards + num_columns - 1) // num_columns
        for i, data in enumerate(video_cards_data):
            if i >= max_rows * num_columns:
                break
            videoCard = VideoCard(data, width=max_width)
            grid_layout.addWidget(videoCard, row, col)
            col += 1
            if col == num_columns:
                row += 1
                col = 0

    def clearGridLayout(self, grid_layout):
        for i in reversed(range(grid_layout.count())):
            widget = grid_layout.itemAt(i).widget()
            grid_layout.removeWidget(widget)
            widget.deleteLater()

    def onResize(self, event):
        print("Resize event")
        self.updateGridLayouts()
        return QScrollArea.resizeEvent(self, event)

    def updateShowMoreButton(self):
        self.showMoreButton.setText("Ẩn đi" if self.showStates['showMore'] else "Hiển thị thêm")
        self.showMoreButton2.setText("Ẩn đi" if self.showStates['showMore2'] else "Hiển thị thêm")




class VideoCard(QWidget):
    pixmap_cache = {}
    no_image = None
    def __init__(self, video = None, width = 200, parent=None):
        super().__init__(parent)
        self.is_hovered = False  # Biến để theo dõi trạng thái khi di chuột vào
        self.setStyleSheet("VideoCard { background-color: #333; border-radius: 5px; padding: 10px; }")
        self.setCursor(Qt.PointingHandCursor)
        self.vBoxLayout = QVBoxLayout(self)
        self.video_image = video.thumbnail
        self.video = video

        # Video image
        self.videoImageLabel = ImageLabel(self)

        # Video title
        self.videoTitleLabel = QLabel(video.title, self)
        self.videoTitleLabel.setStyleSheet("color: white; font-size: 15px;")


        # Views
        self.viewsLabel = QLabel(f"{video.views} lượt xem", self)
        self.viewsLabel.setStyleSheet("color: white; font-size: 12px;")


        # Time
        # self.timeLabel = QLabel(str(video.duration), self)
        # self.timeLabel.setStyleSheet("color: white; font-size: 10px;")

        # Add widgets to layout
        self.vBoxLayout.addWidget(self.videoImageLabel)
        self.vBoxLayout.addWidget(self.videoTitleLabel)
        self.vBoxLayout.addWidget(self.viewsLabel)
        # self.vBoxLayout.addWidget(self.timeLabel)

        self.vBoxLayout.setContentsMargins(5, 5, 5, 5)

        self.setLayout(self.vBoxLayout)

        self.width = width
        self.loadImage(video.thumbnail)

    def loadImage(self, url):
        if url in self.pixmap_cache:
            pixmap = self.pixmap_cache[url]
            scaled_pixmap = pixmap.scaled(self.width, 150, Qt.IgnoreAspectRatio, Qt.FastTransformation)
            self.videoImageLabel.setPixmap(scaled_pixmap)
        else:
            if self.no_image is not None:
                self.no_image = self.no_image.scaled(self.width, 150, Qt.IgnoreAspectRatio, Qt.FastTransformation)
                self.videoImageLabel.setPixmap(self.no_image)
            nam = QNetworkAccessManager(self)
            nam.finished.connect(self.handleFinished)
            nam.get(QNetworkRequest(QUrl(url)))

    def handleFinished(self, reply):
        er = reply.error()

        if er == QNetworkReply.NoError:
            bytes_string = reply.readAll()
            pixmap = QPixmap()
            pixmap.loadFromData(bytes_string)
            scaled_pixmap = pixmap.scaled(self.width, 150, Qt.IgnoreAspectRatio, Qt.FastTransformation)
            self.pixmap_cache[self.video_image] = scaled_pixmap
            scaled_pixmap.height()
            self.videoImageLabel.setPixmap(scaled_pixmap)

    def enterEvent(self, event):
        # Khi con trỏ chuột vào
        self.is_hovered = True
        self.setStyleSheet("VideoCard { background-color: #555; border-radius: 5px; padding: 10px; }")

    def leaveEvent(self, event):
        # Khi con trỏ chuột rời đi
        self.is_hovered = False
        self.setStyleSheet("VideoCard { background-color: #333; border-radius: 5px; padding: 10px; }")

    def mousePressEvent(self, event: QMouseEvent):
        # Xử lý sự kiện khi nhấp chuột vào VideoCard
        if event.button() == Qt.LeftButton:
            Communication.instance.openVideoChanged.emit(self.video.id)
