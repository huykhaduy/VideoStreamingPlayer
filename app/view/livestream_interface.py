from PyQt5.QtCore import QUrl, QIODevice, Qt, QFile, QStandardPaths
from PyQt5.QtGui import QResizeEvent, QFont, QColor, QPixmap,QMouseEvent
from PyQt5.QtWidgets import QWidget,QMessageBox, QScrollArea,QFrame ,QFileDialog, QGridLayout,QHBoxLayout,QVBoxLayout, QLabel, QPushButton, QLineEdit, QCheckBox,QApplication, QSizePolicy
from qfluentwidgets import (LineEdit, ExpandLayout,SpinBox, DoubleSpinBox, TimeEdit, DateTimeEdit, DateEdit,PushSettingCard,
                            TextEdit, FolderValidator, PasswordLineEdit, StrongBodyLabel, MessageBoxBase, SubtitleLabel, ConfigItem, qconfig, QConfig)

from qfluentwidgets import (ScrollArea, PushButton, ToolButton, FluentIcon, ImageLabel)
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
import requests
from qfluentwidgets.multimedia import VideoWidget, StandardMediaPlayBar, MediaPlayer, MediaPlayerBase

from PyQt5.QtMultimediaWidgets import QVideoWidget

from app.model.Video import Video
import subprocess
import os
import threading

from app.component.play_bar import PlayBar
from PyQt5.QtCore import QTimer, QTime
import os
import subprocess
from app.common.config import cfg


class LivestreamInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("livestreamInterface")
        self.__initWidget()

        self.timer = QTimer()
        self.timer.timeout.connect(self.capture_screen)

        self.output_folder = "recordings"
        os.makedirs(self.output_folder, exist_ok=True)
        self.output_file = os.path.join(self.output_folder, "recorded_screen%03d.mp4")

        self.ffmpeg_process = None
        self.record_start_time = None
        self.thumbnail_file_path = ""  



    def __initWidget(self):
        self.layout = QVBoxLayout()

        self.videoWidget = QVideoWidget()
        self.mediaPlayer = MediaPlayer(self)
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.playBar = PlayBar()

        self.layout.addWidget(self.videoWidget)
        self.layout.addWidget(self.playBar)

        self.bottomLayout = QHBoxLayout()

        # Phần trái chứa tên tiêu đề và checkbox
        self.leftLayout = QVBoxLayout()

        self.titleLabel = QLabel("Tên tiêu đề:")
        self.titleInput = QLineEdit()
        self.titleInput.setMaximumHeight(30)
        self.titleInput.setFixedWidth(450) 

        self.titleLabel.setStyleSheet("color: white;")

        self.use_webcam_checkbox = QCheckBox("Webcam mở livestream")
        self.use_webcam_checkbox.setStyleSheet("color: white;")

   

        self.titleLabelThumb = SubtitleLabel(self.tr('Chọn file thumbnail'), self)
        self.thumbFileCard = PushSettingCard(
                    self.tr('Choose file'),
                    FluentIcon.UP,
                    self.tr("Choose file"),
                    cfg.get(cfg.downloadFolder),
                    # self.musicInThisPCGroup
                )
        self.thumbFileCard.clicked.connect(self.___onChooseFileCardClicked)

        self.titleInput.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.thumbFileCard.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.thumbFileCard.setMaximumWidth(450)
        self.leftLayout.addWidget(self.titleLabel)
        self.leftLayout.addWidget(self.titleInput)
        self.leftLayout.addWidget(self.use_webcam_checkbox)
        self.leftLayout.addWidget(self.titleLabelThumb)
        self.leftLayout.addWidget(self.thumbFileCard)

        self.leftLayout.setAlignment(Qt.AlignLeft)

        self.bottomLayout.addLayout(self.leftLayout)

        # Phần phải chứa các nút bắt đầu và dừng quay
        self.rightLayout = QVBoxLayout()

        self.startButton = QPushButton("Bắt đầu quay")
        self.startButton.clicked.connect(self.start_recording)
        self.stopButton = QPushButton("Dừng quay")
        self.stopButton.clicked.connect(self.stop_recording)
        self.stopButton.setEnabled(False)
        self.stopButton.setFixedSize(100, 30)
        self.stopButton.setFixedSize(100, 30)


        # Thiết lập kích thước cho nút startButton và stopButton
        self.startButton.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.stopButton.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        self.rightLayout.addWidget(self.startButton)
        self.rightLayout.addWidget(self.stopButton)
        self.rightLayout.setContentsMargins(0, 0, 70, 0) 
        self.bottomLayout.addLayout(self.rightLayout)

        self.bottomLayout.setStretch(0, 1)
        # self.bottomLayout.setStretch(1, 1)

        self.layout.addLayout(self.bottomLayout)

        self.setLayout(self.layout)

    def ___onChooseFileCardClicked(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg)")
        file_dialog.setViewMode(QFileDialog.Detail)
        file_path, _ = file_dialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            self.thumbnail_file_path = file_path 


    def start_recording(self):
        self.startButton.setEnabled(False)
        self.stopButton.setEnabled(True)

        title = self.titleInput.text()
        thumbnail = self.thumbnail_file_path  # Sử dụng đường dẫn của file thumbnail đã lưu
        video = Video.init_stream_video(title, 15, thumbnail)

        print("Video:", video.id)

        if video:

            # Bắt đầu quay video
            self.ffmpeg_command = [
                'ffmpeg', '-y',
                '-video_size', '1920x1080', '-framerate', '30', '-f', 'x11grab', '-i', ':1',
                '-f', 'video4linux2', '-i', '/dev/video0',
                '-f', 'alsa', '-ac', '2', '-i', 'hw:1',
                '-c:v', 'libx264', '-g', '60', '-keyint_min', '2',
                '-f', 'segment', '-segment_time', '2', '-reset_timestamps', '1', self.output_file,
            ]

            if self.use_webcam_checkbox.isChecked():
                self.ffmpeg_command.extend([
                '-filter_complex', '[1:v]scale=320:-1 [webcam]; [0:v][webcam]overlay=W-w-10:H-h-10',
                ])

            self.ffmpeg_process = subprocess.Popen(self.ffmpeg_command)

            upload_thread = UploadThread(video.id, self.output_file)
            upload_thread.start()

            self.record_start_time = QTime.currentTime()

        else:
            # Xử lý trường hợp không nhận được video từ API
            QMessageBox.warning(self, "Error", "Failed to start recording. Please check your internet connection.")

    def stop_recording(self):
        self.timer.stop()
        self.startButton.setEnabled(True)
        self.stopButton.setEnabled(False)

        # Kết thúc quay video
        self.ffmpeg_process.terminate()

        print("Video đã được ghi lại và lưu vào:", self.output_folder)

    def capture_screen(self):
        pass


class UploadThread(threading.Thread):
    def __init__(self, video_id, file_path):
        super().__init__()
        self.video_id = video_id
        self.file_path = file_path

    def run(self):

        duration = self.calculate_duration(self.file_path)
        if duration is not None:
            with open(self.file_path, 'rb') as file:
                Video.upload_stream(self.video_id, file, duration)
        else:
            print(f"Không thể xác định duration cho video {self.file_path}")

    def calculate_duration(self, file_path):
        command = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                   '-of', 'default=noprint_wrappers=1:nokey=1', file_path]
        try:
            output = subprocess.check_output(command, stderr=subprocess.STDOUT)
            duration = float(output)
            return duration
        except subprocess.CalledProcessError as e:
            print(f"Error: {e.output}")
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None
