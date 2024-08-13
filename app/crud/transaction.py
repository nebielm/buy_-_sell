from sqlalchemy.orm import Session
from app.models import transaction as m_transaction
from app.schemas import transaction as s_transaction


def get_transaction_by_id(db: Session, transaction_id: int):
    return db.query(m_transaction.Transaction).filter(m_transaction.Transaction.id == transaction_id).first()


def get_transaction_by_buyer_id(db: Session, buyer_id: int):
    return db.query(m_transaction.Transaction).filter(m_transaction.Transaction.buyer_id == buyer_id).all()


def get_transaction_by_seller_id(db: Session, seller_id: int):
    return db.query(m_transaction.Transaction).filter(m_transaction.Transaction.seller_id == seller_id).all()


def get_transaction_by_post_id(db: Session, post_id: int):
    return db.query(m_transaction.Transaction).filter(m_transaction.Transaction.post_id == post_id).all()


def create_transaction(db: Session, transaction: s_transaction.TransactionCreate):
    db_transaction = m_transaction.Transaction(**transaction.model_dump())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


def update_transaction(db: Session, transaction_id: int, new_transaction: s_transaction.TransactionUpdate):
    db_transaction = get_transaction_by_id(db=db, transaction_id=transaction_id)
    if not db_transaction:
        return None
    if new_transaction:
        if new_transaction.price:
            db_transaction.price = new_transaction.price
        if new_transaction.quantity:
            db_transaction.quantity = new_transaction.quantity
        if new_transaction.status:
            db_transaction.status = new_transaction.status
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


def delete_transaction(db: Session, transaction_id: int):
    db_transaction = get_transaction_by_id(db=db, transaction_id=transaction_id)
    if not db_transaction:
        return None
    db.delete(db_transaction)
    db.commit()
    return {"status": "successfully deleted"}
