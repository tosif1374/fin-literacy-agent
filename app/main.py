# app/main.py
from fastapi import FastAPI
from pydantic import BaseModel
from app.retriever import retrieve, contains_pii_request
from app.llm import generate_answer
from app.translate import detect_language, to_english, from_english

app = FastAPI(title="Digital Financial Literacy Agent")

class Query(BaseModel):
    question: str

SCAM_SAFETY_MESSAGE = (
    "Never share your OTP, UPI PIN, card number, or Aadhaar number with anyone — "
    "banks and RBI never ask for these over call/SMS/WhatsApp. "
    "If you've been targeted, report it at cybercrime.gov.in or call 1930."
)

@app.post("/ask")
def ask(query: Query):
    lang = detect_language(query.question)

    if contains_pii_request(query.question):
        return {"answer": SCAM_SAFETY_MESSAGE, "sources": [], "language": lang}

    question_en = to_english(query.question, lang)
    results = retrieve(question_en)
    context_chunks = [doc for doc, _ in results]
    sources = [{"source": meta["source"], "url": meta["url"]} for _, meta in results]

    answer_en = generate_answer(question_en, context_chunks)
    answer = from_english(answer_en, lang)

    return {"answer": answer, "sources": sources, "language": lang}