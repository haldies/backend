from sqlalchemy.orm import Session
from app.models.models import User, AttendanceRecord

from datetime import datetime

def create_user(db: Session, name: str, email: str, role: str):
    db_user = User(name=name, email=email, role=role, class_id=None)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(User).offset(skip).limit(limit).all()

def update_user(db: Session, user_id: str, name: str, email: str, role: str):
    db_user = db.query(User).filter(User.user_id == user_id).first()
    db_user.name = name
    db_user.email = email
    db_user.role = role
    db.commit()
    db.refresh(db_user)
    return db_user

def create_attendance_record(db: Session, user_id: str, session_id: str, status: str):
    timestamp = datetime.utcnow()
    attendance_record = AttendanceRecord(user_id=user_id, session_id=session_id, status=status, timestamp=timestamp)
    db.add(attendance_record)
    db.commit()
    db.refresh(attendance_record)
    return attendance_record


def get_attendance_records(db: Session, skip: int = 0, limit: int = 10):
    return db.query(AttendanceRecord).offset(skip).limit(limit).all()

def create_face_embedding(db: Session, user_id: str, embeddings: list):
    db_user = db.query(User).filter(User.user_id == user_id).first()
    
    if db_user is None:
        raise ValueError("User not found")
    db_user.embeddings = embeddings
    db.commit()
    db.refresh(db_user)
    return db_user
