from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

# this will create the tables & columns in the database
models.Base.metadata.create_all(bind=engine)

class ChoiceBase(BaseModel):
    choice_text: str
    is_correct: bool

class QuestionBase(BaseModel):
    question_text: str
    choices: List[ChoiceBase]

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency Injection
db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/questions/")
async def create_question(question: QuestionBase, db: db_dependency):
    db_question = models.Questions(question_text=question.question_text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)

    for choice in question.choices:
        db_choice = models.Choices(choice.choice_text, is_correct=choice.is_correct, question_id=db_question.id)
        db.add(db_choice)
    db.commit()

@app.get("/questions/{question_id}")
async def get_question(question_id: int, db: db_dependency):
    return db.query(models.Questions).filter(models.Questions.id == question_id).first()


@app.get("/questions/")
async def get_questions(db: db_dependency):
    return db.query(models.Questions).all()

@app.delete("/questions/{question_id}")
async def delete_question(question_id: int, db: db_dependency):
    db.query(models.Questions).filter(models.Questions.id == question_id).delete()
    db.commit()
    return {"message": "Question deleted successfully"}
