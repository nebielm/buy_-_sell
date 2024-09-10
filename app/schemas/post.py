from pydantic import BaseModel, ConfigDict
from datetime import datetime
from enum import Enum


class StatusEnum(str, Enum):
    AVAILABLE = "available"
    RESERVED = "reserved"
    NOT_AVAILABLE = "not available"


class PostBase(BaseModel):
    title: str
    use_payment_option: bool | None = True
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


class PostCreateBase(PostBase):
    sub_category_id: int | None = 139
    description: str | None = None


class PostCreate(PostCreateBase):
    user_id: int


class PostInDB(PostBase):
    id: int
    user_id: int
    description: str
    created_at: datetime
    sub_category_id: int

    model_config = ConfigDict(arbitrary_types_allowed=True)


class Post(PostInDB):
    pass
