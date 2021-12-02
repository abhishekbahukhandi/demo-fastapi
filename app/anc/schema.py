from typing import Optional, Dict
from pydantic import BaseModel
from typing import Optional
from datetime import datetime 
from pydantic import Field
from pydantic.networks import EmailStr

class User(BaseModel):
    email: EmailStr

class UserCreate(User):
    password: str

class UserResponse(User):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class UserLogin(UserCreate):
    pass

class PostBase(BaseModel):
    title: str 
    content: str
    published: bool = True

class PostCreate(PostBase):
    owner_id: Optional[int]

    class Config:
        orm_mode = True

class PostResponse(PostBase):
    id: int
    owner_id: int
    owner: UserResponse

    class Config:
        orm_mode = True

class PostResponse_With_Votes(BaseModel):
    Post: PostResponse
    votes: int
    
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class VoteData(BaseModel):
    post_id: int = (...)
    dir: int = Field(ge=0, le=1)
