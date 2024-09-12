from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.schemas import watchlist_post as s_watch_post
from app.crud import watchlist_post as c_watch_post
from app.crud import post as c_post
from app.models import user as m_user
from app.database import get_db

router = APIRouter()


@router.post("/user/{user_id}/watchlist/post/{post_id}/", response_model=s_watch_post.WatchPost)
def create_watch_post_record(user_id: int, post_id: int, db: Session = Depends(get_db),
                             current_user: m_user.User = Depends(get_current_user)):
    """
    Create a watchlist entry for a post by a user.
    """
    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed"
        )
    db_post = c_post.get_post_by_id(db=db, post_id=post_id)
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Post with given Post_id does not exist"
        )
    watch_post = s_watch_post.WatchPostCreate(following_user_id=user_id, followed_post_id=post_id)
    db_watch_post = c_watch_post.create_watchlist_post(db=db, watch_post=watch_post)
    if not db_watch_post:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="User already follows Post."
        )
    return db_watch_post


@router.get("/user/{user_id}/watchlist/post/{post_id}/",
            response_model=list[s_watch_post.WatchPost])
def get_watchlist_post_by_followed_post(user_id: int, post_id: int, db: Session = Depends(get_db),
                                        current_user: m_user.User = Depends(get_current_user)):
    """
    Retrieve all watchlist entries for a specific post followed by a user.
    """
    if user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Authentication failed")
    db_post = c_post.get_post_by_id(db=db, post_id=post_id)
    if not db_post or db_post.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Posts do not exist or User ID has to belong to post to get access."
        )
    db_watch_posts = (c_watch_post.get_watchlist_post_by_followed_post_id
                      (db=db, followed_post_id=post_id))
    if not db_watch_posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post does not get followed by anyone."
        )
    return db_watch_posts


@router.get("/user/{user_id}/watchlist/", response_model=list[s_watch_post.WatchPost])
def get_watchlist_post_by_following_user(user_id: int, db: Session = Depends(get_db),
                                         current_user: m_user.User = Depends(get_current_user)):
    """
    Retrieve all watchlist entries for a user.
    """
    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed"
        )
    db_watch_posts = (c_watch_post.get_watchlist_post_by_following_user_id
                      (db=db, following_user_id=user_id))
    if not db_watch_posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not follow any Post."
        )
    return db_watch_posts


@router.get("/user/{user_id}/watchlist/{watch_post_id}/", response_model=s_watch_post.WatchPost)
def get_watch_post_record_by_watch_post_id(user_id: int, watch_post_id: int,
                                           db: Session = Depends(get_db),
                                           current_user: m_user.User = Depends(get_current_user)):
    """
    Retrieve a specific watchlist entry by its ID.
    """
    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed"
        )
    db_watch_post = c_watch_post.get_watchlist_post_by_id(db=db, watch_post_id=watch_post_id)
    if not db_watch_post or user_id != db_watch_post.following_user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nobody or User does not follow this post"
        )
    return db_watch_post


@router.delete("/user/{user_id}/watchlist/{watch_post_id}/")
def delete_watch_post_record(user_id: int, watch_post_id: int, db: Session = Depends(get_db),
                             current_user: m_user.User = Depends(get_current_user)):
    """
    Delete a watchlist entry by its ID.
    """
    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed"
        )
    db_watch_post = c_watch_post.get_watchlist_post_by_id(db=db, watch_post_id=watch_post_id)
    if not db_watch_post or user_id != db_watch_post.following_user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nobody or User does not follow this post"
        )
    return c_watch_post.delete_watchlist_post(db=db, watch_post_id=watch_post_id)
