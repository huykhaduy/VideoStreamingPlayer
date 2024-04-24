# class SystemAudioRecorder():
#     def __init__(self, filename="system_audio.wav", samplerate=44100, channels=2):
#         self.filename = filename
#         self.samplerate = samplerate
#         self.channels = channels
#         self.is_recording = False

#     def start(self):
#         def callback(indata, frames, time, status):
#             if status:
#                 print(status)
#             self.audio_frames.append(indata.copy())

#         self.audio_frames = []
#         self.is_recording = True
#         duration = 10.5  # seconds
#         myrecording = sd.rec(int(duration * self.samplerate), samplerate=self.samplerate, channels=self.channels)
#         self.audio_frames.append(myrecording)
#         sd.wait()

#     def stop(self):
#         self.is_recording = False