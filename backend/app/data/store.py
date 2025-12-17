from datetime import datetime
from app.models import Chapter

chapters_db = []
chapter_counter = 1


def create_chapter(title: str, description: str | None):
    global chapter_counter

    chapter = Chapter(
        id=chapter_counter,
        title=title,
        description=description,
        content=None,
        created_at=datetime.utcnow()
    )

    chapters_db.append(chapter)
    chapter_counter += 1
    return chapter


def get_all_chapters():
    return chapters_db
