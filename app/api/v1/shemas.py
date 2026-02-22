from pydantic import BaseModel

class PostCreateSchemas(BaseModel):
    title: str
    body: str