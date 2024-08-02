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
    tel_number = Column(String, index=True, nullable=True)
    profile_picture_path = Column(String, default="laptop-4948838_1280.jpg")
    street = Column(String, index=True, nullable=False)
    house_number = Column(String, nullable=False)
    zip_code = Column(String, index=True, nullable=False)
    city_town_village = Column(String, index=True, nullable=False)
    country = Column(String, index=True, nullable=False)
    commercial_account = Column(Boolean, default=False)
    notification = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    account_status = Column(Boolean, default=True)

    posts = relationship("Post", back_populates="user")
