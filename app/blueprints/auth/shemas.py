from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional


class UserRegisterSchema(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('Пароль должен быть минимум 6 символов')
        if not any(c.isdigit() for c in v):
            raise ValueError('Пароль должен содержать хотя бы одну цифру')
        return v


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class UserResponseSchema(BaseModel):
    id: int
    email: str
    role: str


class TokenResponseSchema(BaseModel):
    token: str
    user: UserResponseSchema