import os
import uuid_utils as uuid
from datetime import datetime, date
import boto3
from pydantic import EmailStr
from dotenv import load_dotenv
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, File, Form, UploadFile
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.models import user as m_user
from app.schemas import user as s_user
from app.crud import user as c_user
from app.database import get_db

router = APIRouter()


load_dotenv()

MEGABYTE = 1024 * 1024


def generate_download_link(image_name):
    return f"https://buysellusers.s3.amazonaws.com/{image_name}"


def upload_file(local_file: Annotated[UploadFile, File()],
                pic_name=None):
    s3_client = boto3.client(
        service_name='s3',
        region_name='eu-north-1',
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_KEY")
    )
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
    if not pic_name:
        pic_name = os.path.basename(local_file.filename).replace(" ", "_")
    image_name = f"{uuid.uuid7()}_{dt_string}_{pic_name}"
    file_size = local_file.size
    file_content = local_file.content_type
    if file_size > MEGABYTE or "image" not in file_content:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Size to big or file not image.")
    try:
        s3_client.upload_fileobj(local_file.file, 'buysellusers', image_name)
        print(f'File {image_name} uploaded successfully.')
        download_link = generate_download_link(image_name)
        return download_link
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


def delete_image_from_s3(object_name):
    s3_client = boto3.client(
        service_name='s3',
        region_name='eu-north-1',
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_KEY")
    )
    try:
        s3_client.delete_object(Bucket='buysellusers', Key=object_name)
        print(f'File {object_name} deleted successfully.')
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


def parse_user_create(
    first_name: str = Form(...),
    last_name: str = Form(...),
    birthday: date = Form(...),
    username: str = Form(...),
    email: EmailStr = Form(...),
    tel_number: str | None = Form(None),
    street: str = Form(...),
    house_number: str = Form(...),
    zip_code: str = Form(...),
    city_town_village: str = Form(...),
    country: str = Form(...),
    commercial_account: bool | None = Form(False),
    notification: bool | None = Form(True),
    account_status: bool | None = Form(True),
    password: str = Form(...)
) -> s_user.UserCreate:
    return s_user.UserCreate(**locals())


def parse_user_update(
    first_name: str | None = Form(None),
    last_name: str | None = Form(None),
    birthday: date | None = Form(None),
    username: str | None = Form(None),
    email: EmailStr | None = Form(None),
    tel_number: str | None = Form(None),
    street: str | None = Form(None),
    house_number: str | None = Form(None),
    zip_code: str | None = Form(None),
    city_town_village: str | None = Form(None),
    country: str | None = Form(None),
    commercial_account: bool | None = Form(None),
    notification: bool | None = Form(None),
    account_status: bool | None = Form(None),
    password: str | None = Form(None)
) -> s_user.UserUpdateBase:
    update_data = {key: value for key, value in locals().items() if value is not None}
    return s_user.UserUpdateBase(**update_data)


@router.post("/users/", response_model=s_user.User)
def create_user(image: Annotated[UploadFile, File()], db: Session = Depends(get_db),
                user: s_user.UserCreate = Depends(parse_user_create)):
    if c_user.get_user_by_email(db=db, user_email=user.email):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Email already registered")
    if c_user.get_user_by_username(db=db, username=user.username):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Username already registered")
    download_link = upload_file(local_file=image)
    user_dict = user.model_dump()
    user_dict['profile_picture_path'] = download_link
    print(user_dict)
    user = s_user.UserCreate(**user_dict)
    print(user)
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
                user: s_user.UserUpdateBase = Depends(parse_user_update),
                db: Session = Depends(get_db), current_user: m_user.User = Depends(get_current_user)):
    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed")
    db_user = c_user.get_user_by_id(db=db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if user.email and c_user.get_user_by_email(db=db, user_email=user.email) and user.email != db_user.email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Email already registered")
    elif user.username and c_user.get_user_by_username(db=db, username=user.username) and user.username != db_user.username:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Username already registered")
    if image:
        image_name = current_user.profile_picture_path.split("/")[-1]
        if "default.jpg" not in image_name:
            delete_image_from_s3(image_name)
        download_link = upload_file(local_file=image)
        user_dict = user.model_dump()
        user_dict['profile_picture_path'] = download_link
        user = s_user.UserUpdate(**user_dict)
    return c_user.update_user(db=db, user_id=user_id, user_new=user)


@router.delete("/users/{user_id}/")
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: m_user.User = Depends(get_current_user)):
    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed")
    image_name = current_user.profile_picture_path.split("/")[-1]
    if "default.jpg" not in image_name:
        delete_image_from_s3(image_name)
    message = c_user.delete_user(db=db, user_id=user_id)
    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No user in DB with ID: {user_id}")
    return message
