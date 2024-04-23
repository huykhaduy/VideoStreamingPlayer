import os
import shutil
import uuid
from typing import Annotated

import shortuuid
from fastapi import APIRouter, UploadFile, Form

from dto.Response import ResponseError, ResponseSuccess
from model.Video import Video
from utils.file_utils import create_folder_if_not_exists, save_file, allowed_file
from utils.hls_utils import convertMP4ToHLS
from utils.aws_utils import uploadFileInFolder, uploadSingleFile

router = APIRouter()


@router.post("/create")
def create_video(file: UploadFile, thumbnail: UploadFile, title:  Annotated[str, Form()], description:  Annotated[str, Form()]):
    try:
        if not allowed_file(file.filename, ["mp4"]):
            return ResponseError(message="File not allowed")

        if not allowed_file(thumbnail.filename, ["png", "jpg", "jpeg"]):
            return ResponseError(message="Thumbnail not allowed")

        # Save file to upload folder
        video_uuid = str(shortuuid.uuid())
        path = f"storage/upload/{video_uuid}_{file.filename}"
        # Have ../ because current folder is inside router
        save_file(file, path)

        # Create temp folder
        TEMP_FOLDER = f"storage/temp_{video_uuid}"
        create_folder_if_not_exists(TEMP_FOLDER)

        # Convert file mp4 to hls
        output_name = file.filename.split(".")[0]
        convertMP4ToHLS(path, f"{TEMP_FOLDER}/{output_name}.m3u8")

        # Upload file to AWS
        uploadFileInFolder(f"{TEMP_FOLDER}", f"video/{video_uuid}")
        uploadSingleFile(thumbnail.file, f"thumbnail/{video_uuid}.{thumbnail.filename.split('.')[-1]}")

        # Xóa file và folder temp
        os.remove(path)
        shutil.rmtree(TEMP_FOLDER)
        # Save to database
        video = Video(id=video_uuid, title=title, description=description, thumbnail=f"/thumbnail/{video_uuid}", url=f"/video/{video_uuid}/{output_name}.m3u8")
        Video.insert(video)

        return ResponseSuccess(data=video.__dict__())
    except Exception as e:
        return ResponseSuccess(message=str(e))


@router.get("/detail/{video_id}")
def get_video(video_id: str):
    video = Video.get(video_id)
    videoModel = Video.from_dict(video)
    videoModel.view += 1
    Video.update(videoModel)
    return video


@router.post("/delete/{video_id}")
def delete_video(video_id: str):
    try:
        Video.delete(video_id)
        return ResponseSuccess(data="Xóa thành công")
    except Exception as e:
        return ResponseError(message=str(e))

@router.get("/view/{video_id}")
def view_video(video_id: str = ""):
    try:
        video = Video.get(video_id)
        video.view += 1
        Video.update(video)
        return ResponseSuccess(data=video.__dict__())
    except Exception as e:
        return ResponseError(message=str(e))


@router.get("/list")
def list_video(search: str = ""):
    return Video.list_all(search)
