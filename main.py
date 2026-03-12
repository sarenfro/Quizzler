import random
from pathlib import Path

import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

XLSX_PATH = Path(__file__).parent / "quiz.xlsx"
STATIC_PATH = Path(__file__).parent / "static"

app = FastAPI(title="Quizzler API", description="Quiz study guide powered by your Excel file")
app.mount("/static", StaticFiles(directory=STATIC_PATH), name="static")


@app.get("/")
def root():
    return FileResponse(STATIC_PATH / "index.html")


def load_questions() -> list[dict]:
    df = pd.read_excel(XLSX_PATH)
    questions = []
    for i, row in df.iterrows():
        questions.append({
            "id": i,
            "question": row["Question"],
            "options": {
                "A": row["Option A"],
                "B": row["Option B"],
                "C": row["Option C"],
                "D": row["Option D"],
            },
            "right_answer": str(row["Right Answer"]).strip().upper(),
        })
    return questions


@app.get("/question/random")
def get_random_question():
    questions = load_questions()
    q = random.choice(questions)
    return {
        "id": q["id"],
        "question": q["question"],
        "options": q["options"],
    }


class AnswerSubmission(BaseModel):
    id: int
    answer: str


@app.post("/answer")
def submit_answer(submission: AnswerSubmission):
    questions = load_questions()
    matches = [q for q in questions if q["id"] == submission.id]
    if not matches:
        raise HTTPException(status_code=404, detail=f"Question with id {submission.id} not found")
    q = matches[0]
    user_answer = submission.answer.strip().upper()
    correct = user_answer == q["right_answer"]
    return {
        "correct": correct,
        "your_answer": user_answer,
        "right_answer": q["right_answer"],
        "right_answer_text": q["options"].get(q["right_answer"]),
    }
 
