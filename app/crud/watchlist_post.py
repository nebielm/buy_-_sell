from sqlalchemy.orm import Session
from app.models import watchlist_post as m_watch_post
from app.schemas import watchlist_post as s_watch_post


def get_watchlist_post_by_id(db: Session, watch_post_id: int):
    return (db.query(m_watch_post.WatchlistPost).filter
            (m_watch_post.WatchlistPost.id == watch_post_id).first())


def get_watchlist_post_by_following_user_id(db: Session, following_user_id: int):
    return (db.query(m_watch_post.WatchlistPost).filter
            (m_watch_post.WatchlistPost.following_user_id == following_user_id).all())


def get_watchlist_post_by_followed_post_id(db: Session, followed_post_id: int):
    return (db.query(m_watch_post.WatchlistPost).filter
            (m_watch_post.WatchlistPost.followed_post_id == followed_post_id).all())


def create_watchlist_post(db: Session, watch_post: s_watch_post.WatchPostCreate):
    existing_watch_post_list = (get_watchlist_post_by_following_user_id
                                (db=db, following_user_id=watch_post.following_user_id))
    if existing_watch_post_list:
        for existing_watch_post in existing_watch_post_list:
            if existing_watch_post.followed_post_id == watch_post.followed_post_id:
                return None
    db_watch_post = m_watch_post.WatchlistPost(**watch_post.model_dump())
    db.add(db_watch_post)
    db.commit()
    db.refresh(db_watch_post)
    return db_watch_post


def update_watchlist_post(db: Session, watch_post_id: int):
    # Does not update, because not intended but existing record is returned
    db_watch_post = get_watchlist_post_by_id(db=db, watch_post_id=watch_post_id)
    if not db_watch_post:
        return None
    return db_watch_post


def delete_watchlist_post(db: Session, watch_post_id: int):
    db_watch_post = get_watchlist_post_by_id(db=db, watch_post_id=watch_post_id)
    if not db_watch_post:
        return None
    db.delete(db_watch_post)
    db.commit()
    return {"status": "successfully deleted"}
