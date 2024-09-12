from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Picture(Base):
    """
    Represents a picture entity in the database.
    """
    __tablename__ = "pictures"

    id = Column(Integer, primary_key=True, autoincrement=True)
    image_path = Column(String, default="https://buysellpostpics.s3.amazonaws.com/01919976-385e-"
                                        "7a60-8eeb-7ab00c13e0cf_28_08_2024_16_49_07_"
                                        "default_post_pic.jpg")
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)

    post = relationship("Post", back_populates="pictures")
