from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFileDialog, QMessageBox
from qfluentwidgets import PushButton, LineEdit, StrongBodyLabel

from app.model.Video import Video


class UploadInterface(QWidget):
    def __init__(self):
        super().__init__()

        self.title_label = StrongBodyLabel('Tải lên video', self)
        self.title_input = LineEdit(self)
        self.description_input = LineEdit(self)

        self.file_input = LineEdit(self)
        self.browse_file_button = PushButton('Chọn video')
        self.browse_file_button.clicked.connect(self.browse_file)

        self.thumbnail_input = LineEdit(self)
        self.browse_thumbnail_button = PushButton('Chọn ảnh bìa')
        self.browse_thumbnail_button.clicked.connect(self.browse_thumbnail)

        self.upload_button = PushButton('Tải lên', self)
        self.upload_button.clicked.connect(self.upload)

        layout = QVBoxLayout(self)
        layout.addWidget(self.title_label)
        layout.addWidget(StrongBodyLabel('Tiêu đề:'))
        layout.addWidget(self.title_input)
        layout.addWidget(StrongBodyLabel('Mô tả:'))
        layout.addWidget(self.description_input)
        layout.addWidget(StrongBodyLabel('Video file'))
        layout.addWidget(self.file_input)
        layout.addWidget(self.browse_file_button)
        layout.addWidget(StrongBodyLabel('Ảnh bìa'))
        layout.addWidget(self.thumbnail_input)
        layout.addWidget(self.browse_thumbnail_button)
        layout.addWidget(self.upload_button)
        self.setObjectName("uploadInterface")

    def browse_file(self):
        file, _ = QFileDialog.getOpenFileName(self, 'Chọn File', "", "Video Files (*.mp4 *.flv *.ts *.3gp *.mov *.avi *.wmv)")
        if file:
            self.file_input.setText(file)

    def browse_thumbnail(self):
        thumbnail, _ = QFileDialog.getOpenFileName(self, 'Chọn Thumbnail', "", "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)")
        if thumbnail:
            self.thumbnail_input.setText(thumbnail)

    def upload(self):
        title = self.title_input.text()
        description = self.description_input.text()
        file = self.file_input.text()
        thumbnail = self.thumbnail_input.text()

        if not title or not description:
            QMessageBox.warning(self, 'Tải lên video', 'Vui lòng nhập tiêu đề và mô tả')
            return

        Video.upload_video(title, description, file, thumbnail)
        QMessageBox.information(self, 'Tải lên video', 'Tải lên video thành công')
        # Here you would add the code to handle the upload
        # For example, you might call a function like this:
        # self.api.upload_video(title, description, file, thumbnail)