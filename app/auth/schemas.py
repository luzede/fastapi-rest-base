### IMPORTS ###
# External Libraries
from pydantic import BaseModel, ConfigDict
from datetime import datetime

# Internal Libraries


### CODE ###


class Token(BaseModel):
    access_token: str
    token_type: str = "Bearer"


class Payload(BaseModel):
    sub: str
    exp: datetime


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    password_hash: str
    salt: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
