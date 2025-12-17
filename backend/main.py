# main.py
from fastapi import FastAPI
from .routes import router  # if you have routes.py with a router

app = FastAPI()

app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI is running!"}
