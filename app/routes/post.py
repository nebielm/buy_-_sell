from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.schemas import post as s_post
from app.schemas import pictures as s_pictures
from app.models import user as m_user
from app.crud import post as c_post
from app.crud import user as c_user
from app.crud import pictures as c_pictures
from app.routes.utils import delete_image_from_s3
from app.database import get_db

router = APIRouter()


@router.post("/users/{user_id}/posts/", response_model=s_post.Post)
def create_post(user_id: int, post: s_post.PostCreate, db: Session = Depends(get_db),
                current_user: m_user.User = Depends(get_current_user)):
    if user_id != current_user.id:
        raise HTTPException(status_code=400, detail="User ID in the request body does not match the URL path user ID")
    post_data = post.model_dump()
    post_data["user_id"] = user_id
    db_post = c_post.create_post(db=db, post=s_post.PostCreate(**post_data))
    default_pic_link = ("https://buysellpostpics.s3.amazonaws.com/01919976-385e-7a60-8eeb-7ab00c13e0cf_"
                        "28_08_2024_16_49_07_default_post_pic.jpg")
    default_picture = s_pictures.PictureCreate(image_path=default_pic_link, post_id=db_post.id)
    c_pictures.create_picture(db=db, picture=default_picture)
    return db_post


@router.get("/users/{user_id}/posts/", response_model=list[s_post.Post])
def get_post_by_user(user_id: int, db: Session = Depends(get_db)):
    if not c_user.get_user_by_id(db, user_id=user_id):
        raise HTTPException(status_code=404, detail=f"No user in DB with ID: {user_id}")
    return c_post.get_post_by_user(db=db, user_id=user_id)


@router.get("/posts/sub_cat/{sub_cat}/", response_model=list[s_post.Post])
def get_post_by_sub_cat(sub_cat_id: int, db: Session = Depends(get_db)):
    posts = c_post.get_post_by_sub_cat(db=db, sub_cat_id=sub_cat_id)
    if not posts:
        raise HTTPException(status_code=404, detail=f"No posts found for sub-category ID: {sub_cat_id}")
    return posts


@router.get("/posts/{post_id}/", response_model=s_post.Post)
def get_post_by_id(post_id: int, db: Session = Depends(get_db)):
    post = c_post.get_post_by_id(db=db, post_id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail=f"No post in DB with ID: {post_id}")
    return post


@router.get("/posts/", response_model=list[s_post.Post])
def get_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return c_post.get_posts(db=db, skip=skip, limit=limit)


@router.put("/posts/{post_id}/", response_model=s_post.Post)
def update_post(post_id: int, post: s_post.PostUpdate, db: Session = Depends(get_db),
                current_user: m_user.User = Depends(get_current_user)):
    db_post = c_post.get_post_by_id(db=db, post_id=post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    if current_user.id != db_post.user_id:
        raise HTTPException(status_code=403, detail="Authentication failed")
    return c_post.update_post(db=db, post_id=post_id, post_new=post)


@router.delete("/posts/{post_id}/")
def delete_post(post_id: int, db: Session = Depends(get_db), current_user: m_user.User = Depends(get_current_user)):
    db_post = c_post.get_post_by_id(db=db, post_id=post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    if current_user.id != db_post.user_id:
        raise HTTPException(status_code=403, detail="Authentication failed")
    post_pictures = c_pictures.get_picture_by_post_id(db=db, post_id=post_id)
    if post_pictures:
        for picture in post_pictures:
            image_name = picture.image_path.split("/")[-1]
            if "default_post_pic.jpg" not in image_name:
                delete_image_from_s3(object_name=picture.image_path, bucket_name='buysellpostpics')
            c_pictures.delete_picture(db=db, picture_id=picture.id)
    return c_post.delete_post(db=db, post_id=post_id)
