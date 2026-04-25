from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class BookCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    status: Optional[str] = "draft"  # черновик по умолчанию
    author_name: str = Field(..., min_length=1, max_length=255)

class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    status: Optional[str] = None
    author_name: Optional[str] = Field(None, min_length=1, max_length=255)

class BookOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str
    author_name: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}  # чтобы работало с ORM

class PaginatedBooks(BaseModel):
    data: List[BookOut]
    meta: dict  # total, page, limit, total_pages