from datetime import datetime
from pydantic import BaseModel, ConfigDict


class MessageBase(BaseModel):
    """
    Base schema for a message containing only the message content.
    """
    message: str


class MessageUpdate(BaseModel):
    """
    Schema for updating a message.
    """
    message: str


class MessageCreateBase(MessageBase):
    """
    Schema for creating a new message, which infos is given by user.
    """
    receiver_id: int


class MessageCreate(MessageCreateBase):
    """
    Full Schema for creating a new message.
    """
    sender_id: int
    post_id: int


class MessageInDB(MessageBase):
    """
    Schema representing a message stored in the database.
    """
    id: int
    sender_id: int
    receiver_id: int
    post_id: int
    last_message_change: datetime

    model_config = ConfigDict(arbitrary_types_allowed=True)


class Message(MessageInDB):
    """
    Schema for returning message data in API responses.
    """
    pass
