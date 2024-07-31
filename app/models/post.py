from enum import Enum
from sqlalchemy import Enum as SQLAlchemyEnum, Column, Boolean, Float, Integer, String, ForeignKey, Date, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base


class StatusEnum(Enum):
    AVAILABLE = "available"
    RESERVED = "reserved"
    NOT_AVAILABLE = "not available"


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    use_payment_option = Column(Boolean, default=True)
    description = Column(String, nullable=False)
    price = Column(Float, default=0.00)
    condition = Column(String, nullable=True)
    quantity = Column(Integer, default=1)
    pick_up = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(SQLAlchemyEnum(StatusEnum), default=StatusEnum.AVAILABLE, nullable=False)
    show_email = Column(Boolean, default=True)
    show_tel = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    sub_category_id = Column(Integer, ForeignKey("sub_category.id"), nullable=False)

    user = relationship("User", back_populates="posts")
    sub_category = relationship("Sub_Category", back_populates="posts")
