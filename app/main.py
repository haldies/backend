from fastapi import FastAPI, Depends, UploadFile, File
from sqlalchemy.orm import Session
from app.database.crud import create_user, get_users, update_user, create_attendance_record, get_attendance_records

from app.schemas import schemas
import pickle
from uuid import UUID
from datetime import datetime
from app.utils.deepface_utils import save_face_data
import os


app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/api/face_embedding/")
async def create_face_embedding(
    user_id: UUID,
    image: UploadFile = File(...),  
):
    filename = image.filename
   
    contents = await image.read()
  
    image_path = f"uploaded_{filename}"
    with open(image_path, "wb") as f:
        f.write(contents)

    result = save_face_data(image_path, str(user_id))

   
    os.remove(image_path)

    if "error" in result:
        return {"error": result["error"]}
    
    return {
        "user_id": result["user_id"],
        "embeddings": result["embeddings"],
        "message": "File successfully uploaded and processed"
    }
    
    
@app.post("api/verify_face/")

async def verify_face(user_id: UUID, image: UploadFile = File(...)):
    filename = image.filename
   
    contents = await image.read()
  
    image_path = f"uploaded_{filename}"
    with open(image_path, "wb") as f:
        f.write(contents)

    embeddings = DeepFace.represent(img_path=image_path, model_name=model_name, detector_backend=detector_backend)

    user_folder = os.path.join(database_path, user_id)
    if not os.path.exists(user_folder):
        return {"error": "User not found"}

   

    os.remove(image_path)

    distance = DeepFace.findEuclideanDistance(embeddings, user_embeddings)

    return {
        "user_id": user_id,
        "distance": distance,
        "message": "Face verification successful"
    }

@app.post("api/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, name=user.name, email=user.email, role=user.role)


@app.get("api/users/", response_model=list[schemas.User])
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_users(db=db, skip=skip, limit=limit)


@app.put("api/users/{user_id}", response_model=schemas.User)
def update_user(user_id: str, user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.update_user(db=db, user_id=user_id, name=user.name, email=user.email, role=user.role)



@app.post("api/attendance_records/", response_model=schemas.AttendanceRecord)
def create_attendance_record(record: schemas.AttendanceRecordCreate, db: Session = Depends(get_db)):
    return crud.create_attendance_record(db=db, user_id=record.user_id, session_id=record.session_id, status=record.status)


@app.get("api/attendance_records/", response_model=list[schemas.AttendanceRecord])
def get_attendance_records(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_attendance_records(db=db, skip=skip, limit=limit)


