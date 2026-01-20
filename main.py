# from typing import Union

from fastapi import FastAPI
from models import Base, engine

app = FastAPI()

# create tables on startup


@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"Duka FastAPI": "1.0"}

# uvicorn main:app --reload
# http://127.0.0.1:8000/docs
    
