import os
import shutil
from abc import ABC, abstractmethod

import boto3
from fastapi import File


class StorageInterface(ABC):
    @abstractmethod
    def uploadSingleFile(self, f: File, target_path: str) -> str:
        pass

    @abstractmethod
    def uploadFileInFolder(self, upload_folder: str, target_folder: str = "no_name") -> bool:
        pass


class AWSStorage(StorageInterface):
    def __init__(self):
        self.session = self.create_session()

    def uploadFileInFolder(self, upload_folder: str, target_folder: str = "no_name"):
        try:
            s3 = self.session.client('s3')
            for file in os.listdir(upload_folder):
                path = f'{upload_folder}/{file}'
                with open(path, "rb") as f:
                    upload_target = f'{target_folder}/{file}' if target_folder else file
                    s3.upload_fileobj(f, os.getenv("DEFAULT_BUCKET"), upload_target)
            return True
        except Exception as e:
            return False

    def uploadSingleFile(self, f: File, target_path: str):
        s3 = self.session.client('s3')
        s3.upload_fileobj(f, os.getenv("DEFAULT_BUCKET"), target_path)
        return f'{os.getenv("CLOUDFRONT_URL")}/{target_path}'

    def create_session(self):
        return boto3.Session(
            aws_access_key_id=os.getenv("ACCESS_KEY"),
            aws_secret_access_key=os.getenv('SECRET_KEY'),
            region_name=os.getenv('REGION_NAME'),
        )


class LocalStorage(StorageInterface):
    def uploadSingleFile(self, f: File, target_path: str):
        with open(target_path, "wb") as file_object:
            shutil.copyfileobj(f.file, file_object)
        return target_path

    def uploadFileInFolder(self, upload_folder: str, target_folder: str = "no_name"):
        try:
            for file in os.listdir(upload_folder):
                path = f'{upload_folder}/{file}'
                with open(path, "rb") as f:
                    upload_target = f'{target_folder}/{file}' if target_folder else file
                    with open(upload_target, "wb") as file_object:
                        shutil.copyfileobj(f, file_object)
            return True
        except Exception as e:
            return False
