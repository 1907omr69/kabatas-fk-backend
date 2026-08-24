from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    username: str

    class Config:
        from_attributes = True

class PlayerResponse(BaseModel):
    id: int
    team: str
    no: Optional[str]
    name: str
    username: Optional[str]
    goals: int
    assists: int
    matches: int
    photo_path: Optional[str]

    class Config:
        from_attributes = True
