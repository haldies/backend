from sqlalchemy import Column, String, DateTime, Enum, ForeignKey, Date, Time
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.database.connection import Base
from datetime import datetime



class User(Base):
    __tablename__ = "users"
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, unique=True)
    role = Column(Enum("student", "teacher", name="user_roles"), nullable=False)
    class_id = Column(UUID(as_uuid=True), ForeignKey("classes.class_id"))


class Class(Base):
    __tablename__ = "classes"
    class_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    class_name = Column(String, nullable=False)
    teacher_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"))

class Session(Base):
    __tablename__ = "sessions"
    session_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    class_id = Column(UUID(as_uuid=True), ForeignKey("classes.class_id"))
    date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)

class AttendanceRecord(Base):
    __tablename__ = "attendance_records"
    record_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("sessions.session_id"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"))
    status = Column(Enum("present", "absent", "late", name="attendance_statuses"))
    timestamp = Column(DateTime, nullable=False)

class FaceEmbedding(Base):
    __tablename__ = "face_embeddings"
    embedding_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"))
    embedding = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
