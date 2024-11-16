from sqlalchemy.orm import Session
from app.models.models import User, AttendanceRecord

from datetime import datetime

def crud_get_attendance_records(db: Session, skip: int = 0, limit: int = 10):
    return db.query(AttendanceRecord).offset(skip).limit(limit).all()

def crud_create_attendance_record(db: Session, user_id: str, session_id: str, status: str):
    timestamp = datetime.utcnow()
    attendance_record = AttendanceRecord(user_id=user_id, session_id=session_id, status=status, timestamp=timestamp)
    db.add(attendance_record)
    db.commit()
    db.refresh(attendance_record)
    return attendance_record


