# careDataBase/session.py
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
print(f"Connecting with: {DATABASE_URL}") 

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,   # בודק שהחיבור חי לפני שימוש
    pool_size=5,          # גודל הבריכה (כוון לפי עומס)
    max_overflow=10,      # כמה חיבורים מעבר לבריכה בעת עומס
    pool_recycle=1800,    # מחזור חיבורים כדי להימנע מניתוקי idle
    future=True,
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  # מחזיר את החיבור לבריכה
