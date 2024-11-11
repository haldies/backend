# app/deepface_utils.py
import cv2
import os
import pickle
import uuid
import numpy as np
from deepface import DeepFace
from app.config import detector_backend, model_name, database_path

def save_face_data(image_path, user_id):
    try:
       
        img = cv2.imread(image_path)

        faces = DeepFace.extract_faces(img_path=image_path, detector_backend=detector_backend, enforce_detection=True)

        if len(faces) == 0:
            return {"error": "No faces detected in the image."}
        
       
        user_folder = os.path.join(database_path, user_id) 
   
        if not os.path.exists(user_folder):
            os.makedirs(user_folder)

        embeddings = []
        for i, face in enumerate(faces):
        
            face_image = face["face"]
            face_image_bgr = (face_image * 255).astype(np.uint8)
            face_cropped_path = os.path.join(user_folder, f"face_{i}.jpg")
            cv2.imwrite(face_cropped_path, face_image_bgr)

           
            embedding = DeepFace.represent(img_path=image_path, model_name=model_name, detector_backend=detector_backend)[0]['embedding']

         
            embedding_path = os.path.join(user_folder, f"embedding_{i}.pkl")
            with open(embedding_path, 'wb') as f:
                pickle.dump(embedding, f)

            embeddings.append(embedding_path)

        return {"user_id": user_id, "embeddings": embeddings}
    
    except Exception as e:
        return {"error": str(e)}
