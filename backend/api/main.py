from fastapi import FastAPI
from pydantic import BaseModel
from mangum import Mangum
from rag.pipeline import query_plays
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://courtex.vercel.app/"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/query")
def query(request: QueryRequest):
    answer, plays = query_plays(request.question)
    return {"answer": answer, "plays": plays}

handler = Mangum(app)