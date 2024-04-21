# import sys
#
# from PyQt5.QtWidgets import (
#     QApplication, QDialog, QMainWindow, QMessageBox
# )
# from PyQt5.uic import loadUi
#
# from main_window_ui import Ui_Form
#
# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.ui = Ui_Form()
#         self.ui.setupUi(self)
#
# def main():
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec_())
#
# if __name__ == "__main__":
#     main()
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from qfluentwidgets import FluentWindow, setTheme, Theme

from app.common.communication import Communication
from app.view.main_window import MainWindow
from app.view.video_interface import VideoInterface
import resources

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
QApplication.processEvents()

app = QApplication(sys.argv)
app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)
# video = VideoInterface()
# video.show()
Communication.instance = Communication()
MainWindow.instance = MainWindow()
MainWindow.instance.show()
setTheme(Theme.DARK)
app.exec_()
