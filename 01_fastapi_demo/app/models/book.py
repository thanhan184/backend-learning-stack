from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key = True, index = True)
    title = Column(String(255), nullable=True, index=True)
    description = Column(Text, nullable=True)
    publish_year = Column(Integer, nullable=True)
    cover_image = Column(String(255), nullable=True)    #save path, stactic/covers/abc.jpg
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    author_id = Column(Integer, ForeignKey("authors.id", ondelete="RESTRICT"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="RESTRICT"), nullable=False)
    
    #Quan he n - 1
    books = relationship("Author", back_populates="books")
    books = relationship("Category", back_populates="categories")