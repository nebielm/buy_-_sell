from sqlalchemy.orm import Session
from app.models import pictures as m_picture
from app.schemas import pictures as s_picture


def get_picture_by_id(db: Session, picture_id: int):
    return db.query(m_picture.Picture).filter(m_picture.Picture.id == picture_id).first()


def get_picture_by_image_path(db: Session, picture_image_path: str):
    return db.query(m_picture.Picture).filter(m_picture.Picture.image_path == picture_image_path).all()


def get_picture_by_post_id(db: Session, post_id: int):
    return db.query(m_picture.Picture).filter(m_picture.Picture.post_id == post_id).first()


def create_message(db: Session, picture: s_picture.PictureCreate):
    db_picture = m_picture.Picture(**picture.model_dump())
    db.add(db_picture)
    db.commit()
    db.refresh(db_picture)
    return db_picture


def update_message(db: Session, picture_id: int, new_picture: s_picture.PictureUpdate):
    db_picture = get_picture_by_id(db=db, picture_id=picture_id)
    if not db_picture:
        return None
    db_picture.image_path = new_picture.image_path
    db.commit()
    db.refresh(db_picture)
    return db_picture


def delete_message(db: Session, picture_id: int):
    db_picture = get_picture_by_id(db=db, picture_id=picture_id)
    if not db_picture:
        return None
    db.delete(db_picture)
    db.commit()
    return {"status": "successfully deleted"}
