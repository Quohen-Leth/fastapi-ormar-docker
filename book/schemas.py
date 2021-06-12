from typing import Optional

from pydantic import BaseModel

from user.schemas import User


class UploadBook(BaseModel):
    title: str
    author: str
    published: int
    pages: int


class UpdateBook(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    published: Optional[int] = None
    pages: Optional[int] = None


class GetListBook(BaseModel):
    id: int
    title: str
    author: str


class GetBook(GetListBook):
    user: User


class Message(BaseModel):
    message: str
