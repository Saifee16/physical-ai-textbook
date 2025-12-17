import os
import google.generativeai as genai
from fastapi import APIRouter, HTTPException
from app.schemas.chapters import ChapterCreate, ChapterResponse
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# THIS IS THE LINE THAT WAS MISSING
router = APIRouter()

chapters_db = []
chapter_id_counter = 1

def generate_textbook_content(title: str, description: str = None) -> str:
    try:
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"Professional textbook chapter: {title}. Context: {description}. Use Markdown."
        response = model.generate_content(prompt)
        return response.text
    except Exception:
        return f"# {title}\n\nContent about {description}."

@router.get("/health")
def health_check():
    return {"status": "OK"}

@router.get("/", response_model=list[ChapterResponse])
def list_chapters():
    return chapters_db

@router.post("/", response_model=ChapterResponse)
def create_chapter(chapter: ChapterCreate):
    global chapter_id_counter
    content = generate_textbook_content(chapter.title, chapter.description)
    new_data = {"id": chapter_id_counter, "title": chapter.title, "description": chapter.description, "content": content}
    chapters_db.append(new_data)
    chapter_id_counter += 1
    return new_data

@router.get("/{chapter_id}/export")
def export_chapter(chapter_id: int):
    chapter = next((c for c in chapters_db if c["id"] == chapter_id), None)
    if not chapter: raise HTTPException(status_code=404)
    os.makedirs("exports", exist_ok=True)
    path = f"exports/Chapter_{chapter_id}.md"
    with open(path, "w") as f: f.write(chapter["content"])
    return {"message": "Success", "path": path}
