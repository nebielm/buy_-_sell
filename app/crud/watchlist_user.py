from sqlalchemy.orm import Session
from app.models import watchlist_user as m_watch_user
from app.schemas import watchlist_user as s_watch_user


def get_watchlist_user_by_id(db: Session, watch_user_id: int):
    return db.query(m_watch_user.WatchlistUser).filter(m_watch_user.WatchlistUser.id == watch_user_id).first()


def get_watchlist_user_by_following_user_id(db: Session, following_user_id: int):
    return db.query(m_watch_user.WatchlistUser).filter(m_watch_user.WatchlistUser.following_user_id ==
                                                       following_user_id).all()


def get_watchlist_user_by_followed_user_id(db: Session, followed_user_id: int):
    return db.query(m_watch_user.WatchlistUser).filter(m_watch_user.WatchlistUser.followed_user_id ==
                                                       followed_user_id).all()


def create_watchlist_user(db: Session, watch_user: s_watch_user.WatchUserCreate):
    existing_watch_user_list = (get_watchlist_user_by_following_user_id
                                (db=db, following_user_id=watch_user.following_user_id))
    if existing_watch_user_list:
        for existing_watch_user in existing_watch_user_list:
            if existing_watch_user.followed_user_id == watch_user.followed_user_id:
                return None
    db_watch_user = m_watch_user.WatchlistUser(**watch_user.model_dump())
    db.add(db_watch_user)
    db.commit()
    db.refresh(db_watch_user)
    return db_watch_user


def update_watchlist_user(db: Session, watch_user_id: int):
    # Does not update, because not intended but existing record is returned
    db_watch_user = get_watchlist_user_by_id(db=db, watch_user_id=watch_user_id)
    if not db_watch_user:
        return None
    return db_watch_user


def delete_watchlist_user(db: Session, watch_user_id: int):
    db_watch_user = get_watchlist_user_by_id(db=db, watch_user_id=watch_user_id)
    if not db_watch_user:
        return None
    db.delete(db_watch_user)
    db.commit()
    return {"status": "successfully deleted"}
