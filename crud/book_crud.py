"""
crud/book_crud.py
"""

from database import SessionLocal
from models import Book


def add_book(title, author, isbn, category, total_copies):
    db = SessionLocal()
    try:
        book = Book(
            title=title,
            author=author,
            isbn=isbn,
            category=category,
            total_copies=total_copies,
            available_copies=total_copies,
        )
        db.add(book)
        db.commit()
        db.refresh(book)
        return book
    finally:
        db.close()


def get_all_books():
    db = SessionLocal()
    try:
        return db.query(Book).all()
    finally:
        db.close()


def search_books(keyword):
    db = SessionLocal()
    try:
        like = f"%{keyword}%"
        return db.query(Book).filter(
            (Book.title.like(like)) |
            (Book.author.like(like)) |
            (Book.category.like(like))
        ).all()
    finally:
        db.close()


def get_book_by_id(book_id):
    db = SessionLocal()
    try:
        return db.query(Book).filter(Book.id == book_id).first()
    finally:
        db.close()


def update_book(book_id, title, author, isbn, category, total_copies):
    db = SessionLocal()
    try:
        book = db.query(Book).filter(Book.id == book_id).first()
        if not book:
            return None

        borrowed_count = book.total_copies - book.available_copies
        book.title = title
        book.author = author
        book.isbn = isbn
        book.category = category
        book.total_copies = total_copies
        book.available_copies = max(total_copies - borrowed_count, 0)

        db.commit()
        db.refresh(book)
        return book
    finally:
        db.close()


def delete_book(book_id):
    db = SessionLocal()
    try:
        book = db.query(Book).filter(Book.id == book_id).first()
        if book:
            db.delete(book)
            db.commit()
            return True
        return False
    finally:
        db.close()