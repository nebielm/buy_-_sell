from pydantic import BaseModel


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

    class Config:
        orm_mode = True


class WatchPost(WatchPostInDB):
    pass
