
from PyQt5.QtCore import QUrl, QIODevice, Qt, QFile
from PyQt5.QtGui import QResizeEvent, QFont, QColor    
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QWidget,QFrame ,QGraphicsView, QHBoxLayout,QVBoxLayout, QLabel, QPushButton, QLineEdit, QApplication, QSizePolicy
from qfluentwidgets import (LineEdit, SpinBox, DoubleSpinBox, TimeEdit, DateTimeEdit, DateEdit,
                            TextEdit, SearchLineEdit, PasswordLineEdit, StrongBodyLabel)
from app.component.play_bar import PlayBar, FullScreenButton, MyStandardMediaPlayBar

from qfluentwidgets import (ScrollArea, PushButton, ToolButton, FluentIcon)



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
        lineEdit.setText(self.tr('Nhập link video'))
        lineEdit.setClearButtonEnabled(True)
        lineEdit.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Fixed)

        example_card = ExampleCard(
            title=self.tr("Download Video Here !!"),
            widget=lineEdit,
        )
        self.vBoxLayout.addWidget(example_card, 0, Qt.AlignTop)


class ExampleCard(QWidget):
    def __init__(self, title, widget: QWidget, stretch=1, parent=None):
        super().__init__(parent=parent)
        self.widget = widget
        self.stretch = stretch

        self.titleLabel = StrongBodyLabel(title, self)
        self.card = QFrame(self)
        self.sourceWidget = QFrame(self.card)
        self.downloadButton = PushButton(
            self.tr('Tải về ngay'), self, FluentIcon.DOWNLOAD)

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

        self.__initLayout()

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
        self.bottomLayout.addStretch(1)
        self.bottomLayout.addWidget(self.downloadButton, 0, Qt.AlignCenter)
        self.bottomLayout.addStretch(1)
        self.bottomLayout.setAlignment(Qt.AlignCenter)