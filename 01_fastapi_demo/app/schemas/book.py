from pydantic import BaseModel
from datetime import datetime

from app.schemas.author import Author
from app.schemas.category import Category

class BookBase(BaseModel):
    title: str
    description: str
    publish_year: int
    author_id: int
    category_id: int

class BookCreate(BookBase):
    """Schema for create Book"""
    pass 

class BookUpdate(BaseModel):
    """Schema for update Book"""
    title: str | None = None
    description: str | None = None
    publish_year: int | None = None
    author_id: int | None = None
    category_id: int | None = None

class BookInDB(BookBase):
    id: int
    title: str
    description: str
    publish_year: int
    author_id: int
    category_id: int
    cover_image: str | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Schema nested for author and category
class Book(BookInDB):
    author: Author
    category: Category
    
