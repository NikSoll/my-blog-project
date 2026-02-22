from pydantic import BaseModel, EmailStr
from typing import Optional


class UserRegisterSchema(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class UserResponseSchema(BaseModel):
    id: int
    email: str
    username: str
    role: str


class TokenResponseSchema(BaseModel):
    token: str
    user: UserResponseSchema