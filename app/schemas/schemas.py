from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import List
from fastapi import UploadFile, File
import pickle

class UserBase(BaseModel):
    name: str
    email: str
    role: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    user_id: UUID

    class Config:
        from_attributes = True

class AttendanceRecordBase(BaseModel):
    user_id: UUID
    session_id: UUID
    status: str

class AttendanceRecordCreate(AttendanceRecordBase):
    pass

class AttendanceRecord(AttendanceRecordBase):
    record_id: UUID
    timestamp: datetime

    class Config:
        from_attributes = True
        
        



