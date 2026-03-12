import random
from pathlib import Path

import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

XLSX_PATH = Path(__file__).parent / "quiz.xlsx"

app = FastAPI(title="Quizzler API", description="Quiz study guide powered by your Excel file")


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
    """Return a random question without revealing the answer."""
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
    """Submit an answer for a question and find out if it's correct."""
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
