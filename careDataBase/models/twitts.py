from sqlalchemy import Column, String, Integer, BigInteger, TIMESTAMP, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
import enum
from careDataBase.session import Base, engine

# נניח שיש לך Enum בשם tweet_type_enum
class TweetTypeEnum(enum.Enum):
    TWEET = "tweet"
    RETWEET = "retweet"
    REPLY = "reply"
    QUOTE = "quote"

class Tweet(Base):
    __tablename__ = "tweets"

    tweet_id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.user_id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    text = Column(String, nullable=True)
    like_count = Column(Integer, nullable=True)
    retweet_count = Column(Integer, nullable=True)
    reply_count = Column(Integer, nullable=True)
    quote_count = Column(Integer, nullable=True)
    tweet_type = Column(Enum(TweetTypeEnum, name="tweet_type_enum"), nullable=False)
    in_reply_to_user_id = Column(String, nullable=True)
    referenced_retweet_id = Column(String, nullable=True)
    referenced_reply_id = Column(String, nullable=True)
    api_call_id = Column(BigInteger, ForeignKey("api_calls.id", onupdate="CASCADE", ondelete="SET NULL"), nullable=True)
    raw_json = Column(JSONB, nullable=False)
    ingested_at = Column(TIMESTAMP, nullable=False, server_default="now()")

# יצירת הטבלאות
if __name__ == "__main__":
    print(Base.metadata.tables)
    Base.metadata.create_all(bind=engine)
    print("✅ tweets table ready")