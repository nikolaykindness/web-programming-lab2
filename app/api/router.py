from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.book import BookCreate, BookUpdate, BookOut, PaginatedBooks
from app.services import book as book_service

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/books", response_model=PaginatedBooks)
def list_books(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    status: str = Query(None, description="Фильтр по статусу (draft/published)"),
    db: Session = Depends(get_db)
):
    books, meta = book_service.get_books(db, page=page, limit=limit, filter_status=status)
    return {"data": books, "meta": meta}

@router.get("/books/{book_id}", response_model=BookOut)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = book_service.get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.post("/books", response_model=BookOut, status_code=201)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    return book_service.create_book(db, book)

@router.put("/books/{book_id}", response_model=BookOut)
def full_update(book_id: int, book: BookCreate, db: Session = Depends(get_db)):
    updated = book_service.update_book(db, book_id, BookUpdate(**book.model_dump()))
    if not updated:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated

@router.patch("/books/{book_id}", response_model=BookOut)
def partial_update(book_id: int, book: BookUpdate, db: Session = Depends(get_db)):
    updated = book_service.update_book(db, book_id, book)
    if not updated:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated

@router.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    success = book_service.soft_delete_book(db, book_id)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")
    return None