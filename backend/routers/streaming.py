import os
import shutil
from datetime import datetime

import m3u8
import shortuuid
from fastapi import APIRouter, UploadFile
from starlette.responses import FileResponse

from model.Video import Video
from utils.aws_utils import uploadSingleFile

router = APIRouter()


@router.post("/init")
# def init_stream(title: Annotated[str, Form()], description: Annotated[str, Form()], thumbnail: UploadFile, init_file: UploadFile):
def init_stream(init_file: UploadFile):
    # with open(f"storage/upload/{init_file.filename}", "wb") as f:
    #     shutil.copyfileobj(init_file.file, f)
    # if not os.path.exists(STREAM_FOLDER):
    #     os.mkdir(STREAM_FOLDER)
    # ffmpeg_command = [
    #     'ffmpeg',
    #     '-i', f'concat:{UPLOAD_FOLDER}/{init_file.filename}',
    #     '-c', 'copy',
    #     '-f', 'hls',
    #     '-hls_time', '20',
    #     '-start_number', '0',
    #     f'{STREAM_FOLDER}/{init_file.filename.split(".")[0]}.m3u8'
    # ]
    # subprocess.run(ffmpeg_command)
    # uploadFileInFolder(STREAM_FOLDER, STREAM_FOLDER)
    #
    # shutil.rmtree(STREAM_FOLDER)
    # return {"message": init_file.filename}
    #
    # video_id = shortuuid.uuid()
    # video = Video(video_id=video_id, url="", thumbnail="", duration=0, view=0, description="")
    # Video.insert(video)
    #

    init_url = uploadSingleFile(init_file.file, f"stream/{init_file.filename}")

    playlist = m3u8.M3U8()
    playlist.version = 3
    playlist.media_sequence = 1
    playlist.target_duration = 20


    segment = m3u8.Segment(uri=init_url, duration=20.033333)
    playlist.segments.append(segment)
    with open(f"storage/stream/test2.m3u8", "w") as f:
        f.write(playlist.dumps())

    # with open(f"storage/stream/test2.m3u8", "rb") as f:
    #     url = uploadSingleFile(f, f"stream/test2.m3u8")
    return "OK"


@router.post("/upload")
def upload_stream(file: UploadFile):
    path = "storage/stream/test2.m3u8"
    playlist = m3u8.load(path)
    playlist.media_sequence += 1

    upload_url = uploadSingleFile(file.file, f"stream/{file.filename}")
    segment = m3u8.Segment(uri=upload_url, duration=20.033333)
    playlist.segments.append(segment)

    with open(f"storage/stream/test2.m3u8", "w") as f:
        f.write(playlist.dumps())

    return "OK"
    # with open(f"storage/stream/test2.m3u8", "rb") as f:
    #     url = uploadSingleFile(f, f"stream/test2.m3u8")
    # return url


@router.get("/index.m3u8")
def get_m3u8():
    path = "storage/stream/test2.m3u8"

    return FileResponse(path)
