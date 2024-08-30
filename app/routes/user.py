import os
from dotenv import load_dotenv
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.models import user as m_user
from app.schemas import user as s_user
from app.crud import user as c_user
from app.crud import post as c_post
from app.crud import pictures as c_pictures
from app.database import get_db
from app.routes import utils

router = APIRouter()

load_dotenv()

BUCKET_NAME_PROFILE_PIC = os.getenv("BUCKET_NAME_PROFILE_PIC")
BUCKET_NAME_POST_PIC = os.getenv("BUCKET_NAME_POST_PIC")


@router.post("/users/", response_model=s_user.User)
def create_user(image: Annotated[UploadFile, File()] = None, db: Session = Depends(get_db),
                user: s_user.UserCreateBase = Depends(utils.parse_user_create_base)):
    if c_user.get_user_by_email(db=db, user_email=user.email):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Email already registered")
    if c_user.get_user_by_username(db=db, username=user.username):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Username already registered")
    user_dict = user.model_dump()
    if image:
        download_link = utils.upload_file(local_file=image, bucket_name=BUCKET_NAME_PROFILE_PIC)
        user_dict['profile_picture_path'] = download_link
    else:
        default_download_link = ("https://buysellusers.s3.eu-north-1.amazonaws.com/019199fa-8037-7d70-889d-"
                                 "e5738feb4bd7_28_08_2024_19_13_36_default_profile_pic.jpg")
        user_dict['profile_picture_path'] = default_download_link
    print(user_dict['profile_picture_path'])
    user = s_user.UserCreate(**user_dict)
    return c_user.create_user(db=db, user=user)


@router.get("/users/", response_model=list[s_user.User])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return c_user.get_users(db=db, skip=skip, limit=limit)


@router.get("/users/{user_id}/", response_model=s_user.User)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = c_user.get_user_by_id(db=db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"No user in DB with ID: {user_id}")
    return user


# @router.get("/users/username/{username}/", response_model=s_user.User)
def get_user_by_username(username: str, db: Session = Depends(get_db)):
    user = c_user.get_user_by_username(db=db, username=username)
    if not user:
        raise HTTPException(status_code=404, detail=f"No user in DB with username: {username}")
    return user


# @router.get("/users/email/{email}/", response_model=s_user.User)
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    user = c_user.get_user_by_email(db=db, user_email=email)
    if not user:
        raise HTTPException(status_code=404, detail=f"No user in DB with email: {email}")
    return user


@router.put("/users/{user_id}/", response_model=s_user.User)
def update_user(user_id: int, image: Annotated[UploadFile, File()] = None,
                user: s_user.UserUpdateBase = Depends(utils.parse_user_update_base),
                db: Session = Depends(get_db), current_user: m_user.User = Depends(get_current_user)):
    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed")
    db_user = c_user.get_user_by_id(db=db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if user.email and c_user.get_user_by_email(db=db, user_email=user.email) and user.email != db_user.email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Email already registered")
    elif (user.username and c_user.get_user_by_username(db=db, username=user.username)
          and user.username != db_user.username):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Username already registered")
    if image:
        image_name = current_user.profile_picture_path.split("/")[-1]
        if "default_profile_pic.jpg" not in image_name:
            utils.delete_image_from_s3(object_name=image_name, bucket_name=BUCKET_NAME_PROFILE_PIC)
        download_link = utils.upload_file(local_file=image, bucket_name=BUCKET_NAME_PROFILE_PIC)
        user_dict = user.model_dump()
        user_dict['profile_picture_path'] = download_link
        user = s_user.UserUpdate(**user_dict)
    return c_user.update_user(db=db, user_id=user_id, user_new=user)


@router.delete("/users/{user_id}/")
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: m_user.User = Depends(get_current_user)):
    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed")
    image_name = current_user.profile_picture_path.split("/")[-1]
    if "default_profile_pic.jpg" not in image_name:
        utils.delete_image_from_s3(object_name=image_name, bucket_name=BUCKET_NAME_PROFILE_PIC)
    user_posts = c_post.get_post_by_user(db=db, user_id=user_id)
    if user_posts:
        for post in user_posts:
            post_pictures = c_pictures.get_picture_by_post_id(db=db, post_id=post.id)
            if post_pictures:
                for picture in post_pictures:
                    image_name = picture.image_path.split("/")[-1]
                    if "default_post_pic.jpg" not in image_name:
                        utils.delete_image_from_s3(object_name=image_name, bucket_name=BUCKET_NAME_POST_PIC)
    message = c_user.delete_user(db=db, user_id=user_id)
    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No user in DB with ID: {user_id}")
    return message
