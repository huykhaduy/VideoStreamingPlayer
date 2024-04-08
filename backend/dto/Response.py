from pydantic import BaseModel


class ResponseSuccess(BaseModel):
    status: str = 1
    message: str = "Thao tác thành công"
    data: dict = {}


class ResponseError(BaseModel):
    status: str = 0
    message: str = "Thao tác thất bại"
