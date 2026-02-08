from fastapi import FastAPI
# The dot means "the current directory"
from .routes import chat, documents  

app = FastAPI(title="Physical AI Textbook API")

# Ensure 'chat' and 'documents' files exist inside the 'routes' folder
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(documents.router, prefix="/api/documents", tags=["Documents"])

@app.get("/")
async def root():
    return {"message": "Physical AI API is running"}