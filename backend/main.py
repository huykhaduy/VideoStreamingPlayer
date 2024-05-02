import os
from typing import Union, Annotated

import m3u8
from fastapi import FastAPI, UploadFile, File, Form
from dotenv import load_dotenv
import subprocess
import shutil
from routers.video import router as video_router
from routers.streaming import router as streaming_router

from utils.aws_utils import uploadFileInFolder

app = FastAPI()
# Load env
load_dotenv()

# Constant data
UPLOAD_FOLDER = "storage"
STREAM_FOLDER = "stream"

app.include_router(video_router, prefix="/api/video", tags=["videos"])
app.include_router(streaming_router, prefix="/api/stream", tags=["streaming"])

@app.middleware("http")
async def check_token(request, call_next):
    # print(request.url)
    response = await call_next(request)
    return response

# TODO: Implement model to insert database and return media url
# TODO: Lọc loại file cho phép upload
# TODO: Các folder cần phải tạo theo cách random và xóa theo cách random bởi vì nếu upload nhiều file cùng lúc sẽ bị lỗi
# TODO: Nên chỉnh lại định dạng tên cho từng file upload

# TODO: Kiểm tra loại file của streaming
# Không cho phép lấy tên của file mà lấy theo uuid

# TODO: Chưa hoàn thành
@app.post("/upload-stream")
def upload_file_stream(video_id: Annotated[str, Form()], upload_segment: UploadFile):
    # print(video_id)
    m3u8_path = "https://d3l1s92l55csfd.cloudfront.net/stream/music_video0.m3u8"
    video = m3u8.load(m3u8_path)
    segment = m3u8.model.Segment(uri="sss.ts", duration=5.0)
    video.add_segment(segment)
    if (len(video.segments) > 5):
        video.segments.pop(0)
    video.data['media_sequence'] = 1
    print(video.data['media_sequence'])
    with open("test.m3u8", "w") as f:
        f.write(video.dumps())
    return {"video_id": video.dumps()}


# TODO: Chưa hoàn thành
@app.post("/init-stream")
# def init_stream(title: Annotated[str, Form()], description: Annotated[str, Form()], thumbnail: UploadFile, init_file: UploadFile):
def init_stream(init_file: UploadFile):
    with open(f"{UPLOAD_FOLDER}/{init_file.filename}", "wb") as f:
        shutil.copyfileobj(init_file.file, f)
    if not os.path.exists(STREAM_FOLDER):
        os.mkdir(STREAM_FOLDER)
    ffmpeg_command = [
        'ffmpeg',
        '-i', f'concat:{UPLOAD_FOLDER}/{init_file.filename}',
        '-c', 'copy',
        '-f', 'hls',
        '-hls_time', '20',
        '-start_number', '0',
        f'{STREAM_FOLDER}/{init_file.filename.split(".")[0]}.m3u8'
    ]
    subprocess.run(ffmpeg_command)
    uploadFileInFolder(STREAM_FOLDER, STREAM_FOLDER)

    shutil.rmtree(STREAM_FOLDER)
    return {"message": init_file.filename}