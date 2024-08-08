from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class WatchlistUser(Base):
    __tablename__ = "watchlist_user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    following_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    followed_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    following_user = relationship("User", foreign_keys=[following_user_id], back_populates="following_users")
    followed_user = relationship("User", foreign_keys=[followed_user_id], back_populates="followed_users")
