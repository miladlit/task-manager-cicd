
from fastapi import FastAPI

app = FastAPI(title="Task Manager API")


@app.get("/")
def home():
    return {"message": "Welcome to Task Manager API"}


@app.get("/health")
def health():
    return {"status": "ok"}
