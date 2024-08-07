from fastapi import FastAPI
from app.routes import auth, user, post
from app.database import init_db
from app.core.settings import OPENAPI_SCHEMA

app = FastAPI(openapi_schema=OPENAPI_SCHEMA)

init_db()

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(post.router)
