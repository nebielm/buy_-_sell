from sqlalchemy.orm import Session
from app.crud.sub_category import get_sub_cat_by_parent_id, delete_sub_cat
from app.models import parent_category as m_parent_cat
from app.schemas import parent_category as s_parent_cat
from app.schemas.post import PostUpdate


def get_parent_cat_by_id(db: Session, parent_cat_id: int):
    """
    Retrieve a parent cat by its ID.
    """
    return (db.query(m_parent_cat.ParentCat).filter
            (m_parent_cat.ParentCat.id == parent_cat_id).first())


def get_parent_cat_by_title(db: Session, title: str):
    """
    Retrieve a parent cat by its title.
    """
    return db.query(m_parent_cat.ParentCat).filter(m_parent_cat.ParentCat.title == title).first()


def get_parent_cats(db: Session, skip: int = 0, limit: int = 100):
    """
    Retrieve parent cats with pagination.
    """
    return db.query(m_parent_cat.ParentCat).offset(skip).limit(limit).all()


def create_parent_cat(db: Session, parent_cat: s_parent_cat.ParentCatCreate):
    """
    Create and add a new parent cat to the database.
    """
    existing_cat = get_parent_cat_by_title(db=db, title=parent_cat.title)
    if existing_cat:
        return None
    db_parent_cat = m_parent_cat.ParentCat(**parent_cat.model_dump())
    db.add(db_parent_cat)
    db.commit()
    db.refresh(db_parent_cat)
    return db_parent_cat


def update_parent_cat(db: Session, parent_cat_id: int,
                      new_parent_cat: s_parent_cat.ParentCatUpdate):
    """
    Update an existing parent cat in the database.
    """
    db_parent_cat = get_parent_cat_by_id(db=db, parent_cat_id=parent_cat_id)
    if not db_parent_cat:
        return None
    db_parent_cat.title = new_parent_cat.title
    db.commit()
    db.refresh(db_parent_cat)
    return db_parent_cat


def delete_parent_cat(db: Session, parent_cat_id: int, post_new: PostUpdate):
    """
    Delete a parent cat from the database.
    """
    db_parent_cat = get_parent_cat_by_id(db=db, parent_cat_id=parent_cat_id)
    if not db_parent_cat:
        return None
    db_sub_cats_with_parent_cat_id = get_sub_cat_by_parent_id(db, parent_cat_id)
    for sub_cat in db_sub_cats_with_parent_cat_id:
        delete_sub_cat(db=db, sub_cat_id=sub_cat.id, post_new=post_new)
    db.delete(db_parent_cat)
    db.commit()
    return {"status": "successfully deleted"}
