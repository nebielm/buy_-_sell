from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.schemas import pictures as s_picture
from app.crud import pictures as c_picture
from app.crud import post as c_post
from app.models import user as m_user
from app.database import get_db

router = APIRouter()


@router.post("/users/{user_id}/post/{post_id}/picture/", response_model=s_picture.Picture)
def create_picture(user_id: int, post_id: int, picture: s_picture.PictureCreate, db: Session = Depends(get_db),
                   current_user: m_user.User = Depends(get_current_user)):
    db_post = c_post.get_post_by_id(db=db, post_id=post_id)
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Post in URL path does not exist in DB")
    if user_id != current_user.id or user_id != db_post.user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Authentication failed or User ID in URL Path does not belong to Post")
    return c_picture.create_picture(db=db, picture=picture)


@router.get("/post/{post_id}/picture/", response_model=list[s_picture.Picture])
def get_pictures_by_post(post_id: int, db: Session = Depends(get_db)):
    db_post = c_post.get_post_by_id(db=db, post_id=post_id)
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Post in URL path does not exist in DB")
    return c_picture.get_picture_by_post_id(db=db, post_id=post_id)


@router.get("/picture/{picture_id}/", response_model=s_picture.Picture)
def get_picture_by_id(picture_id: int, db: Session = Depends(get_db)):
    db_picture = c_picture.get_picture_by_id(db=db, picture_id=picture_id)
    if not db_picture:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Picture does not exist in DB")
    return db_picture


@router.put("/users/{user_id}/picture/{picture_id}/", response_model=s_picture.Picture)
def update_picture(user_id: int, picture_id: int, new_picture: s_picture.PictureUpdate,
                   db: Session = Depends(get_db), current_user: m_user.User = Depends(get_current_user)):
    if user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Authentication failed")
    db_picture = c_picture.get_picture_by_id(db=db, picture_id=picture_id)
    if not db_picture:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Picture does not exist in DB")
    db_post = c_post.get_post_by_id(db=db, post_id=db_picture.post_id)
    if db_post.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="User ID in URL does not belong to Picture")
    if db_picture.image_path == "laptop-4948838_1280.jpg":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Default Picture can't be updated")
    return c_picture.update_picture(db=db, picture_id=picture_id, new_picture=new_picture)


@router.delete("/users/{user_id}/picture/{picture_id}/")
def delete_picture(user_id: int, picture_id: int, db: Session = Depends(get_db),
                   current_user: m_user.User = Depends(get_current_user)):
    if user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Authentication failed")
    db_picture = c_picture.get_picture_by_id(db=db, picture_id=picture_id)
    if not db_picture:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Picture does not exist in DB")
    db_post = c_post.get_post_by_id(db=db, post_id=db_picture.post_id)
    if db_post.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="User ID in URL does not belong to Picture")
    db_post_pictures = c_picture.get_picture_by_post_id(db=db, post_id=db_picture.post_id)
    if db_picture.image_path == "laptop-4948838_1280.jpg" and len(db_post_pictures) == 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Default Picture can't be deleted")
    return c_picture.delete_picture(db=db, picture_id=picture_id)
