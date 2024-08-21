from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Annotated


class PictureBase(BaseModel):
    image_path: Annotated[str, Field(min_length=5)]

    @field_validator('image_path')
    def validate_path_ext(cls, value):
        valid_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg')
        if not value.lower().endswith(valid_extensions):
            raise ValueError('Invalid image format')
        return value


class PictureUpdate(BaseModel):
    image_path: Annotated[str, Field(min_length=5)]

    @field_validator('image_path')
    def validate_path_ext(cls, value):
        valid_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg')
        if not value.lower().endswith(valid_extensions):
            raise ValueError('Invalid image format')
        return value


class PictureCreate(PictureBase):
    post_id: int


class PictureInDB(PictureBase):
    id: int
    post_id: int

    model_config = ConfigDict(arbitrary_types_allowed=True)


class Picture(PictureInDB):
    pass
