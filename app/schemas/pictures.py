from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated


class PictureBase(BaseModel):
    image_path: Annotated[str, Field(min_length=5)]


class PictureUpdate(BaseModel):
    image_path: Annotated[str, Field(min_length=5)]


class PictureCreate(PictureBase):
    post_id: int


class PictureInDB(PictureBase):
    id: int
    post_id: int

    model_config = ConfigDict(arbitrary_types_allowed=True)


class Picture(PictureInDB):
    pass
