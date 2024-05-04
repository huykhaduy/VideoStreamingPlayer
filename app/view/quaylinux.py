import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QCheckBox
from PyQt5.QtCore import QTimer, QTime
import subprocess

from app.model.Video import Video



class ScreenRecorder(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Screen Recorder")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.start_button = QPushButton("Start Recording")
        self.start_button.clicked.connect(self.start_recording)
        layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop Recording")
        self.stop_button.clicked.connect(self.stop_recording)
        self.stop_button.setEnabled(False)
        layout.addWidget(self.stop_button)

        self.use_webcam_checkbox = QCheckBox("Use Webcam")
        layout.addWidget(self.use_webcam_checkbox)


        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.capture_screen)

        self.output_folder = "recordings"
        os.makedirs(self.output_folder, exist_ok=True)
        self.output_file = os.path.join(self.output_folder, "recorded_screen%d.mp4")

        self.ffmpeg_process = None
        self.record_start_time = None

    def start_recording(self):
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

        # Bắt đầu quay video
        self.ffmpeg_command = [
            'ffmpeg', '-y',
            '-video_size', '1920x1080', '-framerate', '25', '-f', 'x11grab', '-i', ':1',
            '-f', 'video4linux2', '-i', '/dev/video0',
            '-f', 'alsa', '-ac', '2', '-i', 'hw:1',
            '-f', 'segment', '-segment_time', '5', '-reset_timestamps', '1', self.output_file,
        ]

        if self.use_webcam_checkbox.isChecked():
            self.ffmpeg_command.extend([
            '-filter_complex', '[1:v]scale=320:-1 [webcam]; [0:v][webcam]overlay=W-w-10:H-h-10',
            ])

        self.ffmpeg_process = subprocess.Popen(self.ffmpeg_command)

        self.record_start_time = QTime.currentTime()

    def stop_recording(self):
        self.timer.stop()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

        # Kết thúc quay video
        self.ffmpeg_process.terminate()

        print("Video đã được ghi lại và lưu vào:", self.output_folder)

    def capture_screen(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    recorder = ScreenRecorder()
    recorder.show()
    sys.exit(app.exec_())
