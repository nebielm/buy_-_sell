# import os
# import uuid_utils as uuid
# from datetime import datetime
# import boto3
# from dotenv import load_dotenv
# from io import BytesIO
# from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
# from sqlalchemy.orm import Session
# from typing import Annotated
# from app.core.security import get_current_user
# from app.models import user as m_user
# from app.schemas import user as s_user
# from app.crud import user as c_user
# from app.schemas import pictures as s_picture
# from app.crud import pictures as c_picture
# from app.crud import post as c_post
# from app.database import get_db
#
# router = APIRouter()
#
# load_dotenv()
#
# MEGABYTE = 1024 * 1024
#
#
# def generate_download_link(image_name):
#     return f"https://buysellpostpics.s3.amazonaws.com/{image_name}"
#
#
# def upload_file(local_file: Annotated[UploadFile, File()],
#                 pic_name=None):
#     s3_client = boto3.client(
#         service_name='s3',
#         region_name='eu-north-1',
#         aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
#         aws_secret_access_key=os.getenv("AWS_SECRET_KEY")
#     )
#     now = datetime.now()
#     dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
#     if not pic_name:
#         pic_name = os.path.basename(local_file.filename).replace(" ", "_")
#     image_name = f"{uuid.uuid7()}_{dt_string}_{pic_name}"
#     file_size = local_file.size
#     file_content = local_file.content_type
#     if file_size > MEGABYTE or "image" not in file_content:
#         raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Size to big or file not image.")
#     try:
#         s3_client.upload_fileobj(local_file.file, 'buysellpostpics', image_name)
#         print(f'File {image_name} uploaded successfully.')
#         download_link = generate_download_link(image_name)
#         return download_link
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
#
#
# def delete_image_from_s3(object_name):
#     s3_client = boto3.client(
#         service_name='s3',
#         region_name='eu-north-1',
#         aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
#         aws_secret_access_key=os.getenv("AWS_SECRET_KEY")
#     )
#     try:
#         s3_client.delete_object(Bucket='buysellpostpics', Key=object_name)
#         print(f'File {object_name} deleted successfully.')
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
#
#
# # @router.post("/users/", response_model=s_user.User)
# # def create_user(image: Annotated[UploadFile, File()], db: Session = Depends(get_db),
# #                 user: s_user.UserCreate = Depends(parse_user_create)):
# #     if c_user.get_user_by_email(db=db, user_email=user.email):
# #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Email already registered")
# #     if c_user.get_user_by_username(db=db, username=user.username):
# #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Username already registered")
# #     download_link = upload_file(local_file=image)
# #     user_dict = user.model_dump()
# #     user_dict['profile_picture_path'] = download_link
# #     print(user_dict)
# #     user = s_user.UserCreate(**user_dict)
# #     print(user)
# #     return c_user.create_user(db=db, user=user)
#
#
# # @router.put("/users/{user_id}/", response_model=s_user.User)
# # def update_user(user_id: int, image: Annotated[UploadFile, File()] = None,
# #                 user: s_user.UserUpdateBase = Depends(parse_user_update),
# #                 db: Session = Depends(get_db), current_user: m_user.User = Depends(get_current_user)):
# #     if current_user.id != user_id:
# #         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed")
# #     db_user = c_user.get_user_by_id(db=db, user_id=user_id)
# #     if not db_user:
# #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
# #     if user.email and c_user.get_user_by_email(db=db, user_email=user.email) and user.email != db_user.email:
# #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Email already registered")
# #     elif user.username and c_user.get_user_by_username(db=db, username=user.username) and user.username != db_user.username:
# #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Username already registered")
# #     if image:
# #         image_name = current_user.profile_picture_path.split("/")[-1]
# #         if "default.jpg" not in image_name:
# #             delete_image_from_s3(image_name)
# #         download_link = upload_file(local_file=image)
# #         user_dict = user.model_dump()
# #         user_dict['profile_picture_path'] = download_link
# #         user = s_user.UserUpdate(**user_dict)
# #     return c_user.update_user(db=db, user_id=user_id, user_new=user)
#
#
# # @router.delete("/users/{user_id}/")
# # def delete_user(user_id: int, db: Session = Depends(get_db), current_user: m_user.User = Depends(get_current_user)):
# #     if current_user.id != user_id:
# #         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed")
# #     image_name = current_user.profile_picture_path.split("/")[-1]
# #     if "default.jpg" not in image_name:
# #         delete_image_from_s3(image_name)
# #     message = c_user.delete_user(db=db, user_id=user_id)
# #     if not message:
# #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No user in DB with ID: {user_id}")
# #     return message
#
#
# @router.post("/users/{user_id}/post/{post_id}/picture/", response_model=s_picture.Picture)
# def create_picture(image: Annotated[UploadFile, File()],
#                    user_id: int, post_id: int,
#                    db: Session = Depends(get_db),
#                    current_user: m_user.User = Depends(get_current_user)):
#     db_post = c_post.get_post_by_id(db=db, post_id=post_id)
#     if not db_post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail="Post in URL path does not exist in DB")
#     if user_id != current_user.id or user_id != db_post.user_id:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
#                             detail="Authentication failed or User ID in URL Path does not belong to Post")
#     download_link = upload_file(local_file=image)
#     picture = s_picture.PictureCreate(image_path=download_link, post_id=post_id)
#     return c_picture.create_picture(db=db, picture=picture)
#
#
# @router.put("/users/{user_id}/picture/{picture_id}/", response_model=s_picture.Picture)
# def update_picture(image: Annotated[UploadFile, File()],
#                    user_id: int, picture_id: int,
#                    db: Session = Depends(get_db), current_user: m_user.User = Depends(get_current_user)):
#     if user_id != current_user.id:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
#                             detail="Authentication failed")
#     db_picture = c_picture.get_picture_by_id(db=db, picture_id=picture_id)
#     if not db_picture:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail="Picture does not exist in DB")
#     db_post = c_post.get_post_by_id(db=db, post_id=db_picture.post_id)
#     if db_post.user_id != user_id:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
#                             detail="User ID in URL does not belong to Picture")
#     image_name = db_picture.image_path.split("/")[-1]
#     if "default_post_pic.jpg" not in image_name:
#         delete_image_from_s3(image_name)
#     download_link = upload_file(local_file=image)
#     new_picture = s_picture.PictureUpdate(image_path=download_link)
#     return c_picture.update_picture(db=db, picture_id=picture_id, new_picture=new_picture)
#
#
# @router.delete("/users/{user_id}/picture/{picture_id}/")
# def delete_picture(user_id: int, picture_id: int,
#                    db: Session = Depends(get_db),
#                    current_user: m_user.User = Depends(get_current_user)):
#     if user_id != current_user.id:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
#                             detail="Authentication failed")
#     db_picture = c_picture.get_picture_by_id(db=db, picture_id=picture_id)
#     if not db_picture:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail="Picture does not exist in DB")
#     db_post = c_post.get_post_by_id(db=db, post_id=db_picture.post_id)
#     if db_post.user_id != user_id:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
#                             detail="User ID in URL does not belong to Picture")
#     db_post_pictures = c_picture.get_picture_by_post_id(db=db, post_id=db_picture.post_id)
#     image_name = db_picture.image_path.split("/")[-1]
#     if "default_post_pic.jpg" in image_name and len(db_post_pictures) == 1:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
#                             detail="If last Picture is Default Picture: can't be deleted, try to update.")
#     if "default_post_pic.jpg" in image_name and len(db_post_pictures) > 1:
#         return c_picture.delete_picture(db=db, picture_id=picture_id)
#     if "default_post_pic.jpg" not in image_name and len(db_post_pictures) == 1:
#         default_download_link = ("https://buysellpostpics.s3.amazonaws.com/01919976-385e-7a60-8eeb-7ab00c13e0cf_"
#                                  "28_08_2024_16_49_07_default_post_pic.jpg")
#         default_picture = s_picture.PictureUpdate(image_path=default_download_link)
#         c_picture.update_picture(db=db, picture_id=picture_id, new_picture=default_picture)
#         delete_image_from_s3(image_name)
#         return {"message": "Picture gets updated to default because last picture from Post"}
#     if "default_post_pic.jpg" not in image_name and len(db_post_pictures) > 1:
#         delete_image_from_s3(image_name)
#         return c_picture.delete_picture(db=db, picture_id=picture_id)
