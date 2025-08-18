import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
load_dotenv()
engine = create_engine(os.environ["DATABASE_URL"], echo=True)

SQL = """
CREATE TABLE IF NOT EXISTS users (
  user_id                TEXT PRIMARY KEY,
  username               TEXT UNIQUE,
  name                   TEXT,
  created_at_platform    TIMESTAMPTZ,
  followers_count        INTEGER,
  following_count        INTEGER,
  tweet_count            INTEGER,
  listed_count           INTEGER,
  raw_json               JSONB NOT NULL,
  updated_at             TIMESTAMPTZ NOT NULL DEFAULT now()
);
"""

with engine.begin() as conn:
    conn.exec_driver_sql(SQL)
print("✅ users table ready")
