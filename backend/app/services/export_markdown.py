from pathlib import Path
from app.data.chapters import chapters

EXPORT_DIR = Path("exports/markdown")


def export_chapters_to_markdown():
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)

    for chapter in chapters:
        filename = EXPORT_DIR / f"chapter_{chapter.id}_{chapter.title.replace(' ', '_')}.md"

        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# Chapter {chapter.id}: {chapter.title}\n\n")
            f.write(f"**{chapter.description}**\n\n")

            for i, section in enumerate(chapter.sections, start=1):
                f.write(f"## {chapter.id}.{i} {section.title}\n\n")
                f.write(section.content + "\n\n")

    return {"status": "success", "exported": len(chapters)}
