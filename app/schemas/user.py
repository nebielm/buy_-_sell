from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, datetime


class UserBase(BaseModel):
    first_name: str
    last_name: str
    birthday: date
    username: str
    email: EmailStr
    tel_number: Optional[str] = None
    profile_picture_path: Optional[str] = "laptop-4948838_1280.jpg"
    street: str
    house_number: str
    zip_code: str
    city_town_village: str
    country: str
    commercial_account: Optional[bool] = False
    notification: Optional[bool] = True
    account_status: Optional[bool] = True


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    birthday: Optional[date] = None
    # username: str
    # email: EmailStr
    tel_number: Optional[str] = None
    profile_picture_path: Optional[str] = None
    street: Optional[str] = None
    house_number: Optional[str] = None
    zip_code: Optional[str] = None
    city_town_village: Optional[str] = None
    country: Optional[str] = None
    commercial_account: Optional[bool] = None
    notification: Optional[bool] = None
    account_status: Optional[bool] = None


class UserCreate(UserBase):
    hashed_password: str


class UserInDBBase(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class User(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    hashed_password: str
