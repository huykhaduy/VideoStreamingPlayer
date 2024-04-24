import uuid
from fastapi import APIRouter, UploadFile, Form

router = APIRouter()

@router.post("/token")
def get_token():
    return {"token": str(uuid.uuid4())}