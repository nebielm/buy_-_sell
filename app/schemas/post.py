from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class StatusEnum(str, Enum):
    AVAILABLE = "available"
    RESERVED = "reserved"
    NOT_AVAILABLE = "not available"


class PostBase(BaseModel):
    title: str
    use_payment_option: bool | None = True
    description: str
    price: float | None = 0.00
    condition: str
    quantity: int | None = 1
    pick_up: bool | None = False
    status: StatusEnum = StatusEnum.AVAILABLE
    show_email: bool | None = True
    show_tel: bool | None = True


class PostUpdate(BaseModel):
    title: str | None = None
    use_payment_option: bool | None = None
    description: str | None = None
    price: float | None = None
    condition: str | None = None
    quantity: int | None = None
    pick_up: bool | None = None
    status: StatusEnum | None = None
    show_email: bool | None = None
    show_tel: bool | None = None
    sub_category_id: int | None = None


class PostCreate(PostBase):
    user_id: int
    sub_category_id: int


class PostInDB(PostBase):
    id: int
    user_id: int
    created_at: datetime
    sub_category_id: int

    class Config:
        orm_mode = True


class Post(PostInDB):
    pass
