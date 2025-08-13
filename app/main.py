from fastapi import FastAPI, Response, Body, status, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

from random import randrange

import time
from . import model, schema, database, utils
from .schema import PostBase, CreatePost, UpdatePost
from .model import PostModel
from .database import engine, get_db
from sqlalchemy.orm import Session
from .routers import post, user, vote, auth
from .config import settings


# model.Base.metadata.create_all(bind=engine)

app = FastAPI()
origins = ["https://www.google.com", "https://www.facebook.com"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

myposts = [
    {
        "title": "My first post",
        "content": "Content of my first post",
        "published": True,
        "rating": 5,
        "id": 1,
        "author": "Tomisin Adeniyi",
    },
    {
        "title": "My second post",
        "content": "Content of my second post",
        "published": True,
        "rating": 4,
        "id": 2,
        "author": "Tomisin Adeniyi",
    },
]


def find_post(id: int):
    for post in myposts:
        if post["id"] == id:
            return post


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def get_user():
    return {"message": "Welcome to the FastAPI application!"}
