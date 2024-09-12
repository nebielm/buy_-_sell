from enum import Enum
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class TStatusEnum(str, Enum):
    """
    Enum representing the possible status of a transaction.
    """
    IN_PROGRESS = "in_progress"
    SUCCESSFUL = "successful"
    DECLINED = "declined"


class TransactionBase(BaseModel):
    """
    Base schema for a transaction.
    """
    price: float | None = 1.00
    quantity: int | None = 1
    status: TStatusEnum | None = TStatusEnum.IN_PROGRESS


class TransactionUpdate(BaseModel):
    """
    Schema for updating a transaction.
    """
    price: float | None = None
    quantity: int | None = None
    status: TStatusEnum | None = None


class TransactionCreateBase(TransactionBase):
    """
    Base schema for creating a new transaction.
    """
    pass


class TransactionCreate(TransactionCreateBase):
    """
    Full Schema for creating a new transaction.
    """
    buyer_id: int
    post_id: int
    seller_id: int


class TransactionInDB(TransactionBase):
    """
    Schema representing a transaction stored in the database.
    """
    id: int
    buyer_id: int
    seller_id: int
    post_id: int
    last_status_change: datetime

    model_config = ConfigDict(arbitrary_types_allowed=True)


class Transaction(TransactionInDB):
    """
    Schema for returning transaction data in API responses.
    """
    pass
