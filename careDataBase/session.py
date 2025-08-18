# careDataBase/session.py
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# טוען משתני סביבה
load_dotenv()

# טוען את ה־DB URI מה־.env
DATABASE_URL = os.getenv("DB_URI")
if not DATABASE_URL:
    raise ValueError("❌ DB_URI not found in environment variables (.env file)")

print(f"Connecting with: {DATABASE_URL}")

# יוצר engine ל-SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,   # בודק שהחיבור חי לפני שימוש
    pool_size=5,          # גודל הבריכה
    max_overflow=10,      # כמה חיבורים מעבר לבריכה בעת עומס
    pool_recycle=1800,    # מחזור חיבורים
    future=True,
)

# Session מקומי
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    future=True
)

# פונקציה לקבלת חיבור
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
