from datetime import datetime
from enum import Enum
from pydantic import BaseModel, ConfigDict


class StatusEnum(str, Enum):
    """
    Enumeration representing the possible status of a post.
    """
    AVAILABLE = "available"
    RESERVED = "reserved"
    NOT_AVAILABLE = "not available"


class PostBase(BaseModel):
    """
    Base schema for a post.
    """
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
    """
    Schema for updating an existing post.
    """
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
    """
    Schema for creating a new post, which infos is given by user.
    """
    sub_category_id: int | None = 139
    description: str | None = None


class PostCreate(PostCreateBase):
    """
    Full Schema for creating a new post.
    """
    user_id: int


class PostInDB(PostBase):
    """
    Schema representing a post stored in the database.
    """
    id: int
    user_id: int
    description: str
    created_at: datetime
    sub_category_id: int

    model_config = ConfigDict(arbitrary_types_allowed=True)


class Post(PostInDB):
    """
    Schema for returning post data in API responses.
    """
    pass
