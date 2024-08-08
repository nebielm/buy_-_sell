from enum import Enum
from sqlalchemy import Enum as SQLAlchemyEnum, Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class StatusEnum(str, Enum):
    IN_PROGRESS = "in_progress"
    SUCCESSFUL = "successful"
    DECLINED = "declined"


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    buyer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    price = Column(Float, default=1.00, nullable=False)
    quantity = Column(Integer, default=1, nullable=False)
    status = Column(SQLAlchemyEnum(StatusEnum), default=StatusEnum.IN_PROGRESS, nullable=False)

    buyer = relationship("User", foreign_keys=[buyer_id], back_populates="purchases")
    seller = relationship("User", foreign_keys=[seller_id], back_populates="sales")
    post = relationship("Post", back_populates="transactions")
