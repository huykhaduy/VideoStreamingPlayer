import json

from app.common.api import APIInterceptor
from PyQt5.QtCore import QFile
import base64

class Video:
    def __init__(self, id, title="", url="", thumbnail="", view=0, duration=0, description="", is_streaming=False, created_at=0):
        self.id = id
        self.title = title
        self.thumbnail = thumbnail
        self.url = url
        self.views = view
        self.duration = duration
        self.is_streaming = is_streaming
        self.created_at = created_at
        self.description = description

    @staticmethod
    def from_json(json_string):
        try:
            if isinstance(json_string, str):
                data = json.loads(json_string)
            else:
                data = json_string
            if isinstance(data, list):
                return [Video(**item) for item in data]
            else:
                return Video(**data)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None

    @staticmethod
    def getListVideo(search=""):
        api = APIInterceptor()
        params = {"search": search} if search else {}
        res = api.get("video/list", params=params)
        return Video.from_json(res.text)


    @staticmethod
    def getVideoDetail(video_id):
        api = APIInterceptor()
        res = api.get(f"video/detail/{video_id}")
        return Video.from_json(res.text)
    
    @staticmethod
    def init_stream_video(title, max_duration, thumbnail_path):
        # Ensure thumbnail_path is a valid path
        if thumbnail_path and QFile.exists(thumbnail_path):
            
            data = {'title': title, 'max_duration': max_duration}
            #---------------C1---------------
            # api = APIInterceptor()
            # f = open(thumbnail_path, 'rb')
            # files = {"file": (f.name, f, "multipart/form-data")}
            #---------------C1---------------

            #---------------C2---------------
            # api = APIInterceptor()
            # files = {'thumbnail': open(thumbnail_path, 'rb')}
            #---------------C2---------------

            #---------------C3---------------  
            api = APIInterceptor()
            files = {'thumbnail': open(thumbnail_path, 'rb')}
            #---------------C3---------------

            res = api.post("stream/init",  data=data, files=files)
            
            if res.status_code == 200:
                # print(str(res.json()["data"]))
                return Video.from_json(res.json()["data"])
            else:
                print(f"API returned status code {res.status_code}. Error message: {res.text}")
                return None
        else:
            print("Invalid thumbnail path or file does not exist")
            return None


    @staticmethod
    def upload_stream(video_id, file, duration):
        data = {'duration': duration}
        files = {'file': file}
        api = APIInterceptor()
        res = api.post(f"stream/update/{video_id}", data=data, files=files)
        return Video.from_json(res.text)

