from pydantic import BaseModel


class MessageBase(BaseModel):
    message: str


class UpdateMessage(BaseModel):
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

    class Config:
        orm_mode = True


class Message(MessageInDB):
    pass
