from sqlalchemy.orm import Session
from app.models import pictures as m_picture
from app.schemas import pictures as s_picture


def get_picture_by_id(db: Session, picture_id: int):
    """
    Retrieve a picture by its ID.
    """
    return db.query(m_picture.Picture).filter(m_picture.Picture.id == picture_id).first()


def get_picture_by_image_path(db: Session, picture_image_path: str):
    """
    Retrieve a picture by its image path.
    """
    return (db.query(m_picture.Picture).filter
            (m_picture.Picture.image_path == picture_image_path).all())


def get_picture_by_post_id(db: Session, post_id: int):
    """
    Retrieve pictures by their post ID.
    """
    return db.query(m_picture.Picture).filter(m_picture.Picture.post_id == post_id).all()


def create_picture(db: Session, picture: s_picture.PictureCreate):
    """
    Create and add a new picture to the database.
    """
    db_picture = m_picture.Picture(**picture.model_dump())
    db.add(db_picture)
    db.commit()
    db.refresh(db_picture)
    return db_picture


def update_picture(db: Session, picture_id: int, new_picture: s_picture.PictureUpdate):
    """
    Update an existing picture in the database.
    """
    db_picture = get_picture_by_id(db=db, picture_id=picture_id)
    if not db_picture:
        return None
    db_picture.image_path = new_picture.image_path
    db.commit()
    db.refresh(db_picture)
    return db_picture


def delete_picture(db: Session, picture_id: int):
    """
    Delete a picture from the database.
    """
    db_picture = get_picture_by_id(db=db, picture_id=picture_id)
    if not db_picture:
        return None
    db.delete(db_picture)
    db.commit()
    return {"status": "successfully deleted"}
