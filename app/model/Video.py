import json

from app.common.api import APIInterceptor


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
        data = json.loads(json_string)
        if isinstance(data, list):
            return [Video(**item) for item in data]
        else:
            return Video(**data)

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
