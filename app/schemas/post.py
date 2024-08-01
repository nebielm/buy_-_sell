from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class StatusEnum(str, Enum):
    AVAILABLE = "available"
    RESERVED = "reserved"
    NOT_AVAILABLE = "not available"


class PostBase(BaseModel):
    title: str
    use_payment_option: Optional[bool] = True
    description: str
    price: Optional[float] = 0.00
    condition: str
    quantity: Optional[int] = 1
    pick_up: Optional[bool] = False
    status: StatusEnum = StatusEnum.AVAILABLE
    show_email: Optional[bool] = True
    show_tel: Optional[bool] = True


class PostUpdate(BaseModel):
    title: Optional[str] = None
    use_payment_option: Optional[bool] = None
    description: Optional[str] = None
    price: Optional[float] = None
    condition: Optional[str] = None
    quantity: Optional[int] = None
    pick_up: Optional[bool] = None
    status: Optional[StatusEnum] = None
    show_email: Optional[bool] = None
    show_tel: Optional[bool] = None


class PostCreate(PostBase):
    pass


class PostInDB(PostBase):
    id: int
    user_id: int
    created_at: datetime
    sub_category_id: int

    class Config:
        orm_mode = True
