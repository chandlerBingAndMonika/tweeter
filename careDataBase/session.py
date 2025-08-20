# careDataBase/session.py

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import json

# טוען משתני סביבה
load_dotenv()

# לוקח את ה-URL מתוך ה-env
raw_url = os.environ.get("DATABASE_URL")
if not raw_url:
    raise ValueError("❌ DATABASE_URL is not set in environment variables")

# מתקן את הבעיה של postgres://
db_url = raw_url.replace("postgres://", "postgresql+psycopg2://")

print(f"Connecting with: {db_url}")

# יוצר engine
engine = create_engine(db_url, echo=True)

# יוצר Session מקומי
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# בסיס לכל המודלים
Base = declarative_base()

# 🟢 טוען את ה-config פעם אחת ומצרף אותו ל-Base
with open(r"careDataBase\twitter_rate_limits_config.json", "r") as f:
    Base.config = json.load(f)