"""
crud/borrow_crud.py
"""

from datetime import datetime, timedelta
from database import SessionLocal
from models import BorrowRecord, Book, StatusEnum


def borrow_book(member_id, book_id, loan_days=14):
    db = SessionLocal()
    try:
        book = db.query(Book).filter(Book.id == book_id).first()
        if not book:
            return None, "Book not found."
        if book.available_copies <= 0:
            return None, "No copies available."

        record = BorrowRecord(
            book_id=book_id,
            member_id=member_id,
            issue_date=datetime.utcnow(),
            due_date=datetime.utcnow() + timedelta(days=loan_days),
            status=StatusEnum.borrowed,
        )
        book.available_copies -= 1

        db.add(record)
        db.commit()
        db.refresh(record)
        return record, "Book borrowed successfully."
    finally:
        db.close()


def return_book(record_id):
    db = SessionLocal()
    try:
        record = db.query(BorrowRecord).filter(BorrowRecord.id == record_id).first()
        if not record:
            return False, "Borrow record not found."
        if record.status == StatusEnum.returned:
            return False, "Book already returned."

        record.status = StatusEnum.returned
        record.return_date = datetime.utcnow()

        book = db.query(Book).filter(Book.id == record.book_id).first()
        if book:
            book.available_copies += 1

        db.commit()
        return True, "Book returned successfully."
    finally:
        db.close()


def get_active_borrows_for_member(member_id):
    db = SessionLocal()
    try:
        return db.query(BorrowRecord).filter(
            BorrowRecord.member_id == member_id,
            BorrowRecord.status == StatusEnum.borrowed
        ).all()
    finally:
        db.close()


def get_history_for_member(member_id):
    db = SessionLocal()
    try:
        return db.query(BorrowRecord).filter(
            BorrowRecord.member_id == member_id
        ).order_by(BorrowRecord.issue_date.desc()).all()
    finally:
        db.close()


def get_all_active_borrows():
    db = SessionLocal()
    try:
        return db.query(BorrowRecord).filter(
            BorrowRecord.status == StatusEnum.borrowed
        ).all()
    finally:
        db.close()