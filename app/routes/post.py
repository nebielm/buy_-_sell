import os
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.schemas import post as s_post
from app.schemas import pictures as s_pictures
from app.models import user as m_user
from app.crud import post as c_post
from app.crud import user as c_user
from app.crud import pictures as c_pictures
from app.routes.utils import delete_image_from_s3, generate_description
from app.database import get_db

router = APIRouter()

load_dotenv()

BUCKET_NAME = os.getenv("BUCKET_NAME_POST_PIC")


@router.post("/users/{user_id}/posts/", response_model=s_post.Post)
def create_post(user_id: int, post: s_post.PostCreateBase, keywords: str | None = None,
                db: Session = Depends(get_db),
                current_user: m_user.User = Depends(get_current_user)):
    """
    Create a new post for a specific user. Automatically generates a description if not provided.
    """
    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID in the request body does not match the URL path user ID"
        )
    post_data = post.model_dump()
    post_data["user_id"] = user_id
    if not post_data["description"]:
        parameters = ", ".join(f"{key}: {value}" for key, value in post_data.items())
        post_data["description"] = generate_description(keywords=keywords, parameters=parameters)
    db_post = c_post.create_post(db=db, post=s_post.PostCreate(**post_data))
    default_pic_link = ("https://buysellpostpics.s3.amazonaws.com/01919976-385e-7a60-8eeb-"
                        "7ab00c13e0cf_28_08_2024_16_49_07_default_post_pic.jpg")
    default_picture = s_pictures.PictureCreate(image_path=default_pic_link, post_id=db_post.id)
    c_pictures.create_picture(db=db, picture=default_picture)
    return db_post


@router.get("/users/{user_id}/posts/", response_model=list[s_post.Post])
def get_post_by_user(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieve all posts created by a specific user.
    """
    if not c_user.get_user_by_id(db, user_id=user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No user in DB with ID: {user_id}"
        )
    return c_post.get_post_by_user(db=db, user_id=user_id)


@router.get("/posts/sub_cat/{sub_cat}/", response_model=list[s_post.Post])
def get_post_by_sub_cat(sub_cat_id: int, db: Session = Depends(get_db)):
    """
    Retrieve all posts in a specific sub category.
    """
    posts = c_post.get_post_by_sub_cat(db=db, sub_cat_id=sub_cat_id)
    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No posts found for sub-category ID: {sub_cat_id}"
        )
    return posts


@router.get("/posts/{post_id}/", response_model=s_post.Post)
def get_post_by_id(post_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific post by its ID.
    """
    post = c_post.get_post_by_id(db=db, post_id=post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No post in DB with ID: {post_id}"
        )
    return post


@router.get("/posts/", response_model=list[s_post.Post])
def get_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve a list of posts with pagination.
    """
    return c_post.get_posts(db=db, skip=skip, limit=limit)


@router.put("/posts/{post_id}/", response_model=s_post.Post)
def update_post(post_id: int, post: s_post.PostUpdate, db: Session = Depends(get_db),
                current_user: m_user.User = Depends(get_current_user)):
    """
    Update an existing post.
    """
    db_post = c_post.get_post_by_id(db=db, post_id=post_id)
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    if current_user.id != db_post.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Authentication failed"
        )
    return c_post.update_post(db=db, post_id=post_id, post_new=post)


@router.delete("/posts/{post_id}/")
def delete_post(post_id: int, db: Session = Depends(get_db),
                current_user: m_user.User = Depends(get_current_user)):
    """
    Delete a specific post.
    """
    db_post = c_post.get_post_by_id(db=db, post_id=post_id)
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    if current_user.id != db_post.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Authentication failed"
        )
    post_pictures = c_pictures.get_picture_by_post_id(db=db, post_id=post_id)
    if post_pictures:
        for picture in post_pictures:
            image_name = picture.image_path.split("/")[-1]
            if "default_post_pic.jpg" not in image_name:
                delete_image_from_s3(object_name=image_name, bucket_name=BUCKET_NAME)
    return c_post.delete_post(db=db, post_id=post_id)
