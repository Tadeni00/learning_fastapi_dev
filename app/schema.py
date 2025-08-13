from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import List, Optional

# from app.model import PostModel


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class CreatePost(PostBase):
    pass


class UpdatePost(PostBase):
    pass


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class Post(PostBase):
    id: int
    title: str
    content: str
    created_at: datetime
    user_id: int
    owner: UserOut

    class Config:
        orm_mode = True


class PostResponse(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True


class CreateUser(BaseModel):
    email: EmailStr
    password: str
    created_at: Optional[datetime] = None
    id: Optional[int] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None
    email: Optional[EmailStr] = None

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if isinstance(v, datetime) else v
        }


class Vote(BaseModel):
    post_id: int
    dir: conint(ge=0, le=1)
