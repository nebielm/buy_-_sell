from datetime import date, datetime
from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    """
    Base schema for a user.
    """
    first_name: str
    last_name: str
    birthday: date
    username: str
    email: EmailStr
    tel_number: str
    street: str
    house_number: str
    zip_code: str
    city_town_village: str
    country: str
    commercial_account: bool | None = False
    notification: bool | None = True
    account_status: bool | None = True


class UserUpdateBase(BaseModel):
    """
    Base Schema for updating a user.
    """
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
    """
    Full Schema for updating a user.
    """
    profile_picture_path: str


class UserCreateBase(UserBase):
    """
    Base Schema for creating a new user.
    """
    password: str


class UserCreate(UserCreateBase):
    """
    Full Schema for creating a new user.
    """
    profile_picture_path: str


class UserInDBBase(UserBase):
    """
    Base Schema representing a user stored in the database.
    """
    id: int
    created_at: datetime
    profile_picture_path: str

    model_config = ConfigDict(arbitrary_types_allowed=True)


class User(UserInDBBase):
    """
    Schema for returning transaction data in API responses.
    """
    pass


class UserInDB(UserInDBBase):
    """
    Full Schema representing a user stored in the database.
    """
    hashed_password: str
