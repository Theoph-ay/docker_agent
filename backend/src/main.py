import os
from fastapi import FastAPI

app = FastAPI()

MY_PROJECT = os.environ.get("MY_PROJECT") or "This is my project"
API_KEY = os.environ.get("API_KEY")
if not API_KEY:
    raise NotImplementedError("API_KEY is not set")

@app.get("/")
def read_index():
    return {"Hello": "World", "project_name": MY_PROJECT, "API_KEY": API_KEY}