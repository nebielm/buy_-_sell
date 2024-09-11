from datetime import datetime
from pydantic import BaseModel, ConfigDict


class MessageBase(BaseModel):
    message: str


class MessageUpdate(BaseModel):
    message: str


class MessageCreateBase(MessageBase):
    receiver_id: int


class MessageCreate(MessageCreateBase):
    sender_id: int
    post_id: int


class MessageInDB(MessageBase):
    id: int
    sender_id: int
    receiver_id: int
    post_id: int
    last_message_change: datetime

    model_config = ConfigDict(arbitrary_types_allowed=True)


class Message(MessageInDB):
    pass
