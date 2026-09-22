"""
models.py
"""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from database import Base


class RoleEnum(enum.Enum):
    admin = "admin"
    member = "member"


class StatusEnum(enum.Enum):
    borrowed = "borrowed"
    returned = "returned"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.member, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    borrow_records = relationship("BorrowRecord", back_populates="member")


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    author = Column(String(150), nullable=False)
    isbn = Column(String(20), unique=True, nullable=False)
    category = Column(String(100))
    total_copies = Column(Integer, default=1, nullable=False)
    available_copies = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    borrow_records = relationship("BorrowRecord", back_populates="book")


class BorrowRecord(Base):
    __tablename__ = "borrow_records"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    member_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    issue_date = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime, nullable=False)
    return_date = Column(DateTime, nullable=True)
    status = Column(Enum(StatusEnum), default=StatusEnum.borrowed, nullable=False)

    book = relationship("Book", back_populates="borrow_records")
    member = relationship("User", back_populates="borrow_records")