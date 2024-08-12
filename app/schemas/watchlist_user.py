from pydantic import BaseModel


class WatchUserBase(BaseModel):
    pass


class WatchUserUpdate(BaseModel):
    pass


class WatchUserCreate(WatchUserBase):
    following_user_id: int
    followed_user_id: int


class WatchUserInDB(WatchUserBase):
    id: int
    following_user_id: int
    followed_user_id: int

    class Config:
        orm_mode = True


class WatchPost(WatchUserInDB):
    pass
