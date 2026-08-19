from pydantic import BaseModel, ConfigDict

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

    model_config = ConfigDict(from_attributes=True)

class Category(CategoryInDB):
    """Schema return for clients"""
    pass 

