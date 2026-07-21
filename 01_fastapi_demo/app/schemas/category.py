from pydantic import BaseModel

class CategoryBase(BaseModel):
    name: str
    description: str | None = None

class CategoryCreate(CategoryBase):
    """Schema for create category"""
    pass 

class CategoryUpdate(BaseModel):
    """Schema for update category"""
    name: str | None = None
    description: str | None = None

class CategoryInDB(CategoryBase):
    id: int

    class Config:
        orm_mode = True

class Category(CategoryInDB):
    """Schema return for clients"""
    pass 

