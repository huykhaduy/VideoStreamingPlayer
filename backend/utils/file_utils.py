import os
import shutil

from fastapi import UploadFile


def allowed_file(file_path: str, allowed_extensions: list):
    return '.' in file_path and file_path.rsplit('.', 1)[1].lower() in allowed_extensions


def create_folder_if_not_exists(folder_path: str):
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)


def save_file(file: UploadFile, file_path: str):
    with open(f"{file_path}", "wb") as f:
        shutil.copyfileobj(file.file, f)