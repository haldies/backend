from sqlalchemy.orm import Session
from app.models.models import User, AttendanceRecord

from datetime import datetime

def crud_create_user(db: Session, name: str, email: str, role: str):
    db_user = User(name=name, email=email, role=role, class_id=None)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def crud_get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(User).offset(skip).limit(limit).all()

def crud_update_user(db: Session, user_id: str, name: str, email: str, role: str):
    db_user = db.query(User).filter(User.user_id == user_id).first()
    db_user.name = name
    db_user.email = email
    db_user.role = role
    db.commit()
    db.refresh(db_user)
    return db_user
