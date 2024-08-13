from enum import Enum
from datetime import datetime
from pydantic import BaseModel


class StatusEnum(str, Enum):
    IN_PROGRESS = "in_progress"
    SUCCESSFUL = "successful"
    DECLINED = "declined"


class TransactionBase(BaseModel):
    price: float | None = 1.00
    quantity: int | None = 1
    status: StatusEnum | None = StatusEnum.IN_PROGRESS


class TransactionUpdate(BaseModel):
    price: float | None = None
    quantity: int | None = None
    status: StatusEnum | None = None


class TransactionCreate(TransactionBase):
    buyer_id: int
    seller_id: int
    post_id: int


class TransactionInDB(TransactionBase):
    id: int
    buyer_id: int
    seller_id: int
    post_id: int
    last_status_change: datetime

    class Config:
        orm_mode = True


class Transaction(TransactionInDB):
    pass
