from typing import Annotated
from pydantic import BaseModel, Field, ConfigDict


class PictureBase(BaseModel):
    """
    Base schema for a picture.
    """
    image_path: Annotated[str, Field(min_length=5)]


class PictureUpdate(BaseModel):
    """
    Schema for updating a picture.
    """
    image_path: Annotated[str, Field(min_length=5)]


class PictureCreate(PictureBase):
    """
    Schema for creating a new picture.
    """
    post_id: int


class PictureInDB(PictureBase):
    """
    Schema representing a picture stored in the database.
    """
    id: int
    post_id: int

    model_config = ConfigDict(arbitrary_types_allowed=True)


class Picture(PictureInDB):
    """
    Schema for returning parent category data in API responses.
    """
    pass
