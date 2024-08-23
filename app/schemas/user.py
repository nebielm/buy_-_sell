from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import date, datetime


class UserBase(BaseModel):
    first_name: str
    last_name: str
    birthday: date
    username: str
    email: EmailStr
    tel_number: str | None = None
    street: str
    house_number: str
    zip_code: str
    city_town_village: str
    country: str
    commercial_account: bool | None = False
    notification: bool | None = True
    account_status: bool | None = True


class UserUpdateBase(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    birthday: date | None = None
    username: str | None = None
    email: EmailStr | None = None
    tel_number: str | None = None
    street: str | None = None
    house_number: str | None = None
    zip_code: str | None = None
    city_town_village: str | None = None
    country: str | None = None
    commercial_account: bool | None = None
    notification: bool | None = None
    account_status: bool | None = None
    password: str | None = None


class UserUpdate(UserUpdateBase):
    profile_picture_path: str | None = None


class UserCreate(UserBase):
    password: str
    profile_picture_path: str | None = "https://buysellusers.s3.eu-north-1.amazonaws.com/default.jpg"


class UserInDBBase(UserBase):
    id: int
    created_at: datetime
    profile_picture_path: str

    model_config = ConfigDict(arbitrary_types_allowed=True)


class User(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    hashed_password: str
