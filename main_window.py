from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from qfluentwidgets import PushButton, TitleLabel, setTheme, Theme

# Tài liệu chapter 2: Cách sài GUI Designer
# Download gui designer: https://build-system.fman.io/qt-designer-download
# Video hướng dẫn: https://youtu.be/Fk1TBoBcrR4?t=2494

# --- NÂNG CAO SỬ DỤNG qfluentwidgets trong GUI DESIGNER ---
# Hướng dẫn link https://qfluentwidgets.com/pages/designer/#promoting-widget

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("designer.ui", self)

        self.count = 0

        # Tìm thằng button có objectName là button1 trong designer.ui
        self.button = self.findChild(PushButton, "button1") # Trong video là pushButton nhưng ở đây là button1
        # Liên kết hàm onClick với sự kiện click của button
        self.button.clicked.connect(self.onClick)

        # Tìm thằng label có objectName là label1 trong designer.ui
        self.label = self.findChild(QLabel, "label1")

    def onClick(self):
        self.count += 1
        self.label.setText(f"Counter: {self.count}")


