from pydantic import BaseModel
from enum import Enum


class CategoryEnum(str, Enum):
    CAR_BIKE_BOAT = "Car, Bike & Boat"
    ELECTRONICS = "Electronics"
    HOME_GARDEN = "Home & Garden"
    JOBS = "Jobs"
    NEIGHBOURHOOD_HELP = "Neighbourhood Help"
    SERVICES = "Services"
    FAMILY_CHILD_BABY = "Family, Child & Baby"
    PETS = "Pets"
    FASHION_BEAUTY = "Fashion & Beauty"
    LESSONS_COURSES = "Lessons & Courses"
    ADMISSION_TICKETS = "Admission tickets & tickets"
    LEISURE_HOBBIES = "Leisure, hobbies & neighbourhood"
    REAL_ESTATE = "Real Estate"
    MUSIC_MOVIES_BOOKS = "Music, Movies & Books"
    GIVE_AWAY_SWAP = "Give away & Swap"
    UNDEFINED = "Undefined"


class ParentCatBase(BaseModel):
    title: CategoryEnum | None = CategoryEnum.UNDEFINED


class ParentCatUpdate(BaseModel):
    title: CategoryEnum


class ParentCatCreate(ParentCatBase):
    pass


class ParentCatInDB(ParentCatBase):
    id: int

    class Config:
        orm_mode = True


class ParentCat(ParentCatInDB):
    pass
