from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated
from app.schemas import user as s_user
from app.crud import user as c_user
from app.database import get_db

router = APIRouter()


@router.post("/users/", response_model=s_user.User)
def create_user(user: s_user.UserCreate, db: Session = Depends(get_db)):
    if c_user.get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    return c_user.create_user(db=db, user=user)


@router.get("/users/", response_model=list[s_user.User])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return c_user.get_users(db=db, skip=skip, limit=limit)


@router.get("/users/{user_id}/", response_model=s_user.User)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = c_user.get_user_by_id(db=db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=400, detail=f"No user in DB with ID: {user_id}")
    return user


@router.get("/users/{username}/", response_model=s_user.User)
def get_user_by_username(username: str, db: Session = Depends(get_db)):
    user = c_user.get_user_by_username(db=db, username=username)
    if not user:
        raise HTTPException(status_code=400, detail=f"No user in DB with username: {username}")
    return user


@router.get("/users/{email}/", response_model=s_user.User)
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    user = c_user.get_user_by_email(db=db, user_email=email)
    if not user:
        raise HTTPException(status_code=400, detail=f"No user in DB with email: {email}")
    return user


@router.put("/users/{user_id}/update/", response_model=s_user.User)
def update_user(user_id: int,  user: s_user.UserUpdate, db: Session = Depends(get_db)):
    db_user = c_user.get_user_by_id(db=db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=400, detail=f"No user in DB with ID: {user_id}")
    if user.email and c_user.get_user_by_email(db=db, user_email=user.email) and user_id != db_user.id:
        raise HTTPException(status_code=400, detail=f"Email already registered")
    elif user.username and get_user_by_username(db=db, username=user.username) and user_id != db_user.id:
        raise HTTPException(status_code=400, detail=f"Username already registered")
    return update_user(db=db, user_id=user_id, user_new=user)


@router.delete("users/{user_id}/delete/")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = c_user.get_user_by_id(db=db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=400, detail=f"No user in DB with ID: {user_id}")
    delete_user(db=db, user_id=user_id)
    return {"status": "successfully deleted"}
