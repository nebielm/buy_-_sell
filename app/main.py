from fastapi import FastAPI
from app.database import get_db
from app.routes import auth
from app.routes import user

app = FastAPI()

app.include_router(auth.router)
app.include_router(user.router)
