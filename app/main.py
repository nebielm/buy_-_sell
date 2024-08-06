from fastapi import FastAPI
from app.routes import auth, user, post
from app.database import get_db

app = FastAPI()

get_db()

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(post.router)
