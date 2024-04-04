from pydantic import BaseModel
from typing import Optional

class Login(BaseModel):
    user: str
    password: str

class id(BaseModel):
    user: str

class Chat(BaseModel):
    message:str

class Translate(BaseModel):
    message: str