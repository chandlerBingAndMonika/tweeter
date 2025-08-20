from careDataBase.session import Base, engine
from sqlalchemy import Column, Integer, String, TIMESTAMP, JSON

class User(Base):
    __tablename__ = "users"

    user_id = Column(String, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    name = Column(String)
    created_at_platform = Column(TIMESTAMP)
    followers_count = Column(Integer)
    following_count = Column(Integer)
    tweet_count = Column(Integer)
    updated_at = Column(TIMESTAMP)


