from pydantic import BaseModel, ConfigDict


class WatchUserBase(BaseModel):
    """
    Base schema for a watch-user-record.
    """
    pass


class WatchUserUpdate(BaseModel):
    """
    Schema for updating a watch-user-record.
    """
    pass


class WatchUserCreate(WatchUserBase):
    """
    Schema for creating a new watch-user-record.
    """
    following_user_id: int
    followed_user_id: int


class WatchUserInDB(WatchUserBase):
    """
    Schema representing a watch-user-record stored in the database.
    """
    id: int
    following_user_id: int
    followed_user_id: int

    model_config = ConfigDict(arbitrary_types_allowed=True)


class WatchUser(WatchUserInDB):
    """
    Schema for returning watch-user-record data in API responses.
    """
    pass
