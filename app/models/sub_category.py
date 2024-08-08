from enum import Enum
from sqlalchemy import Enum as SQLAlchemyEnum, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class StatusEnum(str, Enum):
    CARS = "Cars"
    CAR_PARTS = "Car Parts & Tiers"
    BOATS = "Boats & Accessories"
    BICYCLES = "Bicycles & Accessories"
    MOTORCYCLES = "Motorcycle & Scooters"
    MOTORCYCLES_PARTS = "Motorcycle Parts & Accessories"
    COMMERCIAL_VEHICLES_TRAILERS = "Commercial Vehicles & Trailers"
    REPAIRS_SERVICES = "Repairs & Services"
    CARAVANS = "Caravans & Mobile Homes"
    OTHER_CARS_BIKES_BOATS = "Other Car, Bike & Boat"
    UNDEFINED = "undefined"


class SubCat(Base):
    __tablename__ = "sub_categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(SQLAlchemyEnum(StatusEnum), default=StatusEnum.UNDEFINED, nullable=False)
    parent_id = Column(Integer, ForeignKey("parent_categories.id"), nullable=False)

    post = relationship("Post", back_populates="sub_category")
    parent_cat = relationship("ParentCat", back_populates="subcategories")
