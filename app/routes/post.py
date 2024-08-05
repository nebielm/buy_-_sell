from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import post as s_post
from app.crud import post as c_post
from app.crud import user as c_user
from app.database import get_db

router = APIRouter()


@router.post("/users/{user_id}/posts/", response_model=s_post.Post)
def create_post(user_id: int, post: s_post.PostCreate, db: Session = Depends(get_db)):
    if not c_user.get_user_by_id(db, user_id=user_id):
        raise HTTPException(status_code=400, detail=f"No user in DB with ID: {user_id}")
    if post.user_id != user_id:
        raise HTTPException(status_code=400, detail="User ID in the request body does not match the URL path user ID")
    return c_post.create_post(db=db, post=post)


@router.get("/users/{user_id}/posts/", response_model=s_post.Post)
def get_post_by_user(user_id: int, db: Session = Depends(get_db)):
    if not c_user.get_user_by_id(db, user_id=user_id):
        raise HTTPException(status_code=400, detail=f"No user in DB with ID: {user_id}")
    return c_post.get_post_by_user(db=db, user_id=user_id)


@router.get("/posts/{sub_cat}/", response_model=s_post.Post)
def get_post_by_sub_cat(sub_cat_id: int, db: Session = Depends(get_db)):
    return c_post.get_post_by_sub_cat(db=db, sub_cat_id=sub_cat_id)


@router.get("/posts/{post_id}/", response_model=s_post.Post)
def get_post_by_id(post_id: int, db: Session = Depends(get_db)):
    post = c_post.get_post_by_id(db=db, post_id=post_id)
    if not post:
        raise HTTPException(status_code=400, detail=f"No post in DB with ID: {post_id}")
    return post


@router.get("/posts/", response_model=list[s_post.Post])
def get_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return c_post.get_posts(db=db, skip=skip, limit=limit)


@router.put("/posts/{post_id}/update/", response_model=s_post.Post)
def update_post(post_id: int, post: s_post.PostUpdate, db: Session = Depends(get_db)):
    db_post = c_post.update_post(db=db, post_id=post_id, post_new=post)
    if not db_post:
        raise HTTPException(status_code=400, detail="Post ID not in DB")
    return db_post


@router.delete("/posts/{post_id}/delete/")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    message = c_post.delete_post(db=db, post_id=post_id)
    if not message:
        raise HTTPException(status_code=400, detail=f"No post in DB with ID: {post_id}")
    return message
