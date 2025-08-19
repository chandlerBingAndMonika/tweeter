from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, Enum, JSON, ForeignKey, Text
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base
from datetime import datetime, timezone
from careDataBase.session import Base, engine

class ApiCall(Base):
    __tablename__ = "api_calls"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    method = Column(Enum("GET","POST","PUT","DELETE","PATCH","HEAD","OPTIONS", name="http_method"), nullable=False)
    token_name = Column(String, nullable=False)            # מפנה לטבלת tokens.token_name
    status_code = Column(Integer, nullable=False)
    is_success = Column(Boolean, nullable=False)
    error_message = Column(Text, nullable=True)            # הודעת שגיאה אם יש

    # מומלץ להוסיף לפרויקט:
    endpoint = Column(String, nullable=False)              # e.g. "/2/users/:id/tweets"
    url = Column(Text, nullable=False)                     # ה-URL שנקרא בפועל
    query_params = Column(JSONB)                           # פרמטרי השאילתה שנשלחו

    time_cared = Column(Integer(timezone=True), nullable=True)  # זמן הטיפול בפועל של הבקשה

# יצירת הטבלה
if __name__ == "__main__":
    print(Base.metadata.tables)
    Base.metadata.create_all(bind=engine)
    print("✅ api_calls table ready")
