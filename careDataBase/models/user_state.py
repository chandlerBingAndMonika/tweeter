from sqlalchemy import Column, String, Integer, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import TEXT
from careDataBase.session import Base, engine
from careDataBase.models.users import User

class UserState(Base):
    __tablename__ = "user_state"

    user_id = Column(String, ForeignKey("users.user_id", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
    last_seen_id = Column(TEXT, nullable=True)
    oldest_downloaded_tweet_id = Column(TEXT, nullable=True)
    downloaded_tweets_count = Column(Integer, nullable=False, default=0)
    total_tweets_count = Column(Integer, nullable=False, default=0)
    is_limited_access = Column(Boolean, nullable=False, default=False)
    is_tracked = Column(Boolean, nullable=False, default=True)
    updated_at = Column(TIMESTAMP, nullable=False)


