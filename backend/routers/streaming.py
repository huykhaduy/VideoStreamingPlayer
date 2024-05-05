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
    path = "storage/stream/"
    if not os.path.exists(path):
        os.makedirs(path)

    with open(f"storage/stream/{video_id}.m3u8", "w") as f:
        f.write(m3u8_file.dumps())

    thumbnail_url = uploadSingleFile(thumbnail.file, f"thumbnail/video_{video_id}.{thumbnail.filename.split('.')[-1]}")
    with open(f"storage/stream/{video_id}.m3u8", "rb") as f:
        m3u8_url = uploadSingleFile(f, f"stream/{video_id}/index.m3u8")

    video = Video(id=video_id, title=title, duration=0, url=m3u8_url, thumbnail=thumbnail_url, is_streaming=True)
    Video.insert(video)

    # Broadcast all clients by socket the new video
    return ResponseSuccess(data=video.__dict__())


# Hàm cập nhật video mới
@router.post("/update/{video_id}")
def upload_stream(video_id: str, file: Optional[UploadFile], m3u8_file: UploadFile):
    try:
        if file:
            uploadSingleFile(file.file, f"stream/{video_id}/{file.filename}")
            uploadSingleFile(m3u8_file.file, f"stream/{video_id}/index.m3u8")
        else:
            uploadSingleFile(m3u8_file.file, f"stream/{video_id}/index.m3u8")
            video = Video.get(video_id)
            video.is_hidden = True
            Video.update(video)
        return ResponseSuccess(message="Upload successfully!")
    except Exception as e:
        return ResponseError(message=str(e))


# @router.get("/{video_id}.m3u8")
# def get_m3u8(video_id: str):
#     path = f"storage/stream/{video_id}.m3u8"
#     return FileResponse(path)