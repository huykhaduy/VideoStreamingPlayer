from PyQt5.QtWidgets import QWidget, QVBoxLayout

from app.view.list_video_interface import ListVideoInterface


class HomeInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("homeInterface")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.listVideoInterface = ListVideoInterface()
        self.layout.addWidget(self.listVideoInterface)