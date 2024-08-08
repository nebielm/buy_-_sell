from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class ParentCat(Base):
    __tablename__ = "parent_categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, unique=True, nullable=False)

    subcategories = relationship("SubCat", back_populates="parent_cat")
