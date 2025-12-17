from fastapi import FastAPI
from app.routes.chapters import router as chapters_router

app = FastAPI(title="Physical AI Textbook API")

app.include_router(chapters_router, prefix="/chapters", tags=["Chapters"])

@app.get("/")
def root():
    return {"message": "Welcome to Physical AI Textbook!"}
