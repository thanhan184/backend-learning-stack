from pydantic import BaseModel

class AuthorBase(BaseModel):
    name: str
    bio: str | None = None

class AuthorCreate(AuthorBase):
    """Schema for create Author"""
    pass 

class AuthorUpdate(BaseModel):
    """Schema for update Author"""
    name: str | None = None
    bio: str | None = None

class AuthorInDB(AuthorBase):
    id: int

    class Config:
        orm_mode = True

class Author(AuthorInDB):
    """Schema return for clients"""
    pass 

