from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.schemas import transaction as s_transaction
from app.crud import transaction as c_transaction
from app.crud import post as c_post
from app.models import user as m_user
from app.database import get_db

router = APIRouter()


@router.post("/users/{user_id}/post/{post_id}/transaction/", response_model=s_transaction.Transaction)
def create_transaction(user_id: int, post_id: int, transaction_base: s_transaction.TransactionCreateBase,
                       db: Session = Depends(get_db), current_user: m_user.User = Depends(get_current_user)):
    if user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Authentication failed")
    db_post = c_post.get_post_by_id(db=db, post_id=post_id)
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Post not in DB.")
    if db_post.user_id == user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Cant buy your own stuff, you already own it")
    if transaction_base.quantity > db_post.quantity:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Quantity not  available.")
    total_amount = db_post.price * transaction_base.quantity
    if total_amount != transaction_base.price:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Price not correct. Seller: adjust price in Post or Buyer: adjust quantity")
    transaction_data = transaction_base.model_dump()
    transaction = s_transaction.TransactionCreate(**transaction_data, buyer_id=user_id,
                                                  post_id=post_id, seller_id=db_post.user_id)
    return c_transaction.create_transaction(db=db, transaction=transaction)


@router.get("/users/{user_id}/post/{post_id}/transaction/", response_model=list[s_transaction.Transaction])
def get_transaction_by_post_id(user_id: int, post_id: int, db: Session = Depends(get_db),
                               current_user: m_user.User = Depends(get_current_user)):
    if user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Authentication failed or "
                                   "User ID is in URL not the Buyer ID in Request Body.")
    db_transactions = c_transaction.get_transaction_by_post_id(db=db, post_id=post_id)
    if not db_transactions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Transaction with given Post ID not in DB.")
    for transaction in db_transactions:
        if transaction.buyer_id == user_id or transaction.seller_id == user_id:
            return db_transactions
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail="User ID is in URL not the Buyer or Seller")


@router.get("/users/{user_id}/transaction/{transaction_id}/", response_model=s_transaction.Transaction)
def get_transaction_by_transaction_id(user_id: int, transaction_id: int, db: Session = Depends(get_db),
                                      current_user: m_user.User = Depends(get_current_user)):
    if user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Authentication failed or "
                                   "User ID is in URL not the Buyer ID in Request Body.")
    db_transaction = c_transaction.get_transaction_by_id(db=db, transaction_id=transaction_id)
    if not db_transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Transaction with not in DB.")
    if db_transaction.buyer_id != user_id and db_transaction.seller_id != user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="User ID is in URL not the Buyer or Seller")
    return db_transaction


@router.get("/users/{user_id}/sent_transaction/", response_model=list[s_transaction.Transaction])
def get_sent_transactions(user_id: int, db: Session = Depends(get_db),
                          current_user: m_user.User = Depends(get_current_user)):
    if user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Authentication failed or "
                                   "User ID is in URL not the Buyer ID in Request Body.")
    db_transactions = c_transaction.get_transaction_by_buyer_id(db=db, buyer_id=user_id)
    if not db_transactions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User ID is in URL not the Buyer")
    return db_transactions


@router.get("/users/{user_id}/received_transaction/", response_model=list[s_transaction.Transaction])
def get_received_transactions(user_id: int, db: Session = Depends(get_db),
                              current_user: m_user.User = Depends(get_current_user)):
    if user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Authentication failed or "
                                   "User ID is in URL not the Buyer ID in Request Body.")
    db_transactions = c_transaction.get_transaction_by_seller_id(db=db, seller_id=user_id)
    if not db_transactions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User ID is in URL not the Seller")
    return db_transactions


@router.put("/users/{user_id}/transaction/{transaction_id}/", response_model=s_transaction.Transaction)
def update_transaction(user_id: int, transaction_id: int, new_transaction: s_transaction.TransactionUpdate,
                       db: Session = Depends(get_db), current_user: m_user.User = Depends(get_current_user)):
    if user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Authentication failed or "
                                   "User ID is in URL not the Buyer ID in Request Body.")
    db_transaction = c_transaction.get_transaction_by_id(db=db, transaction_id=transaction_id)
    if not db_transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Transaction with not in DB.")
    if db_transaction.buyer_id != user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="User ID is in URL not the Buyer")
    db_post = c_post.get_post_by_id(db=db, post_id=db_transaction.seller_id)
    if new_transaction.quantity or new_transaction.price:
        if new_transaction.quantity > db_post.quantity:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Quantity not  available.")
        total_amount = db_post.price * new_transaction.quantity
        if total_amount != new_transaction.price:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Price not correct.")
    return c_transaction.update_transaction(db=db, transaction_id=transaction_id, new_transaction=new_transaction)


@router.delete("/users/{user_id}/transaction/{transaction_id}/")
def delete_transaction(user_id: int, transaction_id: int, db: Session = Depends(get_db),
                       current_user: m_user.User = Depends(get_current_user)):
    if user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Authentication failed or "
                                   "User ID is in URL not the Buyer ID in Request Body.")
    db_transaction = c_transaction.get_transaction_by_id(db=db, transaction_id=transaction_id)
    if not db_transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Transaction with not in DB.")
    if db_transaction.buyer_id != user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="User ID is in URL not the Buyer")
    if db_transaction.status == "successful":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Successful transactions can't be deleted.")
    return c_transaction.delete_transaction(db=db, transaction_id=transaction_id)
