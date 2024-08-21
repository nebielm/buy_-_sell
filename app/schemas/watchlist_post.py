from pydantic import BaseModel, ConfigDict


class WatchPostBase(BaseModel):
    pass


class WatchPostUpdate(BaseModel):
    pass


class WatchPostCreate(WatchPostBase):
    following_user_id: int
    followed_post_id: int


class WatchPostInDB(WatchPostBase):
    id: int
    following_user_id: int
    followed_post_id: int

    model_config = ConfigDict(arbitrary_types_allowed=True)


class WatchPost(WatchPostInDB):
    pass
