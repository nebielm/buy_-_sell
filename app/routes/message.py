from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.schemas import message as s_message
from app.crud import message as c_message
from app.crud import post as c_post
from app.models import user as m_user
from app.database import get_db

router = APIRouter()


@router.post("/users/{user_id}/post/{post_id}/message", response_model=s_message.Message)
def create_message(user_id: int, post_id: int, base_message: s_message.MessageCreateBase, db: Session = Depends(get_db),
                   current_user: m_user.User = Depends(get_current_user)):
    if user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed")
    post = c_post.get_post_by_id(db=db, post_id=post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post in URL path does not exist in DB")
    if base_message.receiver_id == user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Cant send message to yourself.")
    if post.user_id != user_id and post.user_id != base_message.receiver_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Sender or Receiver ID not in association with Post ID in URL")
    if post.user_id == user_id:
        post_messages = c_message.get_message_by_post_id(db=db, post_id=post_id)
        found_message = False
        for message in post_messages:
            if message.sender_id == base_message.receiver_id:
                found_message = True
        if not found_message:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Potential buyer has to contact seller first.")
    message_data = base_message.model_dump()
    message = s_message.MessageCreate(**message_data, post_id=post_id, sender_id=user_id)
    return c_message.create_message(db=db, message=message)


@router.get("/users/{user_id}/post/{post_id}/message", response_model=list[s_message.Message])
def get_my_messages_by_post(user_id: int, post_id: int, db: Session = Depends(get_db),
                            current_user: m_user.User = Depends(get_current_user)):
    if user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Authentication failed")
    post = c_post.get_post_by_id(db=db, post_id=post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Post in URL path does not exist in DB")
    messages_by_post = c_message.get_message_by_post_id(db=db, post_id=post_id)
    my_messages_by_post = []
    for message in messages_by_post:
        if message.sender_id == user_id or message.receiver_id == user_id:
            my_messages_by_post.append(message)
    if not my_messages_by_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No messages found for the user related to this post.")
    return my_messages_by_post


@router.get("/users/{user_id}/messages")
def get_all_my_messages(user_id: int, db: Session = Depends(get_db),
                        query: str = Query(enum=["sent", "received", "both"], default="both"),
                        current_user: m_user.User = Depends(get_current_user)):
    if user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Authentication failed")
    sent_messages = c_message.get_message_by_sender_id(db=db, sender_id=user_id)
    received_messages = c_message.get_message_by_receiver_id(db=db, receiver_id=user_id)
    if query == "sent":
        return sent_messages
    elif query == "received":
        return received_messages
    elif query == "both":
        return {"sent_messages": sent_messages, "received_messages": received_messages}


@router.put("/users/{user_id}/messages/{message_id}/", response_model=s_message.Message)
def update_message(user_id: int, message_id: int, new_message: s_message.MessageUpdate,
                   db: Session = Depends(get_db), current_user: m_user.User = Depends(get_current_user)):
    if user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Authentication failed")
    db_message = c_message.get_message_by_id(db=db, message_id=message_id)
    if db_message.sender_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="User ID in the request body did not send the message with given Message ID")
    post_messages = c_message.get_message_by_post_id(db=db, post_id=db_message.post_id)
    for message in post_messages:
        if message.last_message_change > db_message.last_message_change:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Given Message ID not last message in conversation")
    print(db_message.last_message_change)
    return c_message.update_message(db=db, message_id=message_id, new_message=new_message)


@router.delete("/users/{user_id}/messages/{message_id}/")
def delete_message(user_id: int, message_id: int, db: Session = Depends(get_db),
                   current_user: m_user.User = Depends(get_current_user)):
    if user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Authentication failed")
    db_message = c_message.get_message_by_id(db=db, message_id=message_id)
    if db_message.sender_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="User ID in the request body did not send the message with given Message ID")
    post_messages = c_message.get_message_by_post_id(db=db, post_id=db_message.post_id)
    for message in post_messages:
        if message.last_message_change > db_message.last_message_change:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Given Message ID not last message in conversation")
    return c_message.delete_message(db=db, message_id=message_id)
