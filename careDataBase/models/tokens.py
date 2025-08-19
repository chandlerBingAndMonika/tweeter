from sqlalchemy import Column, String, Integer, Boolean, TIMESTAMP, Enum
from sqlalchemy.ext.declarative import declarative_base
import enum
from careDataBase.session import Base, engine
# נניח שיש לך Enum בשם twitter_token_type
class TwitterTokenTypeEnum(enum.Enum):
    APP = "app"
    USER = "user"
    # הוסף ערכים נוספים לפי הצורך

# נניח שיש לך Enum בשם twitter_token_status
class TwitterTokenStatusEnum(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    # הוסף ערכים נוספים לפי הצורך

class Token(Base):
    __tablename__ = "tokens"

    token_name = Column(String, primary_key=True)
    token_type = Column(Enum(TwitterTokenTypeEnum, name="twitter_token_type"), nullable=False)
    token_status = Column(Enum(TwitterTokenStatusEnum, name="twitter_token_status"), nullable=False, server_default="ACTIVE")
    is_active = Column(Boolean, nullable=False, default=True)
    owner_label = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    monthly_read_limit = Column(Integer, nullable=True)
    monthly_read_used = Column(Integer, nullable=False, default=0)
    monthly_reset_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default="now()")
    updated_at = Column(TIMESTAMP, nullable=False, server_default="now()")

# יצירת הטבלה
if __name__ == "__main__":
    print(Base.metadata.tables)
    Base.metadata.create_all(bind=engine)
    print("✅ tokens table ready")
