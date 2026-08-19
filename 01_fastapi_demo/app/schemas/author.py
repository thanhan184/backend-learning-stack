from pydantic import BaseModel, ConfigDict

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

    model_config = ConfigDict(from_attributes=True)

class Author(AuthorInDB):
    """Schema return for clients"""
    pass 

