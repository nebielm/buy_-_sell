from pydantic import BaseModel
from datetime import datetime


class MessageBase(BaseModel):
    message: str


class MessageUpdate(BaseModel):
    message: str


class MessageCreate(MessageBase):
    sender_id: int
    receiver_id: int
    post_id: int


class MessageInDB(MessageBase):
    id: int
    sender_id: int
    receiver_id: int
    post_id: int
    last_message_change: datetime

    class Config:
        orm_mode = True


class Message(MessageInDB):
    pass
