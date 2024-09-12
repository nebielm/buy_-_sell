from sqlalchemy.orm import Session
from app.crud.post import get_post_by_sub_cat, update_post
from app.models import sub_category as m_sub_cat
from app.schemas import sub_category as s_sub_cat
from app.schemas.post import PostUpdate


def get_sub_cat_by_id(db: Session, sub_cat_id: int):
    """
    Retrieve a sub cat by its ID.
    """
    return db.query(m_sub_cat.SubCat).filter(m_sub_cat.SubCat.id == sub_cat_id).first()


def get_sub_cat_by_title(db: Session, title: str):
    """
    Retrieve a sub cat by its title.
    """
    return db.query(m_sub_cat.SubCat).filter(m_sub_cat.SubCat.title == title).first()


def get_sub_cat_by_parent_id(db: Session, parent_id: int):
    """
    Retrieve sub cats by their parent cat ID.
    """
    return db.query(m_sub_cat.SubCat).filter(m_sub_cat.SubCat.parent_id == parent_id).all()


def get_sub_cats(db: Session, skip: int = 0, limit: int = 100):
    """
    Retrieve sub cats with pagination.
    """
    return db.query(m_sub_cat.SubCat).offset(skip).limit(limit).all()


def create_sub_cat(db: Session, sub_cat: s_sub_cat.SubCatCreate):
    """
    Create and add a new sub cat to the database.
    """
    if get_sub_cat_by_title(db=db, title=sub_cat.title):
        return None
    db_sub_cat = m_sub_cat.SubCat(**sub_cat.model_dump())
    db.add(db_sub_cat)
    db.commit()
    db.refresh(db_sub_cat)
    return db_sub_cat


def update_sub_cat(db: Session, sub_cat_id: int, new_sub_cat: s_sub_cat.SubCatUpdate):
    """
    Update an existing sub cat in the database.
    """
    db_sub_cat = get_sub_cat_by_id(db=db, sub_cat_id=sub_cat_id)
    if not db_sub_cat:
        return None
    existing_cat = get_sub_cat_by_title(db=db, title=new_sub_cat.title)
    if existing_cat and existing_cat.id != sub_cat_id:
        return None
    db_sub_cat.title = new_sub_cat.title
    db.commit()
    db.refresh(db_sub_cat)
    return db_sub_cat


def delete_sub_cat(db: Session, sub_cat_id: int, post_new: PostUpdate):
    """
    Delete a sub cat from the database.
    """
    db_sub_cat = get_sub_cat_by_id(db=db, sub_cat_id=sub_cat_id)
    if not db_sub_cat:
        return None
    db_post = get_post_by_sub_cat(db=db, sub_cat_id=db_sub_cat.id)
    if db_post:
        update_post(db=db, post_id=db_post.id, post_new=post_new)
    db.delete(db_sub_cat)
    db.commit()
    return {"status": "successfully deleted"}
