from PyQt5.QtCore import QUrl, QIODevice, Qt, QFile, QStandardPaths
from PyQt5.QtGui import QResizeEvent, QFont, QColor, QPixmap,QMouseEvent
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QWidget, QScrollArea,QFrame ,QFileDialog, QGridLayout,QHBoxLayout,QVBoxLayout, QLabel, QPushButton, QLineEdit, QApplication, QSizePolicy
from qfluentwidgets import (LineEdit, ExpandLayout,SpinBox, DoubleSpinBox, TimeEdit, DateTimeEdit, DateEdit,PushSettingCard,
                            TextEdit, FolderValidator, PasswordLineEdit, StrongBodyLabel, MessageBoxBase, SubtitleLabel, ConfigItem, qconfig, QConfig)
from app.component.play_bar import PlayBar, FullScreenButton, MyStandardMediaPlayBar

from qfluentwidgets import (ScrollArea, PushButton, ToolButton, FluentIcon, )
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply


class ListVideoInterface(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName('listVideoInterface')
        self.view = QWidget(self)

        self.vBoxLayout = QVBoxLayout(self.view)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.vBoxLayout.setSpacing(30)
        self.vBoxLayout.setAlignment(Qt.AlignTop)
        self.vBoxLayout.setContentsMargins(36, 20, 36, 36)
        self.setStyleSheet("""
            background-color: transparent; 
            color: #FFFFFF; 
            border: none;
        """)
        self.__initWidget()
    
    def __initWidget(self):
        lineEdit = LineEdit(self)
        lineEdit.setText(self.tr(''))
        lineEdit.setClearButtonEnabled(True)
        lineEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.searchButton = PushButton(
            self.tr('Tìm kiếm'), self, FluentIcon.SEARCH)
        
        # Create a horizontal layout
        hBoxLayout = QHBoxLayout()
        hBoxLayout.addWidget(lineEdit)
        hBoxLayout.addWidget(self.searchButton)
        
        # Add the horizontal layout to the vertical layout
        self.vBoxLayout.addLayout(hBoxLayout)
        self.vBoxLayout.addStretch(1)

        self.titleLabel = StrongBodyLabel("Phát sóng trực tiếp", self)
        self.vBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignTop)

        self.gridLayout = QGridLayout()
        self.gridLayout.setSpacing(10)
        
        self.vBoxLayout.addLayout(self.gridLayout)

        self.showMoreButton = PushButton("Hiển thị thêm", self)
        self.showMoreButton.clicked.connect(self.toggleShowMore)
        self.vBoxLayout.addWidget(self.showMoreButton)

        # Set initial state
        self.showStates = {'showMore': False, 'showMore2': False}
        self.numRows = 1  # Initial number of rows to display
        
        self.vBoxLayout.addStretch(7)

        self.resizeEvent = self.onResize

        self.titleLabel2 = StrongBodyLabel("Các video hiện có", self)
        self.vBoxLayout.addWidget(self.titleLabel2, 0, Qt.AlignTop)
        self.vBoxLayout.addStretch(12)

        self.gridLayout2 = QGridLayout()  
        self.vBoxLayout.addLayout(self.gridLayout2)

        self.showMoreButton2 = PushButton("Hiển thị thêm", self)
        self.showMoreButton2.clicked.connect(self.toggleShowMore2)
        self.vBoxLayout.addWidget(self.showMoreButton2)
        self.vBoxLayout.addStretch(1)

        # Update grid layouts initially
        self.updateGridLayouts()

    def toggleShowMore(self):
        self.toggleState('showMore')

    def toggleShowMore2(self):
        self.toggleState('showMore2')

    def toggleState(self, key):
        self.showStates[key] = not self.showStates[key]
        self.updateGridLayouts()

    def updateGridLayouts(self):
        self.updateGridLayout1()
        self.updateGridLayout2()
        self.updateShowMoreButton()

    def updateGridLayout1(self):
        video_cards_data = [
            ("", "Video Title 1", "2000", "12:00"),
            ("", "Video Title 1", "2000", "12:00"),
            ("", "Video Title 1", "2000", "12:00"),
            ("", "Video Title 1", "2000", "12:00"),
            ("", "Video Title 1", "2000", "12:00"),
            ("", "Video Title 1", "2000", "12:00"),
            ("", "Video Title 1", "2000", "12:00"),
            ("", "Video Title 1", "2000", "12:00"),
             ("", "Video Title 1", "2000", "12:00"),
            ("", "Video Title 1", "2000", "12:00"),
            ("", "Video Title 1", "2000", "12:00"),
            ("", "Video Title 1", "2000", "12:00"),
            ("", "Video Title 1", "2000", "12:00"),
             ("", "Video Title 1", "2000", "12:00"),
            ("", "Video Title 1", "2000", "12:00"),
            ("", "Video Title 1", "2000", "12:00"),
            ("", "Video Title 1", "2000", "12:00"),
            ("", "Video Title 1", "2000", "12:00"),
        ]
        self.updateGridLayout(self.gridLayout, video_cards_data, 'showMore')

    def updateGridLayout2(self):
        video_cards_data = [
            ("", "Video Title 2", "2000", "12:00"),
            ("", "Video Title 2", "2000", "12:00"),
            ("", "Video Title 2", "2000", "12:00"),
            ("", "Video Title 2", "2000", "12:00"),
            ("", "Video Title 2", "2000", "12:00"),
            ("", "Video Title 2", "2000", "12:00"),
            ("", "Video Title 2", "2000", "12:00"),
            ("", "Video Title 2", "2000", "12:00"),
        ]
        self.updateGridLayout(self.gridLayout2, video_cards_data, 'showMore2')

    def updateGridLayout(self, grid_layout, video_cards_data, show_key):
        self.clearGridLayout(grid_layout)
        # Adjust the number of columns based on the available width
        available_width = self.width() - grid_layout.contentsMargins().left() - grid_layout.contentsMargins().right()
        num_columns = max(1, available_width // 250)  # Minimum width for VideoCard is 250
        row = 0
        col = 0
        num_cards = len(video_cards_data)
        max_rows = self.numRows if not self.showStates[show_key] else (num_cards + num_columns - 1) // num_columns
        for i, data in enumerate(video_cards_data):
            if i >= max_rows * num_columns:
                break
            videoCard = VideoCard(*data)
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
        self.updateGridLayouts()
        return QScrollArea.resizeEvent(self, event)

    def updateShowMoreButton(self):
        self.showMoreButton.setText("Ẩn đi" if self.showStates['showMore'] else "Hiển thị thêm")
        self.showMoreButton2.setText("Ẩn đi" if self.showStates['showMore2'] else "Hiển thị thêm")




class VideoCard(QWidget):
    def __init__(self, video_image, video_title, views, time, parent=None):
        super().__init__(parent)
        self.is_hovered = False  # Biến để theo dõi trạng thái khi di chuột vào
        self.setStyleSheet("VideoCard { background-color: #333; border-radius: 5px; padding: 10px; }")
        self.vBoxLayout = QVBoxLayout(self)

        # Video image
        self.videoImageLabel = QLabel(self)

        # Video title
        self.videoTitleLabel = QLabel(video_title, self)
        self.videoTitleLabel.setStyleSheet("color: white; font-size: 15px;")


        # Views
        self.viewsLabel = QLabel(f"{views} views", self)
        self.viewsLabel.setStyleSheet("color: white; font-size: 12px;")


        # Time
        self.timeLabel = QLabel(time, self)
        self.timeLabel.setStyleSheet("color: white; font-size: 10px;")

        # Add widgets to layout
        self.vBoxLayout.addWidget(self.videoImageLabel)
        self.vBoxLayout.addWidget(self.videoTitleLabel)
        self.vBoxLayout.addWidget(self.viewsLabel)
        self.vBoxLayout.addWidget(self.timeLabel)

        self.vBoxLayout.setContentsMargins(5, 5, 5, 5)

        self.setLayout(self.vBoxLayout)
  
        self.loadImage(video_image)

    def loadImage(self, url):
        nam = QNetworkAccessManager(self)
        nam.finished.connect(self.handleFinished)
        nam.get(QNetworkRequest(QUrl(url)))

    def handleFinished(self, reply):
        er = reply.error()

        if er == QNetworkReply.NoError:
            bytes_string = reply.readAll()
            pixmap = QPixmap()
            pixmap.loadFromData(bytes_string)
            scaled_pixmap = pixmap.scaled(200, 150, Qt.KeepAspectRatio, Qt.FastTransformation)
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
            print("Clicked on VideoCard")