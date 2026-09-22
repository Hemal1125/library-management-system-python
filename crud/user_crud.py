"""
crud/user_crud.py
"""

from database import SessionLocal
from models import User, RoleEnum
from auth import hash_password


def create_user(name, email, password, role=RoleEnum.member):
    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.email == email).first()
        if existing:
            return None, "Email already registered."

        user = User(
            name=name,
            email=email,
            password_hash=hash_password(password),
            role=role,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user, "User created successfully."
    finally:
        db.close()


def get_all_users():
    db = SessionLocal()
    try:
        return db.query(User).all()
    finally:
        db.close()


def get_user_by_id(user_id):
    db = SessionLocal()
    try:
        return db.query(User).filter(User.id == user_id).first()
    finally:
        db.close()


def update_user(user_id, name, email, role):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        user.name = name
        user.email = email
        user.role = role
        db.commit()
        db.refresh(user)
        return user
    finally:
        db.close()


def delete_user(user_id):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            db.delete(user)
            db.commit()
            return True
        return False
    finally:
        db.close()