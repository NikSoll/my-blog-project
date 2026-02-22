from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class PostCreateSchema(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    body: str = Field(..., min_length=1)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Мой первый пост",
                "body": "Содержание поста..."
            }
        }


class PostUpdateSchema(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    body: Optional[str] = Field(None, min_length=1)


class PostResponseSchema(BaseModel):
    id: int
    title: str
    body: str
    author_id: int
    author_email: str
    created_at: datetime
    updated_at: Optional[datetime]


class PostListResponseSchema(BaseModel):
    posts: List[PostResponseSchema]
    total: int