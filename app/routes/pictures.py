import os
from typing import Annotated
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.models import user as m_user
from app.schemas import pictures as s_picture
from app.crud import pictures as c_picture
from app.crud import post as c_post
from app.database import get_db
from app.routes import utils

router = APIRouter()

load_dotenv()

BUCKET_NAME = os.getenv("BUCKET_NAME_POST_PIC")


@router.post("/users/{user_id}/post/{post_id}/picture/", response_model=s_picture.Picture)
def create_picture(image: Annotated[UploadFile, File()],
                   user_id: int, post_id: int,
                   db: Session = Depends(get_db),
                   current_user: m_user.User = Depends(get_current_user)):
    db_post = c_post.get_post_by_id(db=db, post_id=post_id)
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post in URL path does not exist in DB"
        )
    if user_id != current_user.id or user_id != db_post.user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Authentication failed or User ID in URL Path does not belong to Post"
        )
    download_link = utils.upload_file(local_file=image, bucket_name=BUCKET_NAME)
    picture = s_picture.PictureCreate(image_path=download_link, post_id=post_id)
    post_pictures = c_picture.get_picture_by_post_id(db=db, post_id=post_id)
    if post_pictures:
        for pic in post_pictures:
            image_name = pic.image_path.split("/")[-1]
            if "default_post_pic.jpg" in image_name:
                c_picture.delete_picture(db=db, picture_id=pic.id)
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
def update_picture(image: Annotated[UploadFile, File()], user_id: int,
                   picture_id: int, db: Session = Depends(get_db),
                   current_user: m_user.User = Depends(get_current_user)):
    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed"
        )
    db_picture = c_picture.get_picture_by_id(db=db, picture_id=picture_id)
    if not db_picture:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Picture does not exist in DB"
        )
    db_post = c_post.get_post_by_id(db=db, post_id=db_picture.post_id)
    if db_post.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User ID in URL does not belong to Picture"
        )
    image_name = db_picture.image_path.split("/")[-1]
    if "default_post_pic.jpg" not in image_name:
        utils.delete_image_from_s3(object_name=image_name, bucket_name=BUCKET_NAME)
    download_link = utils.upload_file(local_file=image, bucket_name=BUCKET_NAME)
    new_picture = s_picture.PictureUpdate(image_path=download_link)
    return c_picture.update_picture(db=db, picture_id=picture_id, new_picture=new_picture)


@router.delete("/users/{user_id}/picture/{picture_id}/")
def delete_picture(user_id: int, picture_id: int,
                   db: Session = Depends(get_db),
                   current_user: m_user.User = Depends(get_current_user)):
    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed"
        )
    db_picture = c_picture.get_picture_by_id(db=db, picture_id=picture_id)
    if not db_picture:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Picture does not exist in DB"
        )
    db_post = c_post.get_post_by_id(db=db, post_id=db_picture.post_id)
    if db_post.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User ID in URL does not belong to Picture"
        )
    db_post_pictures = c_picture.get_picture_by_post_id(db=db, post_id=db_picture.post_id)
    image_name = db_picture.image_path.split("/")[-1]
    if "default_post_pic.jpg" in image_name and len(db_post_pictures) == 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="If last Picture is Default Picture: can't be deleted, try to update."
        )
    if "default_post_pic.jpg" in image_name and len(db_post_pictures) > 1:
        return c_picture.delete_picture(db=db, picture_id=picture_id)
    if "default_post_pic.jpg" not in image_name and len(db_post_pictures) == 1:
        default_download_link = ("https://buysellpostpics.s3.amazonaws.com/01919976-385e-7a60-8eeb"
                                 "-7ab00c13e0cf_28_08_2024_16_49_07_default_post_pic.jpg")
        default_picture = s_picture.PictureUpdate(image_path=default_download_link)
        c_picture.update_picture(db=db, picture_id=picture_id, new_picture=default_picture)
        utils.delete_image_from_s3(object_name=image_name, bucket_name=BUCKET_NAME)
        return {"message": "Picture gets updated to default because last picture from Post"}
    if "default_post_pic.jpg" not in image_name and len(db_post_pictures) > 1:
        utils.delete_image_from_s3(object_name=image_name, bucket_name=BUCKET_NAME)
        return c_picture.delete_picture(db=db, picture_id=picture_id)
