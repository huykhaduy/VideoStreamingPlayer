from PyQt5.QtCore import QObject, pyqtSignal


# Define signal to communicate between components
class Communication(QObject):
    instance = None
    videoFullScreenToggle = pyqtSignal()