from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.schemas import watchlist_user as s_watch_user
from app.crud import watchlist_user as c_watch_user
from app.crud import user as c_user
from app.models import user as m_user
from app.database import get_db

router = APIRouter()


@router.post("/following_user/{following_user_id}/watchlist/followed_user/{followed_user_id}/",
             response_model=s_watch_user.WatchUser)
def create_watch_user_record(following_user_id: int, followed_user_id: int,
                             db: Session = Depends(get_db),
                             current_user: m_user.User = Depends(get_current_user)):
    """
    Create a watchlist entry for a followed user by a following user.
    """
    if following_user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed"
        )
    db_user = c_user.get_user_by_id(db=db, user_id=followed_user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Followed user does not exist"
        )
    watch_user = s_watch_user.WatchUserCreate(following_user_id=following_user_id,
                                              followed_user_id=followed_user_id)
    db_watch_user = c_watch_user.create_watchlist_user(db=db, watch_user=watch_user)
    if not db_watch_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Following user already follows followed user."
        )
    return db_watch_user


@router.get("/following_user/{following_user_id}/watchlist/{watch_user_id}/",
            response_model=s_watch_user.WatchUser)
def get_watch_user_record_by_watch_user_id(following_user_id: int, watch_user_id: int,
                                           db: Session = Depends(get_db),
                                           current_user: m_user.User = Depends(get_current_user)):
    """
    Retrieve a specific watchlist entry by its ID.
    """
    if following_user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed"
        )
    db_watch_user = c_watch_user.get_watchlist_user_by_id(db=db, watch_user_id=watch_user_id)
    if not db_watch_user or db_watch_user.following_user_id != following_user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Authentication failed or Watch user record does not exist"
        )
    return db_watch_user


@router.get("/followed_user/{followed_user_id}/watchlist/",
            response_model=list[s_watch_user.WatchUser])
def get_watchlist_user_by_followed_user(followed_user_id: int, db: Session = Depends(get_db),
                                        current_user: m_user.User = Depends(get_current_user)):
    """
    Retrieve all watchlist entries for a specific user being followed.
    """
    if followed_user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed"
        )
    db_watch_user = (c_watch_user.get_watchlist_user_by_followed_user_id
                     (db=db, followed_user_id=followed_user_id))
    if not db_watch_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not get followed by anyone."
        )
    return db_watch_user


@router.get("/following_user/{following_user_id}/watchlist/",
            response_model=list[s_watch_user.WatchUser])
def get_watchlist_user_by_following_user(following_user_id: int, db: Session = Depends(get_db),
                                         current_user: m_user.User = Depends(get_current_user)):
    """
    Retrieve all watchlist entries for a user who is following other users.
    """
    if following_user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed"
        )
    db_watch_user = (c_watch_user.get_watchlist_user_by_following_user_id
                     (db=db, following_user_id=following_user_id))
    if not db_watch_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not follow by anyone."
        )
    return db_watch_user


@router.delete("/following_user/{following_user_id}/watchlist/{watch_user_id}/")
def delete_watch_user_record(following_user_id: int, watch_user_id: int,
                             db: Session = Depends(get_db),
                             current_user: m_user.User = Depends(get_current_user)):
    """
    Delete a watchlist entry for a followed user by a following user.
    """
    if following_user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed"
        )
    db_watch_user = c_watch_user.get_watchlist_user_by_id(db=db, watch_user_id=watch_user_id)
    if not db_watch_user or db_watch_user.following_user_id != following_user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Authentication failed or Watch user record does not exist"
        )
    return c_watch_user.delete_watchlist_user(db=db, watch_user_id=watch_user_id)
