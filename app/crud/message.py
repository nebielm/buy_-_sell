from sqlalchemy.orm import Session
from app.models import message as m_message
from app.schemas import message as s_message


def get_message_by_id(db: Session, message_id: int):
    return db.query(m_message.Message).filter(m_message.Message.id == message_id).first()


def get_message_by_sender_id(db: Session, sender_id: int):
    return db.query(m_message.Message).filter(m_message.Message.sender_id == sender_id).all()


def get_message_by_receiver_id(db: Session, receiver_id: int):
    return db.query(m_message.Message).filter(m_message.Message.receiver_id == receiver_id).all()


def get_message_by_post_id(db: Session, post_id: int):
    return db.query(m_message.Message).filter(m_message.Message.post_id == post_id).all()


def get_messages(db: Session, skip: int = 0, limit: int = 100):
    return db.query(m_message.Message).offset(skip).limit(limit).all()


def create_message(db: Session, message: s_message.MessageCreate):
    db_message = m_message.Message(**message.model_dump())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def update_message(db: Session, message_id: int, new_message: s_message.MessageUpdate):
    db_message = get_message_by_id(db=db, message_id=message_id)
    if not db_message:
        return None
    db_message.message = new_message.message
    db.commit()
    db.refresh(db_message)
    return db_message


def delete_message(db: Session, message_id: int):
    db_message = get_message_by_id(db=db, message_id=message_id)
    if not db_message:
        return None
    db.delete(db_message)
    db.commit()
    return {"status": "successfully deleted"}
