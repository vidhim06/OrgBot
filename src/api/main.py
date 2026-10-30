
from fastapi import FastAPI
from pydantic import BaseModel

from src.generation.qa_pipeline import answer_question

app = FastAPI(title="OrgBot API")


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {"message": "Welcome to OrgBot!"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/ask")
def ask_question(request: QuestionRequest):
    return answer_question(request.question)
