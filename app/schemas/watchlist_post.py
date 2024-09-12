from pydantic import BaseModel, ConfigDict


class WatchPostBase(BaseModel):
    """
    Base schema for a watch-post-record.
    """
    pass


class WatchPostUpdate(BaseModel):
    """
    Schema for updating a watch-post-record.
    """
    pass


class WatchPostCreate(WatchPostBase):
    """
    Schema for creating a new watch-post-record.
    """
    following_user_id: int
    followed_post_id: int


class WatchPostInDB(WatchPostBase):
    """
    Schema representing a watch-post-record stored in the database.
    """
    id: int
    following_user_id: int
    followed_post_id: int

    model_config = ConfigDict(arbitrary_types_allowed=True)


class WatchPost(WatchPostInDB):
    """
    Schema for returning watch-post-record data in API responses.
    """
    pass
