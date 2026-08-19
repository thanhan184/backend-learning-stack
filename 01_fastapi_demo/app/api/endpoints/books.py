from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List
from sqlalchemy.orm import Session
from app.api.des import get_db
from app import models
from app.schemas.book import BookCreate, BookUpdate, Book

router = APIRouter()

@router.get("/", response_model=List[Book])
def list_books(
    skip: int = 0,
    limit: int = 100,
    author_id: int  | None = Query(None),
    category_id: int  | None = Query(None),
    year: int | None = Query(None),
    keyword: str | None = Query(None),
    db: Session = Depends(get_db)
):
    """
        Get list books, iclude filter by author_id, category_id, year, keyword
    """
    query = db.query(models.Book)

    if author_id is not None:
        query = query.filter(models.Book.author_id == author_id)
    if category_id is not None:
        query = query.filter(models.Book.category_id == category_id)    
    if year is not None:
        query = query.filter(models.Book.publish_year == year)
    if keyword is not None:
        query = query.filter(models.Book.title.ilike(f"%{keyword}%"))
    
    books = query.offset(skip).limit(limit).all()
    return books

@router.get("/{book_id}", response_model=Book)
def get_book(
        book_id: int,
        db: Session = Depends(get_db)
    ):
    """Get book by id"""
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )
    return book

@router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED)
def create_book(
        book_in: BookCreate,
        db: Session = Depends(get_db)
    ):
    """Create new book, check author_id and category_id exist"""
    existing = db.query(models.Book).filter(models.Book.title == book_in.title).first()

    if existing:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail="Book with this title already exists",
        )
    
    author = db.query(models.Author).filter(models.Author.id == book_in.author_id).first()

    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Author not found",
        )

    category = db.query(models.Category).filter(models.Category.id == book_in.category_id).first()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )

    book = models.Book(
        title = book_in.title,
        description = book_in.description,
        publish_year = book_in.publish_year,
        author_id = book_in.author_id,
        category_id = book_in.category_id
    )

    db.add(book)
    db.commit()
    db.refresh(book)

    return book

@router.put("/{book_id}", response_model=Book)
def update_book(
    book_id: int,
    book_in: BookUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing book"""
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    
    update_data = book_in.model_dump(exclude_unset=True)
    
    if "author_id" in update_data:
        author = (
            db.query(models.Author)
            .filter(models.Author.id == update_data["author_id"])
            .first()
        )

        if not author:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Author not found"
            )

    if "category_id" in update_data:
        category = (
            db.query(models.Category)
            .filter(models.Category.id == update_data["category_id"])
            .first()
        )

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )

    for field, value in update_data.items():
        setattr(book, field, value)
        
    db.commit()
    db.refresh(book)
    return book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(
    book_id: int,
    db: Session = Depends(get_db)
):
    """Delete a book by ID"""
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    
    db.delete(book)
    db.commit()
    return None