from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QVBoxLayout
from qfluentwidgets import FluentWindow, NavigationItemPosition
from app.view.video_interface import VideoInterface

from qfluentwidgets import FluentIcon as FIF

class MainWindow(FluentWindow):
    def __init__(self, communication):
        super().__init__()
        self.communication = communication
        self.__centerWindow()
        self.__setTitlebar()
        self.__initWidget()

    def __initWidget(self):
        self.videoInterface = VideoInterface()
        self.videoInterface.setObjectName("videoInterface")
        self.addSubInterface(self.videoInterface, FIF.VIDEO,"Video Interface")

    def __setTitlebar(self):
        self.setWindowTitle("Your Video Player")
        self.setWindowIcon(QIcon(":/icons/app-icon.png"))

    # Make display window center
    def __centerWindow(self):
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())