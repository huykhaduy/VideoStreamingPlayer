import datetime
import os
from decimal import Decimal
import json

import shortuuid
from boto3.dynamodb.conditions import Key, Attr

from utils.aws_utils import create_session


class Video:
    def __init__(self, id="", title="", url="", thumbnail="", duration=0, view=0, description="", is_streaming=False, is_hidden=False, created_at=None):
        self.id = id
        self.title = title
        self.url = url
        self.thumbnail = thumbnail
        self.duration = duration
        self.view = view
        self.description = description
        self.is_streaming = is_streaming
        self.is_hidden = is_hidden
        if created_at is not None:
            self.created_at = created_at
        else:
            self.created_at = int(datetime.datetime.now().timestamp())

    @staticmethod
    def get(video_id: str):
        session = create_session()
        db = session.resource("dynamodb")
        response = db.Table("Video").query(KeyConditionExpression=Key("id").eq(video_id))
        if len(response["Items"]) == 0:
            return None
        return response["Items"][0]

    @staticmethod
    def insert(video):
        session = create_session()
        db = session.resource("dynamodb")
        db.Table("Video").put_item(Item=video.__dict__())

    @staticmethod
    def update(video):
        session = create_session()
        db = session.resource("dynamodb")
        db.Table("Video").update_item(
            Key={
                "id": video.id
            },
            UpdateExpression="SET title = :title, #url = :url, thumbnail = :thumbnail, #dur = :duration, #view = :view, description = :description, is_streaming = :is_streaming, is_hidden = :is_hidden",
            ExpressionAttributeValues={":title": video.title, ":url": video.url, ":thumbnail": video.thumbnail,
                                       ":duration": video.duration, ":view": video.view,
                                       ":description": video.description, ":is_streaming": video.is_streaming, ":is_hidden": video.is_hidden},
            ExpressionAttributeNames={
                "#url": "url",
                "#dur": "duration",
                "#view": "view"
            })

    @staticmethod
    def delete(video_id: str):
        session = create_session()
        db = session.resource("dynamodb")
        db.Table("Video").delete_item(Key={"id": video_id})

    @staticmethod
    def list_all(search: str = ""):
        session = create_session()
        db = session.resource("dynamodb")
        scan_kwargs = {
            'FilterExpression': Attr('title').contains(search) & Attr('is_hidden').eq(False)
        }
        return db.Table("Video").scan(**scan_kwargs)["Items"]

    def __dict__(self):
        return {
            "id": self.id,
            "title": self.title,
            "url":  os.getenv("CLOUDFRONT_URL") + self.url if "http" not in self.url else self.url,
            "thumbnail": os.getenv("CLOUDFRONT_URL") + self.thumbnail if "http" not in self.thumbnail else self.thumbnail,
            "duration": self.duration,
            "view": self.view,
            "created_at": self.created_at,
            "description": self.description,
            "is_streaming": self.is_streaming,
            'is_hidden': self.is_hidden
        }

    @staticmethod
    def create_schema():
        session = create_session()
        db = session.resource("dynamodb")
        table = db.create_table(
            TableName="Video",
            KeySchema=[
                {
                    "AttributeName": "id",
                    "KeyType": "HASH"
                }
            ],
            AttributeDefinitions=[
                {
                    "AttributeName": "id",
                    "AttributeType": "S"
                }
            ],
            ProvisionedThroughput={
                "ReadCapacityUnits": 5,
                "WriteCapacityUnits": 5
            }
        )
        table.wait_until_exists()

    @staticmethod
    def from_json(json_string):
        data = json.loads(json_string)
        if isinstance(data, list):
            return [Video(**item) for item in data]
        else:
            return Video(**data)

    @staticmethod
    def from_dict(data):
        return Video(**data)
