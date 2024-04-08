import os
from typing import Union

import boto3
from fastapi import FastAPI, UploadFile, File
from dotenv import load_dotenv
import subprocess
import shutil
from dto.Response import ResponseSuccess

app = FastAPI()
# Load env
load_dotenv()

# Constant data
DEFAULT_BUCKET = os.getenv("DEFAULT_BUCKET")
CLOUDFRONT_URL = os.getenv("CLOUDFRONT_URL")
UPLOAD_FOLDER = "upload_dir"
TEMP_FOLDER = "temp2"


def create_session():
    session = boto3.Session(
        aws_access_key_id=os.getenv("ACCESS_KEY"),
        aws_secret_access_key=os.getenv('SECRET_KEY'),
        region_name=os.getenv('REGION_NAME'),
    )
    return session


# TODO: Implement model to insert database and return media url
@app.post("/upload-file")
def upload_file(file: UploadFile):
    try:
        output_name = file.filename.split(".")[0]
        with open(f"{UPLOAD_FOLDER}/{file.filename}", "wb") as f:
            shutil.copyfileobj(file.file, f)
        # Tạo temp folder nếu chưa tồn tại
        if not os.path.exists(TEMP_FOLDER):
            os.mkdir(TEMP_FOLDER)
        # Convert file mp4 to hls
        convertMP4ToHLS(file.filename, output_name)

        # Upload file to AWS
        target_folder = TEMP_FOLDER
        uploadAllFilesInFolderToAWS(TEMP_FOLDER, TEMP_FOLDER)

        # # Xóa file và folder temp
        os.remove(f"{UPLOAD_FOLDER}/{file.filename}")
        shutil.rmtree(f"{TEMP_FOLDER}")
        return ResponseSuccess(data={"url": f"{CLOUDFRONT_URL}/{target_folder}/{output_name}.m3u8"})
    except Exception as e:
        return ResponseSuccess(message=str(e))


def convertMP4ToHLS(input_name: str, output_name: str, hls_time: int = 5):
    # Define the ffmpeg command
    ffmpeg_command = [
        'ffmpeg',  # Command
        '-i', f'{UPLOAD_FOLDER}/{input_name}',  # Input file
        '-codec:', 'copy',  # Copy the codec
        '-start_number', '0',  # Start number
        '-hls_time', f'{hls_time}',  # HLS time
        '-hls_list_size', '0',  # HLS list size
        '-f', 'hls',  # Output format
        f'{TEMP_FOLDER}/{output_name}.m3u8'  # Output file name
    ]
    # Execute the ffmpeg command
    subprocess.run(ffmpeg_command)


def uploadAllFilesInFolderToAWS(local_folder: str = TEMP_FOLDER, target_folder: str = "my_video") -> bool:
    session = create_session()
    s3 = session.client('s3')
    for file in os.listdir(local_folder):
        path = f'{local_folder}/{file}'
        with open(path, "rb") as f:
            upload_target = f'{target_folder}/{file}' if target_folder else file
            s3.upload_fileobj(f, DEFAULT_BUCKET, upload_target)
    return True