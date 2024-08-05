from pydantic import BaseModel, EmailStr
from datetime import date, datetime


class UserBase(BaseModel):
    first_name: str
    last_name: str
    birthday: date
    username: str
    email: EmailStr
    tel_number: str | None = None
    profile_picture_path: str | None = "laptop-4948838_1280.jpg"
    street: str
    house_number: str
    zip_code: str
    city_town_village: str
    country: str
    commercial_account: bool | None = False
    notification: bool | None = True
    account_status: bool | None = True


class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    birthday: date | None = None
    username: str | None = None
    email: EmailStr | None = None
    tel_number: str | None = None
    profile_picture_path: str | None = None
    street: str | None = None
    house_number: str | None = None
    zip_code: str | None = None
    city_town_village: str | None = None
    country: str | None = None
    commercial_account: bool | None = None
    notification: bool | None = None
    account_status: bool | None = None
    password: str | None = None


class UserCreate(UserBase):
    password: str


class UserInDBBase(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class User(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    hashed_password: str
