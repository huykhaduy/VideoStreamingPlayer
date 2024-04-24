import os
import shutil
from datetime import datetime
from typing import Annotated, Optional

import m3u8
import shortuuid
from fastapi import APIRouter, UploadFile, Form
from starlette.responses import FileResponse

from dto.Response import ResponseSuccess, ResponseError
from model.Video import Video
from utils.aws_utils import uploadSingleFile

router = APIRouter()


@router.post("/init")
def init_stream_video(title: Annotated[str, Form()], max_duration: Annotated[float, Form()], thumbnail: UploadFile):
    m3u8_file = m3u8.M3U8()
    m3u8_file.version = 3
    m3u8_file.target_duration = max_duration
    m3u8_file.media_sequence = 0

    video_id = shortuuid.uuid()
    with open(f"storage/stream/{video_id}.m3u8", "w") as f:
        f.write(m3u8_file.dumps())

    thumbnail_url = uploadSingleFile(thumbnail.file, f"thumbnail/video_{video_id}.{thumbnail.filename.split('.')[-1]}")

    url = f"http://127.0.0.1:8000/stream/{video_id}.m3u8"
    video = Video(id=video_id, title=title, duration=0, url=url, thumbnail=thumbnail_url)
    Video.insert(video)

    # Broadcast all clients by socket the new video
    return ResponseSuccess(data=video.__dict__())


# Hàm cập nhật video mới
@router.post("/update/{video_id}")
def upload_stream(video_id: str, file: Optional[UploadFile], duration: Annotated[float, Form()]):
    try:
        path = f"storage/stream/{video_id}.m3u8"
        playlist = m3u8.load(path)
        if duration >= 0:
            upload_url = ""
            length = len(playlist.segments)
            if length < 4:
                upload_url = uploadSingleFile(file.file, f"stream/{video_id}/{length}.ts")
                if length == 0:
                    playlist.media_sequence = 0
                else:
                    playlist.media_sequence += 1
            elif length >= 4:
                playlist.segments.pop(0)
                playlist.media_sequence += 1
                upload_url = uploadSingleFile(file.file, f"stream/{video_id}/{playlist.media_sequence}.ts")

            segment = m3u8.Segment(uri=upload_url, duration=duration)
            playlist.segments.append(segment)
        else:
            playlist.is_endlist = True
            # Broadcast all clients by socket the video is end

        with open(path, "w") as f:
            f.write(playlist.dumps())
        return ResponseSuccess()
    except Exception as e:
        return ResponseError(message=str(e))


@router.get("/{video_id}.m3u8")
def get_m3u8(video_id: str):
    path = f"storage/stream/{video_id}.m3u8"
    return FileResponse(path)


# @router.get("/list")
# def list_streaming():
#     return Video.list_all()