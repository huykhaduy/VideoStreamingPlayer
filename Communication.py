from PyQt5.QtCore import QObject, pyqtSignal


class Communication(QObject):
    textChange = pyqtSignal(str)
