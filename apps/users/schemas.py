import uuid
from typing import Optional

from db.schema import BaseModel


class UserSchema(BaseModel):
    id: uuid.UUID
    email: str
    first_name: str
    last_name: str
    mobile: str


class UserCreate(BaseModel):
    email: str
    first_name: str
    last_name: str
    mobile: str
    password: str


class UserUpdate(BaseModel):
    email: str
    first_name: str
    last_name: str
    mobile: str


class AccessTokenSchema(BaseModel):
    access: str


class RefreshTokenSchema(BaseModel):
    refresh: str


class GetAuthSchema(BaseModel):
    access: str
    refresh: str
    user: UserSchema


class LoginSchema(BaseModel):
    email: str
    password: str

