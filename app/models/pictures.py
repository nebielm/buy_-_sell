from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Picture(Base):
    __tablename__ = "pictures"

    id = Column(Integer, primary_key=True, autoincrement=True)
    image_path = Column(String, default="laptop-4948838_1280.jpg")
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)

    post = relationship("Post", back_populates="pictures")
