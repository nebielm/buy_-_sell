from sqlalchemy.orm import Session
from app.core.security import get_password_hashed
from app.models import user as m_user
from app.schemas import user as s_user


def get_user_by_id(db: Session, user_id: int):
    return db.query(m_user.User).filter(m_user.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(m_user.User).filter(m_user.User.username == username).first()


def get_user_by_email(db: Session, user_email: str):
    return db.query(m_user.User).filter(m_user.User.email == user_email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(m_user.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: s_user.UserCreate):
    hashed_password = get_password_hashed(user.password)
    db_user = m_user.User(**user.model_dump(exclude={"password"}), hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int,  user_new: s_user.UserUpdate):
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None
    if user_new.email and get_user_by_email(db, user_new.email) and user_id != db_user.id:
        return None
    if user_new.username and get_user_by_username(db, user_new.username) and user_id != db_user.id:
        return None
    user_data = user_new.model_dump(exclude_unset=True)
    if "password" in user_data:
        if user_data["password"] is not None:
            user_data["hashed_password"] = get_password_hashed(user_data["password"])
        user_data.pop("password", None)
    for attr, value in user_data.items():
        if value:
            setattr(db_user, attr, value)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None
    db.delete(db_user)
    db.commit()
    return {"status": "successfully deleted"}
