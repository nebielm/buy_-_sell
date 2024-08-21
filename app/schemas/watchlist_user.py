from pydantic import BaseModel, ConfigDict


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

    model_config = ConfigDict(arbitrary_types_allowed=True)


class WatchUser(WatchUserInDB):
    pass
