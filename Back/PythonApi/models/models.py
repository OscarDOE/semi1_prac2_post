from pydantic import BaseModel
from typing import Optional

class Login(BaseModel):
    user: str
    password: str

class id(BaseModel):
    user: str

class Chat(BaseModel):
    message:str
    session_id: str

class Translate(BaseModel):
    message: str
