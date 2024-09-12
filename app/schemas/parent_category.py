from enum import Enum
from pydantic import BaseModel, ConfigDict


class CategoryEnum(str, Enum):
    """
    Enumeration representing different Parent categories of items or services.
    """
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
    """
    Base schema for a parent category.
    """
    title: CategoryEnum | None = CategoryEnum.UNDEFINED


class ParentCatUpdate(BaseModel):
    """
    Schema for updating a parent category.
    """
    title: CategoryEnum


class ParentCatCreate(ParentCatBase):
    """
    Schema for creating a new parent category.
    """
    pass


class ParentCatInDB(ParentCatBase):
    """
    Schema representing a parent category stored in the database.
    """
    id: int

    model_config = ConfigDict(arbitrary_types_allowed=True)


class ParentCat(ParentCatInDB):
    """
    Schema for returning parent category data in API responses.
    """
    pass
