# backend/main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from . import models, schemas

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/register/")
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(username=user.username, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/login/")
def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user is None or db_user.password != user.password:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"message": "Login successful"}

@app.post("/feedback/")
def give_feedback(feedback: schemas.FeedbackCreate, db: Session = Depends(get_db)):
    db_feedback = models.Feedback(user_id=feedback.user_id, content=feedback.content)
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback
