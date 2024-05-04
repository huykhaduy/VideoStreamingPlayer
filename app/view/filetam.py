#File dung de chua nhung code co the su dung lai

import soundcard as sc
import soundfile as sf

OUTPUT_FILE_NAME = "out.wav"    # file name.
SAMPLE_RATE = 48000              # [Hz]. sampling rate.
RECORD_SEC = 5                  # [sec]. duration recording audio.

with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(samplerate=SAMPLE_RATE) as mic:
    # record audio with loopback from default speaker.
    data = mic.record(numframes=SAMPLE_RATE*RECORD_SEC)
    
    # change "data=data[:, 0]" to "data=data", if you would like to write audio as multiple-channels.
    sf.write(file=OUTPUT_FILE_NAME, data=data[:, 0], samplerate=SAMPLE_RATE)

#Code này mục đích lấy âm thanh từ laptop

import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PyQt5.QtCore import QTimer, QTime
import subprocess

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

        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.capture_screen)

        if not os.path.exists('short_video'):
            os.makedirs('short_video')

        self.output_folder = "recordings"
        os.makedirs(self.output_folder, exist_ok=True)
        self.output_file = os.path.join(self.output_folder, "recorded_screen.mp4")

        self.ffmpeg_process = None
        self.record_start_time = None
        self.recorded_duration = 0
        self.short_video_counter = 1

    def start_recording(self):
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

        # Bắt đầu quay video
        self.ffmpeg_process = subprocess.Popen([
            'ffmpeg', '-y',
            '-video_size', '1920x1080', '-framerate', '25', '-f', 'x11grab', '-i', ':1',
            '-f', 'video4linux2', '-i', '/dev/video0',
            '-f', 'alsa', '-ac', '2', '-i', 'hw:1',
            '-filter_complex', '[1:v]scale=320:-1 [webcam]; [0:v][webcam]overlay=W-w-10:H-h-10',
            self.output_file
        ])

        self.record_start_time = QTime.currentTime()
        self.timer.start(1000)  # Lập lịch gọi hàm capture_screen mỗi giây

    def stop_recording(self):
        self.timer.stop()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

        # Kết thúc quay video
        self.ffmpeg_process.terminate()

        print("Video đã được ghi lại và lưu vào:", self.output_file)

    def capture_screen(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    recorder = ScreenRecorder()
    recorder.show()
    sys.exit(app.exec_())

    #Doan code phuc vu cho viec hien thi:
    class AudioSystemRecorder():

    def __init__(self, output_file_name = "temp_system_audio.wav", sample_rate = 48000, record_sec = 5):
        self.output_file_name = output_file_name
        self.sample_rate = sample_rate
        self.record_sec = record_sec

    def record(self):
        with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(samplerate=self.sample_rate) as mic:
            # record audio with loopback from default speaker.
            data = mic.record(numframes=self.sample_rate*self.record_sec)

            # change "data=data[:, 0]" to "data=data", if you would like to write audio as multiple-channels.
            sf.write(file=self.output_file_name, data=data[:, 0], samplerate=self.sample_rate)

    def start(self):
        audio_thread = threading.Thread(target=self.record)
        audio_thread.start()

    def stop(self):
        pass



class AudioRecorder():
    "Audio class based on pyAudio and Wave"
    def __init__(self, filename="temp_audio.wav", rate=44100, fpb=1024, channels=2):
        self.open = True
        self.rate = rate
        self.frames_per_buffer = fpb
        self.channels = channels
        self.format = pyaudio.paInt16
        self.audio_filename = filename
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=self.format,
                                      channels=self.channels,
                                      rate=self.rate,
                                      input=True,
                                      frames_per_buffer=self.frames_per_buffer)
        self.audio_frames = []

    def record(self):
        "Audio starts being recorded"
        self.stream.start_stream()
        while self.open:
            data = self.stream.read(self.frames_per_buffer) 
            self.audio_frames.append(data)
            if not self.open:
                break

    def stop(self):
        "Finishes the audio recording therefore the thread too"
        if self.open:
            self.open = False
            self.stream.stop_stream()
            self.stream.close()
            self.audio.terminate()
            waveFile = wave.open(self.audio_filename, 'wb')
            waveFile.setnchannels(self.channels)
            waveFile.setsampwidth(self.audio.get_sample_size(self.format))
            waveFile.setframerate(self.rate)
            waveFile.writeframes(b''.join(self.audio_frames))
            waveFile.close()

    def start(self):
        "Launches the audio recording function using a thread"
        audio_thread = threading.Thread(target=self.record)
        audio_thread.start()

class ScreenWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Get screen size
        monitor = get_monitors()[0]
        self.screen_size = (monitor.width, monitor.height)

        # Define the bounding box of the full screen
        self.bounding_box = {'top': 0, 'left': 0, 'width': self.screen_size[0], 'height': self.screen_size[1]}

        # Create a QLabel to display the image
        self.label = QLabel(self)
        self.label.setFixedSize(800, 600)  # Set the size of the QLabel to 800x600

        # Create buttons for start and stop recording
        self.start_button = QPushButton("Bắt đầu quay", self)
        self.stop_button = QPushButton("Dừng quay", self)

        # Connect buttons to functions
        self.start_button.clicked.connect(self.start_recording)
        self.stop_button.clicked.connect(self.stop_recording)

        # Create a layout and add the label and buttons to it
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.start_button)
        self.layout.addWidget(self.stop_button)

        # Set the layout of the widget
        self.setLayout(self.layout)

        # Initialize video recording variables
        self.is_recording = False
        self.video_writer = None
        self.audio_recorder = None
        self.audio_sys_recorder = None

        # Initialize mss
        self.sct = mss()

    def start_recording(self):
        # Initialize video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.video_writer = cv2.VideoWriter('recorded_video_temp.mp4', fourcc, 25, (self.screen_size[0], self.screen_size[1]))

        # Initialize audio recording
        self.audio_recorder = AudioRecorder()
        self.audio_sys_recorder = AudioSystemRecorder()


        self.audio_recorder.start()
        self.audio_sys_recorder.start()


        # Start recording
        self.is_recording = True

    def stop_recording(self):
        # Stop recording
        self.is_recording = False

        # Release video writer
        if self.video_writer is not None:
            self.video_writer.release()

        # Stop and save audio recording
        if self.audio_recorder is not None:
            self.audio_recorder.stop()

        # Combine video and audio
        video_clip = VideoFileClip('recorded_video_temp.mp4')
        audio_clip = AudioFileClip('temp_audio.wav')
        final_clip = video_clip.set_audio(audio_clip)
        final_clip.write_videofile('recorded_video.mp4', fps=25)

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

        # If recording, write frame to video
        if self.is_recording:
            if self.video_writer is not None:
                self.video_writer.write(cv2.cvtColor(np.array(sct_img), cv2.COLOR_RGB2BGR))

if __name__ == "__main__":
    app = QApplication([])

    screen_widget = ScreenWidget()
    screen_widget.show()

    timer = QTimer()
    timer.timeout.connect(screen_widget.update_image)
    timer.start(100)  # Update image every 100 milliseconds

    app.exec_()