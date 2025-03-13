# backend/schemas.py
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class FeedbackCreate(BaseModel):
    user_id: int
    content: str
