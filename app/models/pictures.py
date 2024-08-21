from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Picture(Base):
    __tablename__ = "pictures"

    id = Column(Integer, primary_key=True, autoincrement=True)
    image_path = Column(String, default="https://buysellusers.s3.eu-north-1.amazonaws.com/default.jpg")
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)

    post = relationship("Post", back_populates="pictures")
