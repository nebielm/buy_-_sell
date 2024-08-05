from sqlalchemy.orm import Session
from app.models import post as m_post
from app.schemas import post as s_post


def get_post_by_id(db: Session, post_id: int):
    return db.query(m_post.Post).filter(m_post.Post.id == post_id).first()


def get_post_by_user(db: Session, user_id: int):
    return db.query(m_post.Post).filter(m_post.Post.user_id == user_id).all()


def get_post_by_sub_cat(db: Session, sub_cat_id: int):
    return db.query(m_post.Post).filter(m_post.Post.sub_category_id == sub_cat_id).all()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(m_post.Post).offset(skip).limit(limit).all()


def create_post(db: Session, post: s_post.PostCreate):
    db_post = m_post.Post(**post.model_dump())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def update_post(db: Session, post_id: int, post_new: s_post.PostUpdate):
    db_post = get_post_by_id(db, post_id)
    if not db_post:
        return None
    for attr, value in post_new.model_dump(exclude_unset=True).items():
        setattr(db_post, attr, value)
    db.commit()
    return db_post


def delete_post(db: Session, post_id: int):
    db_post = get_post_by_id(db, post_id)
    if not db_post:
        return None
    db.delete(db_post)
    db.commit()
