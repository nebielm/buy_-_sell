from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class SubCat(Base):
    __tablename__ = "sub_categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, unique=True, nullable=False)
    parent_id = Column(Integer, ForeignKey("parent_categories.id"), nullable=False)

    post = relationship("Post", back_populates="sub_category")
    parent_cat = relationship("ParentCat", back_populates="subcategories")
