import os

import boto3
from fastapi import File


def create_session():
    return boto3.Session(
        aws_access_key_id=os.getenv("ACCESS_KEY"),
        aws_secret_access_key=os.getenv('SECRET_KEY'),
        region_name=os.getenv('REGION_NAME'),
    )


def uploadFileInFolder(upload_folder: str, target_folder: str = "no_name"):
    session = create_session()
    s3 = session.client('s3')
    for file in os.listdir(upload_folder):
        path = f'{upload_folder}/{file}'
        with open(path, "rb") as f:
            upload_target = f'{target_folder}/{file}' if target_folder else file
            s3.upload_fileobj(f, os.getenv("DEFAULT_BUCKET"), upload_target)


def uploadSingleFile(f: File, target_path: str):
    session = create_session()
    s3 = session.client('s3')
    s3.upload_fileobj(f, os.getenv("DEFAULT_BUCKET"), target_path)
    return f'{os.getenv("CLOUDFRONT_URL")}/{target_path}'