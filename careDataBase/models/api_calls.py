from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, Enum, JSON, ForeignKey, Text
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base
from datetime import datetime, timezone
from base import Base

class ApiCall(Base):
    __tablename__ = "api_calls"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    method = Column(Enum("GET","POST","PUT","DELETE","PATCH","HEAD","OPTIONS", name="http_method"), nullable=False)
    token_name = Column(String, nullable=False)            # מפנה לטבלת tokens.token_name
    status_code = Column(Integer, nullable=False)
    is_success = Column(Boolean, nullable=False)

    duration_ms = Column(Integer)
    user_queried = Column(String)                          # optional: user_id/username
    device_used = Column(String)
    description = Column(Text)

    # מומלץ להוסיף לפרויקט:
    endpoint = Column(String, nullable=False)              # e.g. "/2/users/:id/tweets"
    url = Column(Text, nullable=False)                     # ה-URL שנקרא בפועל
    query_params = Column(JSONB)                           # פרמטרי השאילתה שנשלחו
    response_size_bytes = Column(Integer)

    # רייט-לימיט (מהכותרות)
    rl_limit = Column(Integer)
    rl_remaining = Column(Integer)
    rl_reset_at = Column(DateTime(timezone=True))          # epoch->timestamp

    data_downloaded_at = Column(DateTime(timezone=True))
