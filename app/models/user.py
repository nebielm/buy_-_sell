from sqlalchemy import Column, Boolean, Integer, String, Date, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    birthday = Column(Date, nullable=False)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    tel_number = Column(String, index=True, nullable=False)
    profile_picture_path = Column(String, nullable=False)
    street = Column(String, index=True, nullable=False)
    house_number = Column(String, nullable=False)
    zip_code = Column(String, index=True, nullable=False)
    city_town_village = Column(String, index=True, nullable=False)
    country = Column(String, index=True, nullable=False)
    commercial_account = Column(Boolean, default=False)
    notification = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    account_status = Column(Boolean, default=True)

    post = relationship("Post", back_populates="user", cascade="all, delete-orphan")
    sent_messages = relationship("Message", foreign_keys="Message.sender_id", back_populates="sender",
                                 cascade="all, delete-orphan")
    received_messages = relationship("Message", foreign_keys="Message.receiver_id", back_populates="receiver",
                                     cascade="all, delete-orphan")
    watchlist_posts = relationship("WatchlistPost", foreign_keys="WatchlistPost.following_user_id",
                                   back_populates="following_user", cascade="all, delete-orphan")
    following_users = relationship("WatchlistUser", foreign_keys="WatchlistUser.following_user_id",
                                   back_populates="following_user", cascade="all, delete-orphan")
    followed_users = relationship("WatchlistUser", foreign_keys="WatchlistUser.followed_user_id",
                                  back_populates="followed_user", cascade="all, delete-orphan")
    purchases = relationship("Transaction", foreign_keys="Transaction.buyer_id", back_populates="buyer",
                             cascade="all, delete-orphan")
    sales = relationship("Transaction", foreign_keys="Transaction.seller_id", back_populates="seller",
                         cascade="all, delete-orphan")
