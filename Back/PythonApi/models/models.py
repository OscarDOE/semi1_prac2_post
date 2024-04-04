from pydantic import BaseModel
from typing import Optional


class Login(BaseModel):
    user: str
    password: str

class Profile(BaseModel):
    user: str
    name: str
    photo: str

class id(BaseModel):
    user: str

class Createalbum(BaseModel):
    id: int
    album: str

class Editalbum(BaseModel):
    id: int
    id_album: int
    newalbum: str



class Chat(BaseModel):
    message:str