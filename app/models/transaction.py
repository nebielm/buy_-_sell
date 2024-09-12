from enum import Enum
from sqlalchemy import Enum as SQLAlchemyEnum, Column, Integer, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.event import listens_for
from app.database import Base


class TStatusEnum(str, Enum):
    """
    Enumeration representing the possible statuses of an item.
    """
    IN_PROGRESS = "in_progress"
    SUCCESSFUL = "successful"
    DECLINED = "declined"


class Transaction(Base):
    """
    Represents a Transaction in the database.
    """
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    buyer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    price = Column(Float, default=1.00, nullable=False)
    quantity = Column(Integer, default=1, nullable=False)
    status = Column(SQLAlchemyEnum(TStatusEnum), default=TStatusEnum.IN_PROGRESS, nullable=False)
    last_status_change = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    buyer = relationship("User", foreign_keys=[buyer_id], back_populates="purchases")
    seller = relationship("User", foreign_keys=[seller_id], back_populates="sales")
    post = relationship("Post", back_populates="transactions")


@listens_for(Transaction, 'before_update')
def update_last_status_change(mapper, connection, target):
    """
    Listener function that updates the `last_status_change` field of a Transaction
    entity before an update occurs, if the status has changed.
    """
    target_id = target.id
    previous_transaction = connection.execute(
        mapper.local_table.select()
        .where(mapper.local_table.c.id == target_id)
    ).fetchone()
    if previous_transaction:
        previous_status = previous_transaction.status
        if target.status != previous_status:
            target.last_status_change = func.now()
