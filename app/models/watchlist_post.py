from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class WatchlistPost(Base):
    __tablename__ = "watchlist_post"

    id = Column(Integer, primary_key=True, autoincrement=True)
    following_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    followed_post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)

    following_user = relationship("User", foreign_keys=[following_user_id], back_populates="watchlist_posts")
    followed_post = relationship("Post", foreign_keys=[followed_post_id], back_populates="watchlist_posts")
