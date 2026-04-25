from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.book import Book
from app.schemas.book import BookCreate, BookUpdate

def get_books(db: Session, page: int = 1, limit: int = 10, filter_status: str = None):
    # базовый запрос: только не удалённые
    query = db.query(Book).filter(Book.is_deleted == False)
    
    if filter_status:
        query = query.filter(Book.status == filter_status)

    total = query.count()
    total_pages = (total + limit - 1) // limit  # округление вверх
    offset = (page - 1) * limit
    books = query.order_by(Book.id).offset(offset).limit(limit).all()

    return books, {"total": total, "page": page, "limit": limit, "total_pages": total_pages}

def get_book_by_id(db: Session, book_id: int):
    book = db.query(Book).filter(Book.id == book_id, Book.is_deleted == False).first()
    return book

def create_book(db: Session, book_data: BookCreate):
    book = Book(**book_data.model_dump())
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

def update_book(db: Session, book_id: int, book_data: BookUpdate):
    book = get_book_by_id(db, book_id)
    if not book:
        return None
    update_dict = book_data.model_dump(exclude_unset=True)  # только переданные поля
    for field, value in update_dict.items():
        setattr(book, field, value)
    db.commit()
    db.refresh(book)
    return book

def soft_delete_book(db: Session, book_id: int):
    book = get_book_by_id(db, book_id)
    if not book:
        return None
    book.is_deleted = True
    db.commit()
    return True