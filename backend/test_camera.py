import cv2
import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from mss import mss
from screeninfo import get_monitors


class ScreenWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Get screen size
        monitor = get_monitors()[0]
        self.screen_size = (monitor.width, monitor.height)

        # Define the bounding box of the full screen
        self.bounding_box = {'top': 0, 'left': 0, 'width': self.screen_size[0], 'height': self.screen_size[1]}

        self.sct = mss()

        # Create a QLabel to display the image
        self.label = QLabel(self)
        self.label.setFixedSize(800, 600)  # Set the size of the QLabel to 800x600

        # Create a layout and add the label to it
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)

        # Set the layout of the widget
        self.setLayout(self.layout)

    def update_image(self):
        # Capture screenshot
        sct_img = self.sct.grab(self.bounding_box)

        # Convert the image from BGR to RGB format
        img_rgb = cv2.cvtColor(np.array(sct_img), cv2.COLOR_BGR2RGB)

        # Convert the image to QPixmap format
        qimg = QImage(img_rgb.data, img_rgb.shape[1], img_rgb.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg)

        # Display the image
        self.label.setPixmap(pixmap.scaled(800, 600, Qt.KeepAspectRatio))

if __name__ == "__main__":
    app = QApplication([])

    screen_widget = ScreenWidget()
    screen_widget.show()

    while True:
        screen_widget.update_image()
        app.processEvents()